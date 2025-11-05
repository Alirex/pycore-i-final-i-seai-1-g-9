import pathlib
import shutil
from typing import Annotated, Iterable
from platformdirs import PlatformDirs
from pydantic import BaseModel, Field

from goit_i_pycore_i_personal_assistant.constants.app_info import APP_NAME, APP_AUTHOR
from goit_i_pycore_i_personal_assistant.typing.alias import T_RICH_TEXT


class DirInfo(BaseModel):
    name: str
    path: pathlib.Path


class AppDirs(BaseModel):
    data_dir: Annotated[pathlib.Path, Field(description="Data directory")]
    # config_dir: Annotated[pathlib.Path, Field(description="Configuration directory")]

    # TODO: (?) Use "config" and "logs" directories

    def _get_paths_info(self) -> Iterable[DirInfo]:
        return [
            DirInfo(name="Data", path=self.data_dir),
            # DirInfo(name="Config", path=self.config_dir),
        ]

    def get_for_cli(self) -> T_RICH_TEXT:
        return "\n".join(
            f"[green bold]{info.name} directory:[/green bold] {str(info.path)}"
            for info in self._get_paths_info()
        )

    def remove_all(self):
        for info in self._get_paths_info():
            if info.path.exists():
                shutil.rmtree(info.path)


def get_app_dirs_in_user_space(
    *,
    ensure_exists: bool = False,
) -> AppDirs:
    """Get application directories in user space."""

    platform_dirs = PlatformDirs(
        appname=APP_NAME,
        appauthor=APP_AUTHOR,
        #
        ensure_exists=ensure_exists,
    )

    return AppDirs(
        data_dir=pathlib.Path(platform_dirs.user_data_dir),
        # config_dir=pathlib.Path(platform_dirs.user_config_dir),
        # log_dir=pathlib.Path(platform_dirs.user_log_dir),
    )
