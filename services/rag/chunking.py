import json
from typing import List, Literal, Optional

from nltk.tokenize import sent_tokenize

from constants.core import llm_adapters as llm_adapters_constants
from core.llm_adapters import LLMAdapters
from core.logger import logger
from schemas import LLMAdapterMessageRequest, LLMAdapterUserMessageRequest
from services.rag.init_nltk_data import init_nltk_data

class Chunking:
    """
    Chunking class to handle chunking of documents.
    """
    def __init__(self, full_text: str):
        """
        Initialize the Chunking class with the full text to be chunked.
        :param full_text:
        """
        init_nltk_data()
        self.full_text = full_text

    def fixed_length(self, chunk_length: int = 1000) -> List[str]:
        """
        Chunk the text into fixed length chunks.
        :param chunk_length:
        :return:
        """
        chunks = []
        for i in range(0, len(self.full_text), chunk_length):
            chunks.append(self.full_text[i:i + chunk_length])
        return chunks

    def sentence_based(self) -> List[str]:
        """
        Chunk the text into sentence based chunks.
        :return:
        """
        chunks = []
        sentences = sent_tokenize(self.full_text)
        for sentence in sentences:
            current_chunk = sentence.strip() + '.'
            if len(current_chunk) > 1:
                chunks.append(current_chunk)
        return chunks

    def paragraph_based(self) -> List[str]:
        """
        Chunk the text into paragraph based chunks.
        :return:
        """
        chunks = []
        paragraphs = self.full_text.split('\n\n')
        for paragraph in paragraphs:
            current_chunk = paragraph.strip()
            if len(current_chunk) > 0:
                chunks.append(current_chunk)
        return chunks

    def sliding_windows(self, n_slide: int = 1) -> List[str]:
        """
        Chunk the text into sliding windows.
        :return:
        """
        sentences = sent_tokenize(self.full_text)
        chunks = [". ".join(sentences[i:i + n_slide]) + "." for i in range(len(sentences) - n_slide + 1)]
        return chunks
