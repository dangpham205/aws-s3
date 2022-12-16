from fastapi import APIRouter, Depends, File, UploadFile
from utils.S3_wkf import S3_wkf
from utils.schemas import *
from decouple import config
# from depends.auth_bearer import JWTBearer
from depends.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/workflow",
    tags=["Workflow"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(JWTBearer())],
)

@router.get('/')
async def root(regetToken=Depends(JWTBearer())):
    return {'root': 'workflow'}

@router.post('/upload_single', summary='upload không public')
async def upload(file: UploadFile = File(...), regetToken=Depends(JWTBearer())):
    """
    +file (File): file cần upload, must be unique\n
    """
    s3 = S3_wkf()
    result = s3.upload_file(
        upload_file= file, 
        bucket_name = config('BUCKET_NAME_WKF'),
        public_access=False
    )
    return result


@router.post('/get_presigned_url', summary='Lấy presigned url')
async def get_presigned(obj: presigned_schema_wkf, regetToken=Depends(JWTBearer())):
    """
    +file_name (str): tên file cần lấy\n
    +expires_time (int | nullable): số second url có hiệu lực, default 60 seconds\n
    """
    s3 = S3_wkf()
    result = s3.get_presigned_url(file_name=obj.file_name, expires_time=obj.expires_time)
    return result

# @router.post('/upload_multi', summary='upload multiple files (chung dir)')
# async def upload_multi(files: List[UploadFile] = File(...), dir: str = ''):
#     """
#     +file (File): file cần upload\n
#     +dir (str): dir sẽ chứa file, default ở root của bucket\n
#     """
#     for file in files:
#         s3 = MyS3()
#         result = s3.upload_file(
#             upload_file= file, 
#             bucket_name= config('BUCKET_NAME'), 
#             location= dir,
#             public_access=True
#         )
#     return result
    
# @router.delete('/clear_bucket', summary='Xóa hết tất cả file trong bucket')
# async def delete(bucket_name: str):
#     s3 = MyS3()
#     result = s3.clear_bucket(bucket_name)
#     return result

# @router.delete('/delete_file', summary='Xóa file theo tên')
# async def delete( file_name: str, bucket_name: str = None, dir: str = ''):
#     """
#     +bucket_name (str): bucket chứa file cần xóa (HIỆN TẠI KHÔNG SD, KHÔNG CẦN TRUYỀN)\n
#     +file_name (str): tên file cần lấy\n
#     +dir (str): dir chứa file trong bucket, default ở root của bucket\n
#     """
#     s3 = MyS3()
#     bucket_name = config('BUCKET_NAME')
#     result = s3.remove_file(
#         bucket_name=bucket_name, 
#         file_name=file_name, 
#         file_location=dir, 
#         remove_on_cloudfront=False
#     )
#     return  result


# @router.get('/download_file', summary='Download file từ bucket')
# async def down(bucket_name: str, file: str, download_location: str):
#     s3 = MyS3()
#     s3.download_file(bucket_name, file, download_location)
    