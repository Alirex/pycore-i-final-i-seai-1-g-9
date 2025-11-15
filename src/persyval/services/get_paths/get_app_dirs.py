import pathlib
import shutil
from typing import TYPE_CHECKING, Annotated

from platformdirs import PlatformDirs
from pydantic import BaseModel, Field
from rich.markup import escape

from persyval.constants.app_info import APP_AUTHOR, APP_NAME
from persyval.services.console.types import RichFormattedText

if TYPE_CHECKING:
    from collections.abc import Iterable


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

    def get_for_cli(self) -> RichFormattedText:
        return RichFormattedText(
            "\n".join(
                f"[green bold]{escape(info.name)} directory:[/green bold] {escape(str(info.path))}"
                for info in self._get_paths_info()
            ),
        )

    def remove_all(self) -> None:
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


def get_downloads_dir_in_user_space(
    *,
    ensure_exists: bool = False,
) -> pathlib.Path:
    """Get application downloads directory in user space."""
    return pathlib.Path(PlatformDirs(ensure_exists=ensure_exists).user_downloads_dir)


def get_data_dir_in_user_space(
    *,
    ensure_exists: bool = False,
) -> pathlib.Path:
    """Get application data directory in user space."""
    return get_app_dirs_in_user_space(ensure_exists=ensure_exists).data_dir
