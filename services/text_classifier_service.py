from typing import Dict, List, Literal, Optional, Union

from constants.core import (
    LLM_SERVICE_OPENAI,
    OLLAMA_DEFAULT_PORT,
)
from core.llm_adapters import LLMAdapters
from schemas.core.llm_adapters import LLMAdapterMessageRequest

class TextClassifierService:
    """Text Classifier Service"""

    def __init__(
        self,
        llm_api_key: Optional[str] = None,
        llm_model: Optional[str] = None,
        llm_tag: Optional[str] = None,
        llm_service: Literal[
            "groq",
            "huggingface",
            "ollama",
            "ollama-langchain",
            "openai"
        ] = LLM_SERVICE_OPENAI,
        **kwargs,
    ):
        self.llm_adapters = LLMAdapters(
            api_key=llm_api_key,
            host=kwargs.get("llm_host", ""),
            llm_service=llm_service,
            model=llm_model,
            port=kwargs.get("llm_port", OLLAMA_DEFAULT_PORT),
            tag=llm_tag,
        )

    async def classify(
        self,
        classes: str,
        text: str
    ) -> Optional[Dict[str, str]]:
        """Classify text"""
        messages = []
        system_content = """
            You are an intelligent system that answer the question about a classification task.
            The valid answer should be a clean Python dictionary like: 
            {\"status\": \"200\", \"response\": \"the_answer\"} 
            the answer should be placed as the \"response\" key's value. If you are asked to response
            in Boolean, please put the \"the_answer\" as a string like \"true\" or \"false\".\n\n
            If the class is a binary class, please response with \"true\" or \"false\". Else, please 
            response with the class name. \n
            For example:\n
            **Question Example:** Is the text belongs to the sentiment class: \n\"positive, negative\"?\n
            **Text Example:** This is a good day.\n
            **Answer Example:** {\"status\": \"200\", \"response\": \"true\"}\n
            **Question Example:** Is the text belongs to the sentiment class: \n\"positive, negative\"?\n
            Please answer with \"true\" or \"false\", where \"true\" means \"positive\" and \"false\" means
            \"negative\".\n
            **Text Example:** This is a bad day.\n
            **Answer Example:** {\"status\": \"200\", \"response\": \"false\"}
            **Question Example:** Is the text belongs to the sentiment class: \n\"positive, negative, neutral\"?\n
            **Text Example:** I don't know about the weather today, I think it's so-so.\n
            **Answer Example:** {\"status\": \"200\", \"response\": \"neutral\"}\n
            \n\n
            Now let's start with the real question! \n
            The question: \n
            Is the text belongs to the class:\n 
        """
        system_content += classes
        system_content += """?\n
        The text: \n
        """
        system_message = LLMAdapterMessageRequest(
            role="system",
            content=system_content
        )
        messages.append(system_message)
        user_message = LLMAdapterMessageRequest(
            role="user",
            content=text
        )
        messages.append(user_message)
        response = await self.llm_adapters.inference(messages)
        return response
