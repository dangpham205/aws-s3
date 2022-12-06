from pydantic import BaseModel
from fastapi import File, UploadFile


class presigned_schema(BaseModel):
    file_location: str
    file_name: str = None
    file_location: str = None
    expires_time: int = None
    