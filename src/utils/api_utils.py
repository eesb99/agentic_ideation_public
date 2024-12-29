import httpx
import os

async def make_api_call(messages, model, purpose):
    """
    Make an asynchronous API call to the DeepSeek V3 API.
    """
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("API key not found in environment variable 'OPENROUTER_API_KEY'.")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "$SITE_URL",  # OpenRouter requires this but accepts $SITE_URL for development
            "X-Title": "Task Agent System"
        }

        payload = {
            "model": model,
            "messages": messages
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    except httpx.HTTPError as http_err:
        print(f"HTTP error occurred in {purpose}: {http_err}")
        if isinstance(http_err, httpx.HTTPStatusError):
            print(f"Error response: {http_err.response.text}")
    except Exception as err:
        print(f"Other error occurred in {purpose}: {err}")
        if 'response' in locals():
            print(f"Response content: {response.text}")
    return None
