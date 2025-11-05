import pathlib
from typing import Annotated, Iterable
from platformdirs import PlatformDirs
from pydantic import BaseModel, Field

from goit_i_pycore_i_personal_assistant.constants.app_info import APP_NAME, APP_AUTHOR
from goit_i_pycore_i_personal_assistant.typing.alias import T_RICH_TEXT


def get_platform_dirs(
    *,
    ensure_exists: bool = False,
) -> PlatformDirs:
    return PlatformDirs(
        appname=APP_NAME,
        appauthor=APP_AUTHOR,
        #
        ensure_exists=ensure_exists,
    )


class AppPaths(BaseModel):
    data_dir: Annotated[pathlib.Path, Field(description="Data directory.")]
    # config_dir: Annotated[pathlib.Path, Field(description="Configuration directory.")]

    def _get_paths(self) -> Iterable[pathlib.Path]:
        return [
            self.data_dir,
            # self.config_dir,
        ]

    def get_for_cli(self) -> T_RICH_TEXT:
        text_as_list = []

        # noinspection PyTypeChecker
        for key in AppPaths.model_fields:
            name = AppPaths.model_fields[key].description or key
            path_as_uri = getattr(self, key).as_uri()
            text_as_list.append(f"[bold green]{name}[/bold green]: {path_as_uri}")

        return "\n".join(text_as_list)

    def remove_all(self):
        for path in self._get_paths():
            if path.exists():
                path.rmdir()


def get_app_paths(
    *,
    ensure_exists: bool = False,
) -> AppPaths:
    platform_dirs = get_platform_dirs(ensure_exists=ensure_exists)
    return AppPaths(
        data_dir=pathlib.Path(platform_dirs.user_data_dir),
        # config_dir=pathlib.Path(platform_dirs.user_config_dir),
    )
