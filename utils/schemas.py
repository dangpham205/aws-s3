from pydantic import BaseModel
from fastapi import File, UploadFile


class presigned_schema(BaseModel):
    file_name: str 
    size: str = None
    expires_time: int = 60
    