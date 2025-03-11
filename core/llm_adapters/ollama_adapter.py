from typing import List
from uuid import uuid4

import ollama
from ollama import AsyncClient

from constants.core import (
    HTTP_SCHEME_STR,
    HTTPS_SCHEME_STR,
    LOCALHOST_URI,
    MODEL_TAG_LATEST,
    OLLAMA_DEFAULT_PORT,
    OLLAMA_MODELS_LITERAL,
)
from core.logger import logger
from schemas import LLMAdapterMessageRequest, LLMAdapterResponse

class OllamaAdapter:
    """
    LLM Adapter using Ollama
    """
    def __init__(
        self,
        host: str = LOCALHOST_URI,
        *,
        model_name: OLLAMA_MODELS_LITERAL,
        model_tag: str = MODEL_TAG_LATEST,
        port: int = OLLAMA_DEFAULT_PORT
    ):
        """
        Init function
        :param model_name:
        :param model_tag:
        """
        self.model_name = f"{model_name}:{model_tag}"
        host_name = host \
            if host.startswith(HTTP_SCHEME_STR) or host.startswith(HTTPS_SCHEME_STR) \
            else HTTP_SCHEME_STR + host
        self.hosted_ollama_url = f"{host_name}:{port}"

    async def download_model(self, model_name: str):
        client = AsyncClient(
            host=self.hosted_ollama_url
        )
        try:
            logger.info(f"OllamaAdapter: download_model: Downloading the {model_name} model...")
            await client.pull(model=model_name)
            logger.info("OllamaAdapter: download_model: Download initiated.")
        except Exception as e:
            request_id = str(uuid4()).replace("-", "")
            logger.error(f"OllamaAdapter: download_model error: {request_id} {e}", exc_info=True)
            raise RuntimeError(e)

    async def prestart_check(self):
        """
        Function to check the Ollama service before ready to be used
        :return:
        """
        client = AsyncClient(
            host=self.hosted_ollama_url
        )
        get_current_models = await client.list()
        current_models = get_current_models.models
        models_name = [model.model for model in current_models]

        if self.model_name not in models_name:
            logger.warn(f"OllamaAdapter: prestart_check: the model {self.model_name} does not exist. "
                        f"Downloading the {self.model_name} model...")
            await self.download_model(self.model_name)
        else:
            logger.info(f"OllamaAdapter: prestart_check: the model {self.model_name} exists and "
                        f"ready to be used.")

    async def infer(
        self,
        messages: List[LLMAdapterMessageRequest]
    )->LLMAdapterResponse:
        """
        Function to chat with Ollama model
        :param messages:
        :return:
        """
        await self.prestart_check()  # Check if the model is ready to be used

        client = AsyncClient(
            host=self.hosted_ollama_url
        )
        chat_content = ""
        try:
            messages_list = [message.model_dump() for message in messages]
            chat_response = await client.chat(
                model=self.model_name,
                messages=messages_list,
            )

            if chat_response.message.content:
                chat_content = chat_response.message.content
        except (ollama.ResponseError, Exception) as e:
            request_id = str(uuid4()).replace("-", "")
            logger.error(f"OllamaAdapter: chat: {request_id} Error: {e}", exc_info=True)
            raise ValueError(f"Error while processing message from the AI model. Request ID: {request_id}")

        response = LLMAdapterResponse(
            content=chat_content
        )

        return response
