import boto3
from decouple import config
from utils.handle_return import HandleReturn
from PIL import Image
from utils.utils import write_file, delete_file

class S3_public():
    
    # content_type sẽ hỗ trợ show image trong browser,
    # còn word, excel sẽ buộc download
    content_types = {
        # 'word': 'application/msword',
        # 'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'image': 'image/jpeg',
        'video': 'video/mp4',
        'sound': 'audio/mpeg'
    }
    
    def __init__(self):
        self.__s3 = boto3.resource('s3')
        
    def upload_file(self, bucket_name, file, resource_type, public_access):
        '''
        upload_file (File): path dẫn tới file cần upload
        bucket_name (str): tên bucket
        resource_type (str): loại resource (trang nhất,...)
        key (str): location muốn lưu trong bucket (mặc định ở root của bucket)
        '''
        key = None
        file_name = file.filename

        # Xét xem file có dc hỗ trợ không 
        file_type = self.get_file_type(file_name)
        if not file_type:
            return HandleReturn().response(500, False, 'Định dạng file không hỗ trợ')
        else:
            key = file_type+'/'

        extra_args = {
            'ContentType': self.content_types[file_type]
        }
        if public_access:
            extra_args['ACL'] = 'public-read'
        
        result = self.upload_to_s3(
            upload_file=file, 
            bucket_name=bucket_name, 
            key=key, 
            extra_args=extra_args,
            resource_type=resource_type
        )
        return result
    
    def upload_to_s3(self, upload_file, bucket_name, key, extra_args, resource_type):
        try:
            write_file(upload_file)
            file_name = upload_file.filename
            if key.startswith('image/') and resource_type and resource_type == 'TRANG NHẤT':
                image = Image.open(file_name)
                width, height = image.size
                if width > 375: 
                    new_width = 375
                    new_height = new_width * height / width
                    image_resized = image.resize((new_width, new_height))

                    image_resized_name = 'RESIZED_'+file_name

                    image_resized.save(image_resized_name)
                    self.__s3.meta.client.upload_file(
                        image_resized_name, 
                        bucket_name, 
                        key,
                        ExtraArgs=extra_args
                    )
            else:
                self.__s3.meta.client.upload_file(
                    file_name, 
                    bucket_name, 
                    key,
                    ExtraArgs=extra_args
                )
        except Exception:
            return HandleReturn().response(500, False, 'Something went wrong')
        finally:
            if key.startswith('image/') and resource_type and resource_type == 'TRANG NHẤT':
                delete_file(image_resized_name)
            delete_file(file_name)
            return HandleReturn().response(200, True, 'Tải lên thành công')
    
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
        pdf = ['pdf']
        images = ['jpeg', 'jpg', 'png', 'PNG']
        video = ['mp4']
        sound = ['wav', 'mp3']
        
        # if file_extension == 'doc' or file_extension == 'docx':
        #     return 'word'
        # elif file_extension == 'xls' or file_extension == 'xlsx':
        #     return 'excel'
        if file_extension in images:
            return 'image'
        elif file_extension in video:
            return 'video'
        elif file_extension in sound:
            return 'sound'
        else:
            return False