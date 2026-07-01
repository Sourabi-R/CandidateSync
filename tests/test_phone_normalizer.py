from src.normalizer.phone_normalizer import PhoneNormalizer


def test_phone_normalizer_formats_e164():
    normalized = PhoneNormalizer.normalize("(415) 555-0100")

    assert normalized == "+14155550100"


def test_phone_normalizer_returns_none_for_invalid_phone():
    assert PhoneNormalizer.normalize("12345") is None
