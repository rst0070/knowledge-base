from litellm.router import Router


def _get_model_list(
    openai_api_key: str,
    openai_api_base: str,
    anthropic_api_key: str,
    anthropic_api_base: str,
) -> list[dict]:
    hamlet_headers = {
        "x-feature-id": "ae-answer-evaluator-test",
    }

    return [
        {
            "model_name": "openai/gpt-4o-mini",
            "litellm_params": {
                "model": "azure/gpt-4o-mini",
                "api_key": openai_api_key,
                "api_base": openai_api_base,
                "timeout": 300,
                "stream_timeout": 1,
                "tpm": 150000000,
                "rpm": 25000,
                "base_model": "azure/gpt-4o-mini",
                "custom_llm_provider": "azure",
                "api_version": None,
            },
            "model_info": {"base_model": "openai/gpt-4o-mini"},
        },
        {
            "model_name": "claude-3-7-sonnet",
            "litellm_params": {
                "model": "anthropic/claude-3-7-sonnet-20250219",
                "api_key": anthropic_api_key,
                "api_base": anthropic_api_base,
                "timeout": 300,
                "stream_timeout": 1,
                "extra_headers": hamlet_headers,
            },
        },
    ]


def get_litellm_router(
    openai_api_key: str,
    openai_api_base: str,
    anthropic_api_key: str,
    anthropic_api_base: str,
) -> Router:
    model_list = _get_model_list(
        openai_api_key=openai_api_key,
        openai_api_base=openai_api_base,
        anthropic_api_key=anthropic_api_key,
        anthropic_api_base=anthropic_api_base,
    )
    return Router(model_list=model_list)
