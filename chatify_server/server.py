"""
This is the main file for the server. It contains the FastAPI app and the
routes for the API. It also contains the main function to run the server.

"""

from functools import lru_cache
import pathlib
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse

from .prompt_stores.JSONFilePromptStore import JSONFilePromptStore
from .response_providers import OpenAIResponseProvider

from .AppManager import AppManager
from .models import Prompt, PromptID
from .config import ApplicationSettings

app = FastAPI()
# cors:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()
prompt_router = APIRouter(
    prefix="/prompt",
    tags=["prompt"],
    responses={404: {"description": "Not found"}},
)

class Commons:
    def __init__(self, app_manager: AppManager):
        self.app_manager = app_manager


@lru_cache()
def get_commons():
    config = ApplicationSettings()
    return Commons(
        app_manager=AppManager(
            [OpenAIResponseProvider()],
            # prompt_store=DynamoPromptStore(
            #     aws_access_key_id=config.aws_access_key_id,
            #     aws_secret_access_key=config.aws_secret_access_key,
            #     aws_region=config.aws_region,
            #     table_name=config.assignments_table,
            # ),
            JSONFilePromptStore("prompts.json"),
        )
    )


@router.get("/")
async def app_get():
    templates = pathlib.Path(__file__).parent / "templates"
    return HTMLResponse(open(templates / "index.html").read())


@router.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    data = """User-agent: *\nDisallow: /"""
    return data

@prompt_router.get("/")
async def get_all_prompts(
    commons: Annotated[Commons, Depends(get_commons)],
) -> dict[str, dict[PromptID, Prompt]]:
    prompts = await commons.app_manager.get_all_prompts()
    return {"prompts": prompts}

@prompt_router.post("/{prompt_id}/response")
async def get_response(
    prompt_id: PromptID,
    user_text: str,
    commons: Annotated[Commons, Depends(get_commons)],
) -> str:
    try:
        _ = await commons.app_manager.get_prompt(prompt_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Could not retrieve prompt.")

    try:
        response = await commons.app_manager.get_response(prompt_id, user_text)
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Could not generate response.")



app.include_router(router)
app.include_router(prompt_router)


def serve():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9900, workers=4)



async def _serve_debug():

    commons = get_commons()
    prompts = await commons.app_manager.get_all_prompts()
    if len(prompts) == 0:
        await commons.app_manager.add_prompt(Prompt(
            prompt_text="Explain this code in simple words.",
            category="explanations",
            system_prompt="You are a helpful and cheerful software engineer mentor.")
        )

def serve_debug():
    import asyncio
    import uvicorn
    asyncio.run(_serve_debug())
    uvicorn.run(app, host="0.0.0.0", port=9900)