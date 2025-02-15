import pytest

from src.views import generate_json_response


def test_generate_json_response_invalid_date_format():
    # Неверный формат даты
    with pytest.raises(ValueError):
        generate_json_response("2025-15-02 12:30:00", "dummy_path.xlsx", "dummy_user_settings.json")
