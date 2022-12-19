from fastapi import APIRouter, Depends, File, Form, UploadFile
from classes.S3_public import S3_public
from utils.schemas import *
from decouple import config
# from depends.auth_bearer import JWTBearer
from depends.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/public",
    tags=["Public"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(JWTBearer())],
)


@router.post('/upload', summary='upload public')
async def upload(resource_type: str = Form(...), file: UploadFile = File(...), regetToken=Depends(JWTBearer())):
    """
    +reource_type (str): loại resource (TRANG NHẤT, ...)\n
    +file (File): file cần upload, file_name must be unique\n
    """
    s3 = S3_public()
    result = s3.upload_file(
        bucket_name = config('BUCKET_NAME_PUBLIC'),
        file= file, 
        resource_type = str(resource_type),
        public_access=True
    )
    return result

@router.get('/get_url', summary='Lấy presigned url')
async def get_presigned(file_name: str, regetToken=Depends(JWTBearer())):
    """
    +file_name (str): tên file cần lấy\n
    +expires_time (int | nullable): số second url có hiệu lực, default 60 seconds\n
    """
    s3 = S3_public()
    result = s3.get_presigned_url(file_name=file_name)
    return result