import os

import pytest
from fastapi import HTTPException

from integration_auth import require_santor_api_key


def test_missing_configuration_returns_service_unavailable(monkeypatch):
    monkeypatch.delenv("SANTOR_API_KEY", raising=False)

    with pytest.raises(HTTPException) as exc:
        require_santor_api_key("x" * 32)

    assert exc.value.status_code == 503


def test_invalid_key_returns_unauthorized(monkeypatch):
    monkeypatch.setenv("SANTOR_API_KEY", "s" * 32)

    with pytest.raises(HTTPException) as exc:
        require_santor_api_key("x" * 32)

    assert exc.value.status_code == 401


def test_valid_key_is_accepted(monkeypatch):
    key = "s" * 32
    monkeypatch.setenv("SANTOR_API_KEY", key)

    require_santor_api_key(key)
