import os

from pathlib import Path
from typing import Optional, List,  Tuple, Type, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource
from functools import lru_cache

from datenstrom.common.settings import JsonConfigSettingsSource

_config_dir = os.path.dirname(os.path.realpath(__file__))
_base_dir = os.path.abspath(os.path.join(_config_dir, ".."))


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding='utf-8')

    base_dir: str = _base_dir
    asset_dir: str = os.path.join(_base_dir, "assets")
    max_bytes: int = 190000  # 190 kB < 256 kb after base64 for SQS

    vendors: List[str] = [
        "com.ruzd"
    ]
    enable_redirect_tracking: bool = False

    iglu_schema_registries: List[str] = [
        "http://iglucentral.com/schemas/",
    ]

    geoip_enabled: bool = False
    download_geoip_db: bool = False
    geoip_db_url: str = "https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb"
    geoip_db_file: str = "GeoLite2-City.mmdb"

    record_format: Literal["thrift", "avro"]
    sink: Literal["dev", "kafka", "sqs"]

    sqs_queue_raw: Optional[str] = None
    sqs_queue_events: Optional[str] = None
    sqs_queue_errors: Optional[str] = None

    kafka_topic: str = "datenstrom_raw"
    kafka_brokers: Optional[str] = None

    cookie_enabled: bool = True
    cookie_expiration_days: int = 365
    cookie_name: str = "sp"
    cookie_secure: bool = True
    cookie_http_only: bool = True
    cookie_same_site: str = "None"

    cookie_domains: Optional[List[str]] = None
    cookie_fallback_domain: Optional[str] = None

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            JsonConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )

    def get(self, key, default=None):
        return getattr(self, key, default)


@lru_cache()
def get_settings():
    config_cls = BaseConfig
    return config_cls()


config = get_settings()
