from pydantic import BaseModel

PromptID = str

class Prompt(BaseModel):
    """
    A prompt is a string of text to trigger an explanation from an LLM, as well
    as a category and a "system"-facing prompt.

    """

    prompt_text: str
    category: str
    system_prompt: str

