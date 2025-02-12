import json
from typing import List
from uuid import uuid4

from openai import OpenAI, RateLimitError

from constants.core import OPENAI_LITERAL_MODELS
from core.logger import logger
from schemas import LLMAdapterMessageRequest, LLMAdapterResponse

class OpenAIAdapter:
    """
    LLM Adapter for OpenAI service
    """
    def __init__(self, model: OPENAI_LITERAL_MODELS, api_key: str):
        """
        Initialization function
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def infer(self, messages: List[LLMAdapterMessageRequest])->LLMAdapterResponse:
        """
        Function to do LLM inference using OpenAI
        :param messages:
        :return:
        """
        messages_json = [json.loads(message.json()) for message in messages]
        response = ""
        try:
            ai_response = self.client.chat.completions.create(
                messages=messages_json,
                model=self.model,
                store=True,
                temperature=0.,
            )
            if ai_response.choices[0].message.content:
                response = ai_response.choices[0].message.content
        except RateLimitError:
            req_id = str(uuid4()).replace("-", "")
            logger.error(f"OpenAIAdapter: infer: {req_id} Rate Limit Error!")
            raise ValueError("LLM functionality is having an error because of a Rate Limitation."
                             f"Please contact your administrator. Request ID: {req_id}")

        return LLMAdapterResponse(content=response)

