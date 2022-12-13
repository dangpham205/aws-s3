from pydantic import BaseModel
from fastapi import File, UploadFile


class presigned_schema(BaseModel):
    file_slug: str 
    size: str = None
    expire_time: int = 60
class presigned_schema_wkf(BaseModel):
    file_name: str 
    expires_time: int = 60
    
class upload_multiple_schema(BaseModel):
    file_slug: str
    file: UploadFile = File(...)
    