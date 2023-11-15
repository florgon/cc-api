"""
    Services for pastes.
    Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from app.services.api.errors import ApiErrorException, ApiErrorCode


def validate_paste_text(text: str | None) -> None:
    """
    Skip None value because this function may be used in patch view
    where text is not required.
    """
    if text is None:
        return
    if len(text) < 10 or len(text) > 4096:
        raise ApiErrorException(
            ApiErrorCode.API_INVALID_REQUEST,
            "Paste text must be from 10 to 4096 characters length!"
        )


def validate_paste_language(language: str | None) -> None:
    """
    Skip None value because this function may be used in patch view
    where language is not required.
    """
    if language is None:
        return
    if len(language) == 0 or len(language) > 4096:
        raise ApiErrorException(
            ApiErrorCode.API_INVALID_REQUEST,
            "Paste language must be from 1 to 20 characters length!"
        )
