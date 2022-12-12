from fastapi import APIRouter, File, UploadFile
from utils.S3_baongay import S3_baongay
from typing import List
from utils.schemas import *
from decouple import config

router = APIRouter(
    prefix="",
    tags=["APIS"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(JWTBearer())],
)


@router.post('/upload_single', summary='upload không public')
async def upload(resource_slug: str):
    """
    +resource_slug (str): slug tới file cần upload
    """
    s3 = S3_baongay()
    result = s3.upload_file(
        file_slug= resource_slug, 
        bucket_name = config('BUCKET_NAME'),
        public_access=False
    )
    return result


@router.post('/get_presigned_url', summary='Lấy presigned url')
async def get_presigned(list: List[presigned_schema]):
    """
    +file_name (str): tên file cần lấy\n
    +size (str | nullable): nếu là ảnh thì truyền vô, accepted values: 'PC' / 'MOBILE'\n
    +expires_time (int | nullable): số second url có hiệu lực, default 60 seconds\n
    """
    s3 = S3_baongay()
    slug = None
    output = []
    for obj in list:
        if obj.file_slug[0] == '/':
            slug = obj.file_slug[1:]
        else:
            slug = obj.file_slug
        result = s3.get_presigned_url(file_slug=slug, expire_time=obj.expire_time, size=obj.size)
        output.append(result)
    return output



        