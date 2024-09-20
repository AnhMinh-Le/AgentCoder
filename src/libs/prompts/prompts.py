import os
from dotenv import load_dotenv
from libs.typing import Dataset, Role

load_dotenv()


class Prompts:
    _instance = None

    def __init__(self, role: Role):
        self.__DATASET: str = os.getenv("DATASET")
        self.__HUMANEVAL_PROGRAMMER_PROMPT_PATH: str = os.getenv(
            "HUMANEVAL_PROGRAMMER_PROMPT_PATH"
        )
        self.__HUMANEVAL_TEST_DESIGNER_PROMPT_PATH: str = os.getenv(
            "HUMANEVAL_TEST_DESIGNER_PROMPT_PATH"
        )
        self.__role: Role = role
        self.load_prompts()

    def load_prompts(self):
        if self.DATASET == Dataset.HUMAN_EVAL:
            if self.__role == Role.PROGRAMMER:
                few_shot_prompt_path = self.__HUMANEVAL_PROGRAMMER_PROMPT_PATH
                self.__template_prompt = """
<few_shot_prompt>

**Input Code Snippet**:
```python
<prompt>
```
## Completion 3:
"""
            elif self.__role == Role.TEST_DESIGNER:
                few_shot_prompt_path = self.__HUMANEVAL_TEST_DESIGNER_PROMPT_PATH
                self.__template_prompt = """
<few_shot_prompt>

**Input Code Snippet**:
```python
<prompt>
```
"""
            with open(few_shot_prompt_path, "r") as f:
                self.__few_shot_prompt = f.read()

    @property
    def DATASET(self) -> str:
        return self.__DATASET

    @property
    def few_shot_prompt(self) -> str:
        return self.__few_shot_prompt

    @property
    def role(self) -> str:
        return self.__role

    @property
    def template_prompt(self) -> str:
        return self.__template_prompt

    @template_prompt.setter
    def template_prompt(self, v: dict):
        for key, value in v.items():
            self.__template_prompt = self.__template_prompt.replace(f"<{key}>", value)
