"""Info about the app.

Used for defining app-related directories.

Usage example: https://github.com/tox-dev/platformdirs?tab=readme-ov-file#example-output
"""

from typing import Final

APP_NAME: Final[str] = "persyval"
"""Name of the app.

Used as a folder name for app-related directories.

Better to be latin, no spaces.

Must be unique, if possible. Otherwise, can be conflict with other apps.

Must be permanent. Or data can be lost.
"""

APP_AUTHOR: Final[str] = "seai-1-g-9"
"""Author of the app.

Name of the group or company.

Not used on Linux, macOS.
Used on Windows.
"""
