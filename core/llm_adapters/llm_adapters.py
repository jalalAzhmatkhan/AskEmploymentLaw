import asyncio
import json
from typing import Dict, List, Literal, Optional, Union
from uuid import uuid4

from constants.core import (
    KEYWORD_ARGS_HOST,
    KEYWORD_ARGS_IP_ADDR,
    KEYWORD_ARGS_MODEL_TAG,
    KEYWORD_ARGS_PORT,
    KEYWORD_ARGS_TAG,
    LLM_SERVICE_GROQ,
    LLM_SERVICE_HUGGINGFACE,
    LLM_SERVICE_OLLAMA,
    LLM_SERVICE_OLLAMA_VIA_LANGCHAIN,
    LLM_SERVICE_OPENAI,
    OLLAMA_DEFAULT_PORT,
)
from core.llm_adapters.groq_adapter import GroqAdapter
from core.llm_adapters.huggingface_adapter import HuggingfaceAdapter
from core.llm_adapters.ollama_adapter import OllamaAdapter
from core.llm_adapters.ollama_langchain_adapter import OllamaLangchainAdapter
from core.llm_adapters.openai_adapter import OpenAIAdapter
from core.logger import logger
from schemas.core import LLMAdapterMessageRequest, LLMAdapterResponse

class LLMAdapters:
    """
    An Adapter to Connect to LLM service
    """
    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        llm_service: Literal[
            "groq",
            "huggingface",
            "ollama",
            "ollama-langchain",
            "openai"
        ] = LLM_SERVICE_OPENAI,
        **kwargs
    ):
        """
        Init function

        :param model:
        :param api_key:
        :param llm_service:
        :param kwargs:
        """
        self.adapter = None
        self.service = llm_service
        if llm_service == LLM_SERVICE_GROQ:
            self.adapter = GroqAdapter(
                api_key=api_key,
                model=model,
            )
        elif llm_service == LLM_SERVICE_HUGGINGFACE:
            self.adapter = HuggingfaceAdapter(
                api_key=api_key,
                model_id=model
            )
        elif llm_service == LLM_SERVICE_OLLAMA or llm_service == LLM_SERVICE_OLLAMA_VIA_LANGCHAIN:
            if KEYWORD_ARGS_HOST not in kwargs and KEYWORD_ARGS_IP_ADDR not in kwargs:
                req_id = str(uuid4()).replace("-", "")
                logger.error(f"LLMAdapters: init: {req_id} No host for connecting to Ollama service.")
                raise ValueError(f"Error while connecting to the LLM service provider. Request ID: {req_id}")
            if KEYWORD_ARGS_HOST in kwargs and KEYWORD_ARGS_IP_ADDR in kwargs:
                req_id = str(uuid4()).replace("-", "")
                logger.error(f"LLMAdapters: init: {req_id} Use either \"host\" or \"ip_address\" as a parameter "
                             f"for connecting to Ollama service.")
                raise ValueError(f"Error while connecting to the LLM service provider. Request ID: {req_id}")
            if KEYWORD_ARGS_PORT not in kwargs:
                req_id = str(uuid4()).replace("-", "")
                logger.error(f"LLMAdapters: init: {req_id} No port for connecting to Ollama service.")
                raise ValueError(f"Error while connecting to the LLM service provider. Request ID: {req_id}")
            if KEYWORD_ARGS_MODEL_TAG not in kwargs and KEYWORD_ARGS_TAG not in kwargs:
                req_id = str(uuid4()).replace("-", "")
                logger.error(f"LLMAdapters: init: {req_id} No tag info for model selection on the Ollama service.")
                raise ValueError(f"Error while connecting to the LLM service provider. Request ID: {req_id}")
            if KEYWORD_ARGS_MODEL_TAG in kwargs and KEYWORD_ARGS_TAG in kwargs:
                req_id = str(uuid4()).replace("-", "")
                logger.error(f"LLMAdapters: init: {req_id} Use either \"model_tag\" or \"tag\" as a parameter "
                             f"for connecting to Ollama service\'s model.")
                raise ValueError(f"Error while connecting to the LLM service provider. Request ID: {req_id}")
            host = ""
            port = OLLAMA_DEFAULT_PORT
            tag = ""
            if KEYWORD_ARGS_HOST in kwargs and KEYWORD_ARGS_IP_ADDR not in kwargs:
                host = kwargs.get(KEYWORD_ARGS_HOST, "")
            if KEYWORD_ARGS_HOST not in kwargs and KEYWORD_ARGS_IP_ADDR in kwargs:
                host = kwargs.get(KEYWORD_ARGS_IP_ADDR, "")
            if KEYWORD_ARGS_PORT in kwargs:
                port = int(kwargs.get(KEYWORD_ARGS_PORT, OLLAMA_DEFAULT_PORT))
            if KEYWORD_ARGS_MODEL_TAG in kwargs and KEYWORD_ARGS_TAG not in kwargs:
                tag = kwargs.get(KEYWORD_ARGS_MODEL_TAG, "")
            if KEYWORD_ARGS_MODEL_TAG not in kwargs and KEYWORD_ARGS_TAG in kwargs:
                tag = kwargs.get(KEYWORD_ARGS_TAG, "")

            if llm_service == LLM_SERVICE_OLLAMA:
                self.adapter = OllamaAdapter(
                    host=host,
                    model_name=model, # type: ignore
                    port=port,
                    model_tag=tag,
                )
            elif llm_service == LLM_SERVICE_OLLAMA_VIA_LANGCHAIN:
                self.adapter = OllamaLangchainAdapter(
                    host=host,
                    chat_model=model, # type: ignore
                    port=port,
                    chat_model_tag=tag,
                )
        elif llm_service == LLM_SERVICE_OPENAI:
            self.adapter = OpenAIAdapter(
                api_key=api_key,
                model=model,
            )

    def clean_and_parse_response(
        self,
        ai_response: LLMAdapterResponse
    )->Union[List[Dict[str, str]], Dict[str, str]]: # type: ignore
        """
        Function to clean and parse the response from the LLM
        This function will return either a Python Dictionary, or
        a List of Dictionaries, depending on the prompt.
        :param ai_response:
        :return:
        """
        response_from_llm = ai_response.content
        if response_from_llm:
            if isinstance(response_from_llm, str):
                cleaned_response = response_from_llm.replace('```python', '').strip()
                cleaned_response = cleaned_response.replace('```json', '').strip()
                try:
                    return json.loads(cleaned_response)
                except (SyntaxError, ValueError):
                    req_id = str(uuid4()).replace("-", "")
                    logger.error(f"LLMAdapters: clean_and_parse_response: {req_id} Failed to parse response:"
                                 f"{cleaned_response}.")
                    logger.error(f"LLMAdapters: clean_and_parse_response: {req_id} Error detail: {ValueError}",
                                 exc_info=True)
            elif isinstance(response_from_llm, dict):
                return response_from_llm
            else:
                req_id = str(uuid4()).replace("-", "")
                logger.warn(f"LLMAdapters: clean_and_parse_response: {req_id} Unexpected response type:"
                            f"{type(response_from_llm)}")

    async def inference(
        self,
        messages: List[LLMAdapterMessageRequest]
    )->Union[Optional[List[Dict[str, str]]], Optional[Dict[str, str]]]:
        """
        Function to do LLM inference
        :param messages:
        :return:
        """
        if self.service != LLM_SERVICE_OLLAMA and self.service != LLM_SERVICE_OLLAMA_VIA_LANGCHAIN:
            response_from_adapter = self.adapter.infer(messages=messages)
        else:
            response_from_adapter = await self.adapter.infer(messages=messages)
        json_response = self.clean_and_parse_response(response_from_adapter)
        return json_response
