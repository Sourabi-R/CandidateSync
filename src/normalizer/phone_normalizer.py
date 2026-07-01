from __future__ import annotations

from typing import Any

import phonenumbers

from src.config.constants import DEFAULT_PHONE_REGION


class PhoneNormalizer:
    """Normalize phone numbers into E.164 format."""

    @staticmethod
    def normalize(phone: str | None) -> str | None:
        if not phone:
            return None

        try:
            number = phonenumbers.parse(phone, DEFAULT_PHONE_REGION)
            if phonenumbers.is_valid_number(number):
                return phonenumbers.format_number(
                    number,
                    phonenumbers.PhoneNumberFormat.E164,
                )
        except phonenumbers.phonenumberutil.NumberParseException:
            return None
        except Exception:
            return None

        return None
