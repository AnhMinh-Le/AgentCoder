import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.load_settings()
        return cls._instance

    def load_settings(self):
        self.__AZURE_OPENAI__ENDPOINT: str = os.getenv("AZURE_OPENAI__ENDPOINT")
        self.__AZURE_OPENAI__KEY: str = os.getenv("AZURE_OPENAI__KEY")
        self.__AZURE_OPENAI__GPT_DEPLOYMENT_NAME: str = os.getenv(
            "AZURE_OPENAI__GPT_DEPLOYMENT_NAME"
        )
        self.__AZURE_OPENAI__EMBED_DEPLOYMENT_NAME: str = os.getenv(
            "AZURE_OPENAI__EMBED_DEPLOYMENT_NAME"
        )
        self.__AZURE_OPENAI__VERSION: str = os.getenv("AZURE_OPENAI__VERSION")

    @property
    def AZURE_OPENAI__ENDPOINT(self) -> str:
        return self.__AZURE_OPENAI__ENDPOINT

    @property
    def AZURE_OPENAI__KEY(self) -> str:
        return self.__AZURE_OPENAI__KEY

    @property
    def AZURE_OPENAI__GPT_DEPLOYMENT_NAME(self) -> str:
        return self.__AZURE_OPENAI__GPT_DEPLOYMENT_NAME

    @property
    def AZURE_OPENAI__EMBED_DEPLOYMENT_NAME(self) -> str:
        return self.__AZURE_OPENAI__EMBED_DEPLOYMENT_NAME

    @property
    def AZURE_OPENAI__VERSION(self) -> str:
        return self.__AZURE_OPENAI__VERSION


settings = Settings()
