from typing import List
from uuid import uuid4

from langchain_ollama.chat_models import ChatOllama

from constants.core import (
    HTTP_SCHEME_STR,
    HTTPS_SCHEME_STR,
    LOCALHOST_URI,
    OLLAMA_DEFAULT_PORT,
    OLLAMA_MODELS_LITERAL,
)
from core.logger import logger
from schemas import LLMAdapterMessageRequest, LLMAdapterResponse

class OllamaLangchainAdapter:
    """
    Adapter class for integrating the Ollama model within a LangChain-based framework.

    This class establishes a bridge between the Ollama model and the LangChain
    library, enabling seamless interplay between the two. Its primary purpose is to
    handle and mediate data exchange and decision-making processes between the
    model and LangChain. It supports the efficient utilization of the Ollama model's
    functionalities within LangChain workflows.
    """
    def __init__(
        self,
        chat_model: OLLAMA_MODELS_LITERAL,
        chat_model_tag: str,
        host: str = LOCALHOST_URI,
        port: int = OLLAMA_DEFAULT_PORT,
        temperature: float = 0.
    ):
        """
        Initializes the OllamaLangchainAdapter class.
        :param chat_model:
        :param chat_model_tag:
        :param host:
        :param port:
        :param temperature:
        """
        host_name = host \
            if host.startswith(HTTP_SCHEME_STR) or host.startswith(HTTPS_SCHEME_STR) \
            else HTTP_SCHEME_STR + host
        hosted_ollama_url = f"{host_name}:{port}"
        self.ollama_model = ChatOllama(
            base_url=hosted_ollama_url,
            model=f"{chat_model}:{chat_model_tag}",
            temperature=temperature,
        )

    async def infer(
        self,
        messages: List[LLMAdapterMessageRequest]
    )->LLMAdapterResponse:
        """
        Function for inference using Ollama
        :param messages:
        :return:
        """
        chat_content = ""
        try:
            message_list = [message.model_dump() for message in messages]
            chat_response = await self.ollama_model.ainvoke(message_list)

            if chat_response.content:
                chat_content = chat_response.content
        except Exception as e:
            request_id = str(uuid4()).replace("-", "")
            logger.error(f"OllamaAdapter: chat: {request_id} Error: {e}", exc_info=True)
            raise ValueError(f"Error while processing message from the AI model. Request ID: {request_id}")

        return LLMAdapterResponse(content=chat_content)
