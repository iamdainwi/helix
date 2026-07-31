import asyncio
import httpx
import json

async def run():
    payload = {
        "model": "hf.co/rectangleworm/ideogram-4-gguf:Q4_K_M",
        "prompt": "A futuristic city in cyberpunk style",
        "stream": False
    }

    async with httpx.AsyncClient(timeout=300) as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json=payload,
        )
        if response.status_code == 200:
            data = response.json()
            if "response" in data:
                print("RESPONSE HEAD:")
                print(data["response"][:500])
        else:
            print(response.text)

asyncio.run(run())
