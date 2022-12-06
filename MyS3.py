import boto3


class MyS3():
    
    
    def __init__(self):
        self.__s3 = boto3.resource('s3')
            
    def get_bucket(self, bucket_name):
        for bucket in self.__s3.buckets.all():
            # print(bucket.name)
            if bucket.name == bucket_name:
                my_bucket = self.__s3.Bucket(bucket.name)
                return my_bucket
        return False
    
    
    def upload_file(self, upload_file, bucket_name, key, file_type, public_access = False):
        '''
        upload_file: path dẫn tới file cần upload
        bucket_name: tên bucket
        key: location muốn lưu trong bucket
        file_type: hiện tại chấp nhận 3 gtri (word | excel | image)
        '''

        # content_type sẽ hỗ trợ show image trong browser,
        # còn word, excel sẽ buộc download
        content_type = {
            'word': 'application/msword',
            'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'image': 'image/jpeg'
        }
            
        # try:
        if public_access:
            print('Starting to upload (public_access)')
            result = self.__s3.meta.client.upload_file(upload_file, 
                                    bucket_name, 
                                    key,
                                    ExtraArgs={
                                        "ContentType": content_type[file_type],
                                        'ACL': 'public-read'
                                    }
            )
        else:
            print('Starting to upload (no public_access)')
            result = self.__s3.meta.client.upload_file(upload_file, 
                                    bucket_name, 
                                    key,
                                    ExtraArgs={
                                        "ContentType": content_type[file_type],
                                    }
            )
        return True
        # except Exception:
        #     print('Somewhere went wrong :D')
        #     return False
        
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
    
    def get_presigned_url(self, bucket, key, expires_time=60):
        url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object', 
            Params={
                'Bucket': bucket, 
                'Key': key
            },
            ExpiresIn=expires_time #second
        )
        return url