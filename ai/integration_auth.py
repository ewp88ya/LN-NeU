import hmac
import os

from fastapi import Header, HTTPException


def require_santor_api_key(x_ln_neu_api_key: str | None = Header(default=None)) -> None:
    configured_key = os.getenv("SANTOR_API_KEY", "").strip()

    if not configured_key or len(configured_key) < 32:
        raise HTTPException(status_code=503, detail="Santor integration is not configured")

    if not x_ln_neu_api_key or not hmac.compare_digest(x_ln_neu_api_key, configured_key):
        raise HTTPException(status_code=401, detail="Invalid service credentials")
