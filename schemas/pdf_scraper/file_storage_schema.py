from pydantic import BaseModel
from typing_extensions import Annotated

from fastapi import File

class FileStorageSchema(BaseModel):
    """
    A schema for Tbl_File_Storage
    """
    document_id: int
    document_file: Annotated[bytes, File()]
