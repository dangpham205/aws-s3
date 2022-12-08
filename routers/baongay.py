from fastapi import APIRouter, File, UploadFile
from MyS3 import MyS3
from typing import List
from utils.schemas import *
from decouple import config

router = APIRouter(
    prefix="",
    tags=["APIS"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(JWTBearer())],
)

@router.get('/')
async def root():
    return {'root': 'root'}

@router.post('/upload_single', summary='upload không public')
async def upload(file: UploadFile = File(...)):
    """
    +file (File): file cần upload, must be unique\n
    """
    s3 = MyS3()
    result = s3.upload_file(
        upload_file= file, 
        bucket_name = config('BUCKET_NAME'),
        public_access=False
    )
    return result


@router.post('/get_presigned_url', summary='Lấy presigned url')
async def get_presigned(obj: presigned_schema):
    """
    +file_name (str): tên file cần lấy\n
    +size (str | nullable): nếu là ảnh thì truyền vô, accepted values: 'PC' / 'MOBILE'\n
    +expires_time (int | nullable): số second url có hiệu lực, default 60 seconds\n
    """
    s3 = MyS3()
    result = s3.get_presigned_url(file_name=obj.file_name, expires_time=obj.expires_time, size=obj.size)
    return result



        