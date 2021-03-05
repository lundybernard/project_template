from bat import GlobalConfig

from .configuration.manager import Configuration, dataclass

from .configuration.source import SourceList
from .configuration.sources.args import CliArgsConfig, Namespace
from .configuration.sources.env import EnvConfig
from .configuration.sources.file import FileConfig
from .configuration.sources.dataclass import DataclassConfig


def get_config(
    config_class: dataclass = GlobalConfig,
    cli_args: Namespace = None,
    config_file: FileConfig = None,
    config_file_name: str = None,
    config_env: str = None,
) -> Configuration:

    # Build a prioritized config source list
    config_sources = [
        CliArgsConfig(cli_args) if cli_args else None,
        EnvConfig(),
        config_file if config_file else FileConfig(
            config_file_name, config_env=config_env
        ),
        DataclassConfig(config_class),
    ]

    source_list = config_sources = SourceList(config_sources)

    return Configuration(source_list, config_class)
