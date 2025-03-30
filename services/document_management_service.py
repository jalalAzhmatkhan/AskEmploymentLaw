from datetime import datetime
from typing import List, Literal, Optional

from openai import OpenAI
from pdf2image import convert_from_bytes
import pytesseract
from sqlalchemy.orm import Session
import torch
from transformers import BertModel, BertTokenizer

from constants.services import document_management as document_management_constants
from models import TblDocuments
from repositories import crud_tbl_documents
from schemas import (
    AllDocumentsResponse,
    DocumentsSchema,
)
from services.rag import Chunking

class DocumentManagementService:
    """
    CRUD Service class for Document Management
    """
    def get_all_documents(
        self,
        db: Session,
        limit: int = 10,
        page: int = 1
    )->List[AllDocumentsResponse]:
        """
        Function to get all documents
        :return:
        """
        responses_from_crud = []
        if limit == 0 and page == 0:
            responses_from_crud = crud_tbl_documents.get_all()
        elif limit > 0 and page > 0:
            responses_from_crud = crud_tbl_documents.get_all_limited(db, limit, page)
        responses = [AllDocumentsResponse(
            id=resp.id,
            document_name=resp.document_name,
            document_type=resp.document_type,
            document_description=resp.document_description,
            document_hash=resp.document_hash,
            is_uploaded=resp.is_uploaded,
            uploader_id=resp.uploader_id,
            uploaded_at=resp.uploaded_at,
        ) for resp in responses_from_crud]
        return responses

    def get_uploaded_documents_by_uploader(
        self,
        db: Session,
        uploader_id: int,
        limit: int = 10,
        page: int = 1,
    )->List[AllDocumentsResponse]:
        """
        Function to get all documents uploaded by the current user
        :return:
        """
        responses_from_crud = []
        if limit == 0 and page == 0:
            responses_from_crud = crud_tbl_documents.get_all_by_uploader_id(db, uploader_id)
        elif limit > 0 and page > 0:
            responses_from_crud = crud_tbl_documents.get_all_limited_by_uploader_id(db, uploader_id, limit, page)

        responses = [AllDocumentsResponse(
            id=resp.id,
            document_name=resp.document_name,
            document_type=resp.document_type,
            document_description=resp.document_description,
            document_hash=resp.document_hash,
            is_uploaded=resp.is_uploaded,
            uploader_id=resp.uploader_id,
            uploaded_at=resp.uploaded_at,
        ) for resp in responses_from_crud]

        return responses

    def upload_source_document(
        self,
        db: Session,
        document_name: str,
        document_description: str,
        document_type: str,
        document_hash: str,
        uploader_id: int,
        the_document: bytes,
    )->TblDocuments:
        """
        Function to upload a source document
        :param the_document:
        :param uploader_id:
        :param document_hash:
        :param document_type:
        :param document_description:
        :param document_name:
        :param db:
        :return:
        """
        # Insert the document to the database
        inserted_document = DocumentsSchema(
            document_name=document_name,
            document_description=document_description,
            document_type=document_type,
            document_hash=document_hash,
            is_uploaded=True,
            uploader_id=uploader_id,
            uploaded_at=datetime.now(),
            the_document=the_document
        )
        uploaded_document = crud_tbl_documents.create(db, inserted_document)

        extracted_text = self.pdf_extractor(the_document)
        # Optionally, you can use Chunking to split the text into smaller parts
        chunker = Chunking(extracted_text)
        text_chunks = chunker.sliding_windows(n_slide=5)  # Example: sliding window with 5 sentences

        return uploaded_document

    def delete_document(self, db: Session, document_id: int)->Optional[AllDocumentsResponse]:
        """
        Function to delete a document
        :param db:
        :param document_id:
        :return:
        """
        response_in_db = crud_tbl_documents.delete_by_id(db, document_id)
        if response_in_db:
            return AllDocumentsResponse(
                id=response_in_db.id,
                document_name=response_in_db.document_name,
                document_type=response_in_db.document_type,
                document_description=response_in_db.document_description,
                document_hash=response_in_db.document_hash,
                is_uploaded=response_in_db.is_uploaded,
                uploader_id=response_in_db.uploader_id,
                uploaded_at=response_in_db.uploaded_at,
            )

    def bulk_delete_document(self, db: Session, document_ids: List[int])->List[AllDocumentsResponse]:
        """
        Function to bulk delete documents
        :param db:
        :param document_ids:
        :return:
        """
        response_in_db = crud_tbl_documents.bulk_delete(db, document_ids)
        responses = [AllDocumentsResponse(
            id=resp.id,
            document_name=resp.document_name,
            document_type=resp.document_type,
            document_description=resp.document_description,
            document_hash=resp.document_hash,
            is_uploaded=resp.is_uploaded,
            uploader_id=resp.uploader_id,
            uploaded_at=resp.uploaded_at,
        ) for resp in response_in_db]
        return responses

    def pdf_extractor(self, the_document: bytes)->str:
        """
        Function to extract text from a PDF document
        :param the_document:
        :return:
        """
        try:
            # Convert PDF to a list of PIL images for each page
            # Because not all PDFs are text-based, we need to convert them to images
            images = convert_from_bytes(the_document)

            # Use pytesseract to extract text from each image
            extracted_text = ""
            for image in images:
                text = pytesseract.image_to_string(image)
                extracted_text += text + "\n"  # Append the text with a new line

            return extracted_text.strip()  # Return the full extracted text
        except Exception as e:
            # Handle exceptions (e.g., logging, custom exceptions, etc.)
            print(f"Error during PDF processing: {e}")
            return ""

    def bert_encode(
        self,
        text: str,
        bert_model: Literal["bert-base-uncased", "bert-large-uncased"] = "bert-base-uncased"
    )->List[float]:
        """
        Function to encode text using BERT
        :param text:
        :param bert_model:
        :return:
        """
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load the BERT model and tokenizer
        tokenizer = BertTokenizer.from_pretrained(bert_model)
        model = BertModel.from_pretrained(bert_model)
        model = model.to(device)

        # Tokenize the text
        inputs = tokenizer(text, return_tensors="pt").to(device)

        # Disable gradient calculation
        with torch.no_grad():
            # Get the dense vector from the BERT model
            outputs = model(**inputs)
            return outputs.last_hidden_state.cpu().tolist()

    def openai_embedding(self, text: str, model: str, token: str)->List[float]:
        """
        Function to get an OpenAI embedding from text
        :param token:
        :param model:
        :param text:
        :return:
        """
        # Initialize the OpenAI API
        openai = OpenAI(
            api_key=token
        )

        # Get the OpenAI embedding
        response_openai = openai.embeddings.create(
            input=text,
            model=model,
            dimensions=document_management_constants.BERT_LARGE_EMBEDDING_DIM,
        )
        return response_openai.data[0].embedding

    def get_dense_vector_from_text(
        self,
        text: str,
        embedding_model: Literal[
            "text-embedding-3-small",
            "text-embedding-3-large",
            "text-embedding-ada-002",
            "bert-base-uncased",
            "bert-large-uncased",
        ] = "text-embedding-3-small",
        api_key: Optional[str] = None,
    )->List[float]:
        """
        Function to get a dense vector from text
        :param api_key:
        :param embedding_model:
        :param text:
        :return:
        """
        # Implement the logic to convert text to a dense vector
        response_vectors = []

        if "bert" in embedding_model:
            response_vectors = self.bert_encode(text, embedding_model)  # type: ignore
        elif "text-embedding" in embedding_model:
            # Implement the logic to convert text to a dense vector
            response_vectors = self.openai_embedding(text, embedding_model, api_key)  # type: ignore

        return response_vectors


document_management_service = DocumentManagementService()
