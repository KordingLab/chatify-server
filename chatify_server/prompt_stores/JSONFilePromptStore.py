import json
import uuid
from ..models import Prompt, PromptID
from .PromptStore import PromptStore

class JSONFilePromptStore(PromptStore):

    def __init__(self, filename: str):
        self._filename = filename

    def read_file(self) -> dict[PromptID, Prompt]:
        try:
            with open(self._filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get_prompt(self, prompt_id: PromptID) -> Prompt:
        try:
            return Prompt(**self.read_file()[prompt_id])
        except KeyError:
            raise KeyError(prompt_id + " not found")

    def get_all_prompts(self) -> dict[PromptID, Prompt]:
        return self.read_file()

    def add_prompt(self, prompt: Prompt) -> PromptID:
        prompts = self.read_file()
        prompt_id = PromptID(uuid.uuid4())
        prompts[prompt_id] = prompt.model_dump()
        with open(self._filename, "w") as f:
            json.dump(prompts, f)
        return prompt_id

