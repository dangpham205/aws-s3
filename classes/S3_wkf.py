import boto3
from utils.utils import write_file, delete_file
from utils.handle_return import HandleReturn
import time
from decouple import config

class S3_wkf():
    
    # content_type sẽ hỗ trợ show image trong browser,
    # còn word, excel sẽ buộc download
    content_types = {
        'word': 'application/msword',
        'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'pdf': 'application/pdf',
        'image': 'image/jpeg',
        'video': 'video/mp4',
        'sound': 'audio/mpeg',
    }
    
    def __init__(self):
        self.__s3 = boto3.resource('s3')
        
    def upload_file(self, bucket_name, upload_file, public_access):
        '''
        upload_file (File): path dẫn tới file cần upload
        bucket_name (str): tên bucket
        key (str): location muốn lưu trong bucket (mặc định ở root của bucket)
        '''
        key = None
        is_image = False

        # Xét xem file có dc hỗ trợ không 
        file_type = self.get_file_type(upload_file.filename)
        if not file_type:
            return HandleReturn().response(500, False, 'Định dạng file không hỗ trợ')
        else:
            timestamp = str(time.time()).replace(".", "")
            key = f"{file_type}/{timestamp}_{upload_file.filename}"

        extra_args = {
            'ContentType': self.content_types[file_type]
        }
        if public_access:
            extra_args['ACL'] = 'public-read'
        
        result = self.upload_to_s3(
            upload_file=upload_file, 
            bucket_name=bucket_name, 
            key=key, 
            extra_args=extra_args
        )
        return result
    
    def upload_to_s3(self, upload_file, bucket_name, key, extra_args):
        try:
            write_file(upload_file)
            self.__s3.meta.client.upload_file(
                upload_file.filename, 
                bucket_name, 
                key,
                ExtraArgs=extra_args
            )
            return HandleReturn().response(200, True, key.split('/')[-1])
        except Exception:
            return HandleReturn().response(500, False, 'Somewhere went wrong')
        finally:
            delete_file(upload_file.filename)
            
    def get_presigned_url(self, file_name, expires_time=60):
        
        bucket_name = config('BUCKET_NAME_WKF')
        key = None
        
        file_type = self.get_file_type(file_name)
        if not file_type:
            return HandleReturn().response(500, False, 'Định dạng file không hỗ trợ')
        else:
            key = file_type+'/'+file_name

        url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object', 
            Params={
                'Bucket': bucket_name, 
                'Key': key,
                'ResponseContentType': self.content_types[file_type]
            },
            ExpiresIn=expires_time #second
        )
        
        data = {
            'uri': url,
            'fileType': self.content_types[file_type]
        }
        
        return HandleReturn().response(200, True, data)
        
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
        
        words = ['doc', 'docx']
        spreadsheet = ['xls', 'xlsx']
        images = ['jpeg', 'jpg', 'png', 'PNG']
        pdf = ['pdf']
        video = ['mp4', 'MP4']
        sound = ['wav', 'mp3', 'MP3']
        
        if file_extension == 'doc' or file_extension == 'docx':
            return 'word'
        elif file_extension == 'xls' or file_extension == 'xlsx':
            return 'excel'
        elif file_extension == 'jpeg' or file_extension == 'png' or file_extension == 'jpg' or file_extension == 'PNG':
            return 'image'
        elif file_extension == 'pdf':
            return 'pdf'
        elif file_extension == 'mp4':
            return 'video'
        elif file_extension == 'mp3' or file_extension == 'wav':
            return 'sound'
        else:
            return False
        
