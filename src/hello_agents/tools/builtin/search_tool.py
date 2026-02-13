"""计算器工具"""
import os
from typing import Any, Dict, Iterable, List
from ..base import Tool, ToolParameter

try:
    from tavily import TavilyClient  # type: ignore
except Exception:  # pragma: no cover - 可选依赖
    TavilyClient = None  # type: ignore

CHARS_PER_TOKEN = 4
DEFAULT_MAX_RESULTS = 5
SUPPORTED_RETURN_MODES = {"text", "structured", "json", "dict"}
SUPPORTED_BACKENDS = {
    "tavily"
}

def _limit_text(text: str, token_limit: int) -> str:
    char_limit = token_limit * CHARS_PER_TOKEN
    if len(text) <= char_limit:
        return text
    return text[:char_limit] + "... [truncated]"

def _normalized_result(
    *,
    title: str,
    url: str,
    content: str,
    raw_content: str | None,
) -> Dict[str, str]:
    payload: Dict[str, str] = {
        "title": title or url,
        "url": url,
        "content": content or "",
    }
    if raw_content is not None:
        payload["raw_content"] = raw_content
    return payload

def _structured_payload(
    results: Iterable[Dict[str, Any]],
    *,
    backend: str,
    answer: str | None = None,
    notices: Iterable[str] | None = None,
) -> Dict[str, Any]:
    return {
        "results": list(results),
        "backend": backend,
        "answer": answer,
        "notices": list(notices or []),
    }

class SearchTool(Tool):
    """支持多后端、可返回结构化结果的搜索工具。"""

    def __init__(
        self,
        backend: str = "hybrid",
        tavily_key: str | None = None,
        serpapi_key: str | None = None,
        perplexity_key: str | None = None,
    ) -> None:
        super().__init__(
            name="search",
            description=(
                "智能网页搜索引擎，支持 Tavily后端，可返回结构化或文本化的搜索结果。"
            ),
        )
        self.backend = backend
        self.tavily_key = tavily_key or os.getenv("TAVILY_API_KEY")

        self.available_backends: list[str] = []
        self.tavily_client = None
        self._setup_backends()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self, parameters: Dict[str, Any]) -> str | Dict[str, Any]:  # type: ignore[override]
        query = (parameters.get("input") or parameters.get("query") or "").strip()
        if not query:
            return "错误：搜索查询不能为空"

        backend = str(parameters.get("backend", self.backend) or "hybrid").lower()
        backend = backend if backend in SUPPORTED_BACKENDS else "hybrid"

        mode = str(
            parameters.get("mode")
            or parameters.get("return_mode")
            or "text"
        ).lower()
        if mode not in SUPPORTED_RETURN_MODES:
            mode = "text"

        fetch_full_page = bool(parameters.get("fetch_full_page", False))
        max_results = int(parameters.get("max_results", DEFAULT_MAX_RESULTS))
        max_tokens = int(parameters.get("max_tokens_per_source", 2000))
        loop_count = int(parameters.get("loop_count", 0))

        payload = self._structured_search(
            query=query,
            backend=backend,
            fetch_full_page=fetch_full_page,
            max_results=max_results,
            max_tokens=max_tokens,
            loop_count=loop_count,
        )

        if mode in {"structured", "json", "dict"}:
            return payload

        return self._format_text_response(query=query, payload=payload)

    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="input",
                type="string",
                description="搜索查询关键词",
                required=True,
            ),
        ]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _setup_backends(self) -> None:
        if self.tavily_key and TavilyClient is not None:
            try:
                self.tavily_client = TavilyClient(api_key=self.tavily_key)
                self.available_backends.append("tavily")
                print("✅ Tavily 搜索引擎已初始化")
            except Exception as exc:  # pragma: no cover - 第三方库初始化失败
                print(f"⚠️ Tavily 初始化失败: {exc}")
        elif self.tavily_key:
            print("⚠️ 未安装 tavily-python，无法使用 Tavily 搜索")
        else:
            print("⚠️ TAVILY_API_KEY 未设置")

    def _structured_search(
        self,
        *,
        query: str,
        backend: str,
        fetch_full_page: bool,
        max_results: int,
        max_tokens: int,
        loop_count: int,
    ) -> Dict[str, Any]:
        # 统一将 hybrid 视作 advanced，以保持向后兼容的优先级逻辑
        target_backend = "advanced" if backend == "hybrid" else backend

        if target_backend == "tavily":
            return self._search_tavily(
                query=query,
                fetch_full_page=fetch_full_page,
                max_results=max_results,
                max_tokens=max_tokens,
            )

        raise ValueError(f"Unsupported search backend: {backend}")

    def _search_tavily(
        self,
        *,
        query: str,
        fetch_full_page: bool,
        max_results: int,
        max_tokens: int,
    ) -> Dict[str, Any]:
        if not self.tavily_client:
            message = "TAVILY_API_KEY 未配置或 tavily 未安装"
            raise RuntimeError(message)

        response = self.tavily_client.search(  # type: ignore[call-arg]
            query=query,
            max_results=max_results,
            include_raw_content=fetch_full_page,
        )

        results = []
        for item in response.get("results", [])[:max_results]:
            raw = item.get("raw_content") if fetch_full_page else item.get("content")
            if raw and fetch_full_page:
                raw = _limit_text(raw, max_tokens)
            results.append(
                _normalized_result(
                    title=item.get("title") or item.get("url", ""),
                    url=item.get("url", ""),
                    content=item.get("content") or "",
                    raw_content=raw,
                )
            )

        return _structured_payload(
            results,
            backend="tavily",
            answer=response.get("answer"),
        )

    def _format_text_response(self, *, query: str, payload: Dict[str, Any]) -> str:
        answer = payload.get("answer")
        notices = payload.get("notices") or []
        results = payload.get("results") or []
        backend = payload.get("backend", self.backend)

        lines = [f"🔍 搜索关键词：{query}", f"🧭 使用搜索源：{backend}"]
        if answer:
            lines.append(f"💡 直接答案：{answer}")

        if results:
            lines.append("")
            lines.append("📚 参考来源：")
            for idx, item in enumerate(results, start=1):
                title = item.get("title") or item.get("url", "")
                lines.append(f"[{idx}] {title}")
                if item.get("content"):
                    lines.append(f"    {item['content']}")
                if item.get("url"):
                    lines.append(f"    来源: {item['url']}")
                lines.append("")
        else:
            lines.append("❌ 未找到相关搜索结果。")

        if notices:
            lines.append("⚠️ 注意事项：")
            for notice in notices:
                if notice:
                    lines.append(f"- {notice}")

        return "\n".join(line for line in lines if line is not None)