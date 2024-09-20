import logging
import openai
from libs.config import settings


class Chatter:
    def __init__(self, system_message: str, retries: int = 3, timeout: int = 3):
        self.__retries = retries
        self.__timeout = timeout
        self.__system_message = system_message
        self.__configure_openai()

    @property
    def system_message(self):
        return self.__system_message

    def __configure_openai(self):
        openai.api_key = settings.AZURE_OPENAI__KEY
        openai.api_base = settings.AZURE_OPENAI__ENDPOINT
        openai.api_type = "azure"
        openai.api_version = settings.AZURE_OPENAI__VERSION

    def call_openai_api(self, query: str) -> dict:
        for attempt in range(self.__retries):
            try:
                res = openai.ChatCompletion.create(
                    engine=settings.AZURE_OPENAI__GPT_DEPLOYMENT_NAME,
                    temperature=0 + attempt * 0.1,
                    timeout=self.__timeout,
                    messages=[
                        {"role": "system", "content": self.system_message},
                        {"role": "user", "content": query},
                    ],
                )
                return {"message": str(res["choices"][0]["message"]["content"])}
            except Exception as e:
                logging.error(f"[Chatter] - An exception has occurred. {e}")
        return {"message": ""}

    def postprocess_code_completion(self, completion: str, lan: str = "python") -> str:
        if f"```{lan}" in completion:
            completion = completion[completion.find(f"```{lan}") + len(f"```{lan}") :]
            completion = completion[: completion.find("```")]
        else:
            logging.error("Error: No code block found")
        return completion

    def chat(self, query: str) -> str:
        res = self.call_openai_api(query)["message"]
        return res
