from typing import List, Literal, Optional

from pydantic import SecretStr

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from nltk.tokenize import sent_tokenize

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
            current_chunk = sentence.strip() + '.' if sentence.strip()[-1] != "." else sentence.strip()
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
        chunks = [" ".join(sentences[i:i + n_slide]) for i in range(len(sentences) - n_slide + 1)]
        return chunks

    def semantic_chunking(
        self,
        openai_embedding_api_key: str,
        embedding_dim: int = 1024,
        embedding_model: Literal["text-embedding-3-small", "text-embedding-3-large"] = "text-embedding-3-large",
        threshold_type: Literal["percentile", "standard_deviation", "interquartile", "gradient"] = "gradient",
        breakpoint_threshold_amount: Optional[float] = 95.,
    )->List[str]:
        """
        Chunk the text by its semantic meaning
        :param openai_embedding_api_key:
        :param embedding_dim:
        :param embedding_model:
        :param threshold_type:
        :param breakpoint_threshold_amount:
        :return:
        """
        text_splitter = SemanticChunker(
            OpenAIEmbeddings(
                api_key=SecretStr(openai_embedding_api_key),
                dimensions=embedding_dim,
                model=embedding_model
            ),
            breakpoint_threshold_amount=breakpoint_threshold_amount,
            breakpoint_threshold_type=threshold_type,
        )
        lang_documents = text_splitter.create_documents([self.full_text])
        return [lang_document.page_content for lang_document in lang_documents]

    def recursive_chunking(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """
        Chunk the text into recursive chunks.
        :param chunk_size:
        :param chunk_overlap:
        :return:
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        chunks = text_splitter.split_text(self.full_text)
        return chunks
