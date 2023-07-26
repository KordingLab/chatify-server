from typing import Optional, Protocol
import guidance

from ..models import Prompt

from ..config import OpenAIConfig


class ResponseProvider(Protocol):

    async def get_response(self, prompt: Prompt, content: str) -> str:
        ...

    async def can_handle(self, prompt: Prompt):
        ...

class OpenAIResponseProvider:
    """
    """

    def __init__(self, config_override: Optional[OpenAIConfig] = None):
        if config_override is not None:
            self.config = config_override
        else:
            self.config = OpenAIConfig()

    async def can_handle(self, prompt: Prompt):
        return prompt is not None

    async def get_response(self, prompt: Prompt, content: str) -> str:
        """

        Returns the feedback.

        Arguments:
            submission: The submission to provide feedback for.
            assignment: The assignment to provide feedback for.
        Returns:
            A list of feedback objects.
        """

        # set the default language model used to execute guidance programs
        try:
            openai_kwargs = self.config.dict()
            guidance.llm = guidance.llms.OpenAI("gpt-3.5-turbo", **openai_kwargs)

            grader = guidance.Program(
                """
            {{#system~}}
            {{ system_prompt }}
            {{~/system}}

            {{#user~}}
            The student has requested your feedback on this content, from a Jupyter Notebook cell:

            ----
            {{ student }}
            ----

            The student has asked for the following help:

            ----
            {{ prompt_text }}
            ----

            Be particularly mindful of scientific rigor issues including confusing correlation with causation, biases, and logical fallacies. You must also correct code errors using your extensive domain knowledge, even if the errors are subtle or minor.

            What do you think of this content?
            {{~/user}}


            {{#assistant~}}
            {{gen 'machine_answer'}}
            {{~/assistant}}
            """
            )

            response = grader(
                prompt_text=prompt.prompt_text,
                system_prompt=prompt.system_prompt,
                student=content,
            )

            return response['machine_answer']
        except Exception as e:
            print(e)
            return ""

__all__ = [
    "OpenAIResponseProvider"
]
