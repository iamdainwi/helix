import asyncio
import httpx

async def run():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "x/flux2-klein:latest",
                "prompt": "test",
                "stream": False
            },
            timeout=120
        )
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            if "image" in data:
                print("Length of image:", len(data["image"]))
                print("Type of image:", type(data["image"]))
                print("Image starts with:", data["image"][:20])
        else:
            print(response.text)

asyncio.run(run())
