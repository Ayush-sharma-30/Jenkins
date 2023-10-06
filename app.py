from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import asyncio

app = FastAPI()


class TriggerRequest(BaseModel):
    text: str


class Config:
    url = "https://jenkins.zwayam.com/job/"
    token = "119afd49520031e5cff545a6d847119459%27"
    auth_token = "c3VyZW5kcmFuYXRoOjExOWFmZDQ5NTIwMDMxZTVjZmY1NDVhNmQ4NDcxMTk0NTk="


async def request(client: httpx.AsyncClient, config: Config):
    response = await client.post(
        url=config.url,
        data={
            "token": config.token
        },
        headers={
            "Authorization": "Basic " + config.auth_token,
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 201:
        return 1
    return 0


@app.post("/trigger_build/")
async def trigger_build(trigger_request: TriggerRequest):
    config = Config()
    config.url = config.url+trigger_request.text+"/build/"
    result =  await task(config=config)
    if result == 1:
        return {
            "msg": "successfully triggered build",
        }
    return {
        "msg": "failed to trigger build"
    }


async def task(config):
    async with httpx.AsyncClient(verify=False) as client:
        tasks = [request(client, config=config) for i in range(100)]
        return await asyncio.gather(*tasks)
        
