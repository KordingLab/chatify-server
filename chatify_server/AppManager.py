from .prompt_stores import PromptStore
from .models import Prompt, PromptID
from .response_providers import ResponseProvider


class AppManager:
    """
    An AppManager handles the retrieval of prompts and combination of prompt+
    user-defined content into an LLM-facing prompt.

    """

    def __init__(self, providers: list[ResponseProvider], prompt_store: PromptStore):
        """
        Construct a new app manager, with a list of language providers and a
        prompt store.

        The AppManager class is designed to be a convenient container to access
        a Commons-compatible object from anywhere in the application.
        """
        self._providers = providers
        self._prompt_store = prompt_store

    async def get_all_prompts(self) -> dict[PromptID, Prompt]:
        """
        Get all prompts from the prompt store.
        """
        return self._prompt_store.get_all_prompts()

    async def get_prompt(self, prompt_id: PromptID) -> Prompt:
        """
        Get a prompt by ID.
        """
        return self._prompt_store.get_prompt(prompt_id)

    async def add_prompt(self, prompt: Prompt) -> PromptID:
        """
        Add a prompt.
        """
        return self._prompt_store.add_prompt(prompt)

    async def get_response(self, prompt_id: PromptID, content: str) -> str:
        """
        Get a response from the language model.
        """
        prompt = await self.get_prompt(prompt_id)
        for provider in self._providers:
            if await provider.can_handle(prompt):
                return await provider.get_response(prompt, content)
        raise ValueError("No provider can handle this prompt.")