from fastapi import APIRouter, File, UploadFile
from MyS3 import MyS3
from typing import List
from schemas import *

router = APIRouter(
    prefix="/utils",
    tags=["utils"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(JWTBearer())],
)

@router.post('/upload_single', summary='upload public')
# async def upload(file: UploadFile = File(...), file_location: str = ''):
async def upload(file: UploadFile = File(...), file_location: str = ''):
    """
    +file (File): file cần upload\n
    +file_location (str): dir sẽ chứa file, default ở root của bucket\n
    """
    s3 = MyS3()
    result = s3.upload_file(
        upload_file= file, 
        bucket_name= 'haidawng-bucket-1', 
        location= file_location,
        public_access=True
    )
    return result

@router.post('/upload_multi')
async def upload_multi(files: List[UploadFile] = File(...)):
    for file in files:
        s3 = MyS3()
        s3.upload_file(file.file, 'haidawng-bucket-1', file.filename)
        # s3.upload_file('reqs.txt', 'haidawng-bucket-1', 'reqs.txt')
        return file.filename
    
@router.delete('/clear_bucket', summary='Xóa hết tất cả file trong bucket')
async def delete(bucket_name: str):
    s3 = MyS3()
    result = s3.clear_bucket(bucket_name)
    return result

@router.delete('/delete_file', summary='Xóa file theo tên')
async def delete(file_name: str):
    s3 = MyS3()
    return 

@router.get('/get_presigned_url', summary='Lấy presigned url')
async def get_presigned(bucket_name: str, file_name: str, file_location: str = '', expires_time: int = 60):
    """
    +bucket_name (str): bucket chứa file cần lấy\n
    +file_name (str): tên file cần lấy\n
    +file_location (str): dir chứa file trong bucket, default ở root của bucket\n
    +expires_time (int): số second url có hiệu lực\n
    """
    if file_location[-1] != '/':
        file_location += '/'
    s3 = MyS3()
    result = s3.get_presigned_url(bucket=bucket_name, key=file_location+file_name, expires_time=expires_time)
    return result

    

        