"""配置管理模块"""
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载环境变量
# 首先尝试加载当前目录的.env
load_dotenv()


class Settings(BaseSettings):
    """应用配置"""

    # 应用基本配置
    app_name: str = "MyAgents"
    app_version: str = "1.0.0"
    debug: bool = False

    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000

    # 日志配置
    log_level: str = "INFO"


# 创建全局配置实例
settings = Settings()


def get_settings() -> Settings:
    """获取配置实例"""
    return settings
