from typing import Optional
from litellm.router import Router


def _get_model_list(
    gemini_api_key: Optional[str] = None
) -> list[dict]:
    extra_headers = {}
    model_list = []

    if gemini_api_key:
        # For using google ai studio, only need to set gemini_api_key
        model_list.extend([
            {
                "model_name": "gemini-2.0-flash",
                "litellm_params": {
                    "model": "gemini/gemini-2.0-flash",
                    "api_key": gemini_api_key,
                    "timeout": 300,
                    "extra_headers": extra_headers,
                },
            },
            {
                "model_name": "gemini-2.5-flash",
                "litellm_params": {
                    "model": "gemini/gemini-2.5-flash-preview-04-17",
                    "api_key": gemini_api_key,
                    "timeout": 300,
                    "extra_headers": extra_headers,
                },
            }
        ])

    return model_list


def get_litellm_router(
    gemini_api_key: Optional[str] = None
) -> Router:
    model_list = _get_model_list(
        gemini_api_key=gemini_api_key,
    )
    return Router(model_list=model_list)
