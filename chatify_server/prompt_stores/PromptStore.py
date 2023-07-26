from typing import Protocol
from ..models import Prompt, PromptID


class PromptStore(Protocol):

    def get_prompt(self, prompt_id: PromptID)  -> Prompt:
        """
        Get a prompt by ID.
        """
        ...

    def get_all_prompts(self) -> dict[PromptID, Prompt]:
        """
        Get all prompts.
        """
        ...

    def add_prompt(self, prompt: Prompt) -> PromptID:
        """
        Add a prompt.
        """
        ...