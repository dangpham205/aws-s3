from fastapi import APIRouter, File, UploadFile
from MyS3 import MyS3
import shutil
from typing import List
import os

router = APIRouter(
    prefix="/utils",
    tags=["utils"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(JWTBearer())],
)

@router.post('/upload_single', summary='upload public')
async def upload(file: UploadFile = File(...)):
    result = write_file(file)
    if result:
        s3 = MyS3()
        result = s3.upload_file(
            upload_file= file.filename, 
            bucket_name= 'haidawng-bucket-1', 
            key= file.filename,
            file_type= get_file_type(file.filename), 
            public_access=False
        )
    delete_file(file)
    if result:
        return {
            'host': 'https://haidawng-bucket-1.s3.ap-northeast-1.amazonaws.com/',
            'filename': file.filename,
        }
    return result

@router.post('/upload_multi')
async def upload_multi(files: List[UploadFile] = File(...)):
    for file in files:
        # print(file.file)
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
async def get_presigned(key: str):
    s3 = MyS3()
    
    result = s3.generate_presigned_url(bucket='haidawng-bucket-1', key=key)
    return result

# @router.post('/cms_upload')
# async def upload_multi(files: File()):
#     for file in files:
#         # print(file.file)
#         s3 = MyS3()
#         s3.upload_file(file.file, 'haidawng-bucket-1', file.filename)
#         # s3.upload_file('reqs.txt', 'haidawng-bucket-1', 'reqs.txt')
#         return file.filename


def write_file(file):
    try:
        with open(f'{file.filename}', 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        return True
    except Exception:
        return False
    
def delete_file(file):
    os.remove(file.filename)
    
def get_file_type(filename):
    file_name = filename
    if '/' in filename:
        file_name = filename.split('/')[-1]
    elif '\\' in filename:
        file_name = filename.split('\\')[-1]
    
    file_extension = file_name.split('.')[-1]
    if file_extension == 'doc' or file_extension == 'docx':
        return 'word'
    if file_extension == 'xls' or file_extension == 'xls':
        return 'excel'
    if file_extension == 'jpeg' or file_extension == 'png' or file_extension == 'jpg' or file_extension == 'PNG':
        return 'image'

        