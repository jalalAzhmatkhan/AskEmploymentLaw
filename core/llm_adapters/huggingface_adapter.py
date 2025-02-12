from typing import List, Optional
from uuid import uuid4

from huggingface_hub import login
import torch
import transformers

from constants.core import (
    DEVICE_CPU,
    DEVICE_CUDA,
    GENERATED_TEXT,
    PIPELINE_TEXT_GENERATION,
    TERMINATOR_TOKEN,
)
from core.logger import logger
from schemas import LLMAdapterMessageRequest, LLMAdapterResponse

class HuggingfaceAdapter:
    """
    LLM Adapter using Huggingface
    """
    def __init__(
        self,
        api_key: str,
        model_id: str,
        chat_template: Optional[str] = "<|start_of_text|>{system_message}\n{user_messages}<|end_of_text|>",
        max_new_token: Optional[int] = 8192
    ):
        """
        Init function
        """
        try:
            login(token=api_key)
        except Exception as e:
            req_id = str(uuid4()).replace("-", "")
            logger.error(f"HuggingfaceAdapter: init: {req_id} Error while logging in to Huggingface:"
                         f"{e}")
            raise ValueError(f"Error occured while requesting session to Huggingface. Request ID: {req_id}")

        self.model_name = model_id
        self.chat_template = chat_template
        self.MAX_NEW_TOKEN = max_new_token

    def format_message(
        self,
        chat_template: str,
        messages: List[LLMAdapterMessageRequest]
    )->str:
        """
        Function to format the message to LLM
        :param chat_template:
        :param messages:
        :return:
        """
        system_msg = []
        user_msg = []

        if "system_messages" not in chat_template or "user_messages" not in chat_template:
            req_id = str(uuid4()).replace("-", "")
            logger.error(f"HuggingfaceAdapter: format_message: {req_id} \"system_messages\" or \"user_messages\" "
                         f"does not exist in the \"chat_template\" parameter. Please check your chat "
                         f"template again!")
            raise ValueError("Wrong chat template!")

        for message in messages:
            if message.role == "system":
                system_msg.append(f"System: {message.content}")
            elif message.role == "user":
                user_msg.append(f"User: {message.content}")
        system_prompt = "\n".join(system_msg)
        user_prompt = "\n".join(user_msg)
        output_chat = chat_template.format(
            system_messages=system_prompt,
            user_messages=user_prompt
        )
        return output_chat

    def infer(self, messages: List[LLMAdapterMessageRequest])->str:
        """
        Function to infer
        :param messages:
        :return:
        """
        device = torch.device(DEVICE_CUDA if torch.cuda.is_available() else DEVICE_CPU)
        logger.info(f"HuggingfaceAdapter: infer: Using device {device}")
        pipeline = transformers.pipeline(
            GENERATED_TEXT,
            model=self.model_name,
            model_kwargs={
                "torch_dtype": torch.bfloat16,
            },
            device=device
        )
        formatted_chat = self.format_message(self.chat_template, messages=messages)
        outputs = pipeline(
            formatted_chat,
            max_new_tokens=self.MAX_NEW_TOKEN
        )
        response = ""
        if len(outputs) > 0:
            response = outputs[0]["generated_text"]
        else:
            req_id = str(uuid4()).replace("-", "")
            logger.warn(f"HuggingfaceAdapter: infer: {req_id} Got 0 response from the LLM {self.model_name}!")
        return response
