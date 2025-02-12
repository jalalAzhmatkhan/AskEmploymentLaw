import json
import time
from typing import List, Tuple
from uuid import uuid4

from groq import Groq, RateLimitError, APIError

from core.logger import logger
from schemas import LLMAdapterMessageRequest, LLMAdapterResponse

class GroqAdapter:
    """
    LLM Adapter for Groq service
    """
    def __init__(self, api_key: str, model: str):
        """
        Initialization function
        :param api_key:
        """
        self.client = Groq(api_key=api_key)
        self.model = model
        self.wait_time = 5

    def infer(self, messages: List[LLMAdapterMessageRequest])->LLMAdapterResponse:
        """
        Function to do inference with Groq
        :param messages:
        :return:
        """
        response = ""
        try:
            llm_response = self.client.chat.completions.create(
                messages=[json.loads(message.json()) for message in messages],
                model=self.model
            )
            llm_response_content = llm_response.choices[0].message.content
            if llm_response_content:
                response = llm_response_content
        except RateLimitError:
            req_id = str(uuid4()).replace("-", "")
            logger.error(f"GroqAdapter: infer: {req_id} Error while doing inference using"
                         f"Groq: Rate Limit reached!")
            waited_time, output = self.retry_infer(
                wait_time_in_second=self.wait_time,
                messages=messages
            )
            self.wait_time += waited_time
            return output
        except APIError as e:
            req_id = str(uuid4()).replace("-", "")
            logger.error(f"GroqAdapter: infer: {req_id} Error while doing inference using"
                         f"Groq: {e}")
            raise ValueError(f"Error while doing inference using Groq. Request ID: {req_id}")
        return LLMAdapterResponse(content=response)

    def retry_infer(
        self,
        wait_time_in_second: int = 5,
        *,
        messages: List[LLMAdapterMessageRequest]
    )->Tuple[int, LLMAdapterResponse]:
        """
        Function to retry the inference
        :param messages:
        :param wait_time_in_second:
        :return:
        """
        time.sleep(wait_time_in_second)
        return wait_time_in_second, self.infer(messages)
