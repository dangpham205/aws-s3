from fastapi import APIRouter, File, UploadFile
from utils.S3_baongay import S3_baongay
from typing import List
from utils.schemas import *
from decouple import config
from utils.handle_return import HandleReturn

router = APIRouter(
    prefix="",
    tags=["APIS"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(JWTBearer())],
)


@router.post('/upload_single', summary='upload không public')
async def upload(file_slug: str, file: UploadFile = File(...)):
    """
    +file_slug (str): location/new_name mà file sẽ đc lưu\n
    +file (File): file cần upload
    """
    s3 = S3_baongay()
    result = verify_file_type(file.filename, file_slug)
    if not result:
        return HandleReturn().response(500, False, 'Định dạng file bị thay đổi')

    result = s3.upload_file(
        bucket_name = config('BUCKET_NAME'),
        file = file, 
        file_slug=file_slug,
        public_access=False
    )
    return result


@router.post('/get_presigned_url', summary='Lấy presigned url')
async def get_presigned(list: List[presigned_schema]):
    """
    +file_slug (str): tên file cần lấy\n
    +size (str | nullable): nếu là ảnh thì truyền vô, accepted values: 'PC' / 'MOBILE'\n
    +expires_time (int | nullable): số second url có hiệu lực, default 60 seconds\n
    """
    s3 = S3_baongay()
    output = []
    for obj in list:
        result = s3.get_presigned_url(file_slug=obj.file_slug, expire_time=obj.expire_time, size=obj.size)
        output.append(result)
    return output


def verify_file_type(current_file_name, upload_file_name):
    file_name_1 = current_file_name.split('/')[-1]
    file_name_2 = upload_file_name.split('/')[-1]

    file_type_1 = file_name_1.split('.')[-1]
    file_type_2 = file_name_2.split('.')[-1]

    return file_type_1 == file_type_2

        