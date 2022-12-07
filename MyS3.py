import boto3
import os
import shutil
from decouple import config
import time
from utils.handle_return import HandleReturn
class MyS3():
    
    # content_type sẽ hỗ trợ show image trong browser,
    # còn word, excel sẽ buộc download
    content_types = {
        'word': 'application/msword',
        'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'image': 'image/jpeg'
    }
    
    def __init__(self):
        self.__s3 = boto3.resource('s3')
            
    def get_bucket(self, bucket_name):
        for bucket in self.__s3.buckets.all():
            # print(bucket.name)
            if bucket.name == bucket_name:
                my_bucket = self.__s3.Bucket(bucket.name)
                return my_bucket
        return False
    
    
    def upload_file(self, upload_file, bucket_name, location, public_access):
        '''
        upload_file (File): path dẫn tới file cần upload
        bucket_name (str): tên bucket
        key (str): location muốn lưu trong bucket (mặc định ở root của bucket)
        '''
        if location != '' and location[-1] != '/':
            location += '/'

        # Xét xem file có dc hỗ trợ không 
        file_type = self.get_file_type(upload_file.filename)
        if not file_type:
            return HandleReturn().response(500, False, 'Định dạng file không hỗ trợ')

        extra_args = {
            'ContentType': self.content_types[file_type]
        }
        if public_access:
            extra_args['ACL'] = 'public-read'

        try:
            self.write_file(upload_file)
            self.__s3.meta.client.upload_file(
                upload_file.filename, 
                bucket_name, 
                location+upload_file.filename,
                ExtraArgs=extra_args
            )
            domain = config('CLOUDFRONT_DOMAIN')
            return {
                'url': f'https://{domain}/{location+upload_file.filename}',
            }
        except Exception:
            return HandleReturn().response(500, False, 'Somewhere went wrong :D')
        finally:
            self.delete_file(upload_file.filename)
        
    def clear_bucket(self, bucket_name):
        bucket = self.get_bucket(bucket_name)
        if bucket:
            try:
                for key in bucket.objects.all():
                    key.delete()
                return True
            except Exception:
                return False
        return False
    
    def remove_file(self, bucket_name, file_name, file_location, remove_on_cloudfront):
        if file_location != '' and file_location[-1] != '/':
            file_location += '/'
        key = file_location+file_name

        if remove_on_cloudfront:
            invalidation_key = '/'+key
            res = self.create_cloudfront_invalidation(key=invalidation_key)
            if not res:
                return HandleReturn().response(500, False, 'Somewhere went wrong :D')

        try:
            self.__s3.meta.client.delete_object(Bucket=bucket_name, Key=key)
            return HandleReturn().response(200, True, 'Xóa thành công')
        except Exception:
            return HandleReturn().response(500, False, 'Somewhere went wrong :D')

    def create_cloudfront_invalidation(self, key):
        client = boto3.client('cloudfront')
        distribution_id = config('CLOUDFRONT_DISTRIBUTION_ID')
        res = client.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': [
                        key
                    ]
                },
                'CallerReference': str(time.time()).replace(".", "")
            }
        )
        # response mẫu
        #{
        #     'Location': 'string',
        #     'Invalidation': {
        #         'Id': 'string',
        #         'Status': 'string',
        #         'CreateTime': datetime(2015, 1, 1),
        #         'InvalidationBatch': {
        #             'Paths': {
        #                 'Quantity': 123,
        #                 'Items': [
        #                     'string',
        #                 ]
        #             },
        #             'CallerReference': 'string'
        #         }
        #     }
        # }
        invalidation_id = res['Invalidation']['Id']
        return invalidation_id
    
    def get_presigned_url(self, bucket, key, expires_time=60):
        url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object', 
            Params={
                'Bucket': bucket, 
                'Key': key
            },
            ExpiresIn=expires_time #second
        )
        return HandleReturn().response(200, True, url)

    def download_file(self, bucket_name, file, download_location):
        boto3.client('s3').download_file(bucket_name, file, download_location)
        # pass
    
    
    def write_file(self, file):
        with open(f'{file.filename}', 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    
    def delete_file(self, filename):
        os.remove(filename)

    def get_file_type(self, filename):
        """
            Trả về file type của file name
            Nếu file không dược hỗ trợ sẽ trả về False
        """
        file_name = filename
        if '/' in filename:
            file_name = filename.split('/')[-1]
        elif '\\' in filename:
            file_name = filename.split('\\')[-1]
        
        file_extension = file_name.split('.')[-1]

        # allowed_file_types = ['doc', 'docx', 'xls', 'xlsx', 'jpeg', 'jpg', 'png', 'PNG']
        
        if file_extension == 'doc' or file_extension == 'docx':
            return 'word'
        elif file_extension == 'xls' or file_extension == 'xlsx':
            return 'excel'
        elif file_extension == 'jpeg' or file_extension == 'png' or file_extension == 'jpg' or file_extension == 'PNG':
            return 'image'
        else:
            return False