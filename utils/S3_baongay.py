import boto3
from decouple import config
from utils.handle_return import HandleReturn
from PIL import Image
from utils.utils import write_file, delete_file

class S3_baongay():
    
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
            
    
    def upload_file(self, bucket_name, file_slug, public_access):
        '''
        upload_file (File): path dẫn tới file cần upload
        bucket_name (str): tên bucket
        key (str): location muốn lưu trong bucket (mặc định ở root của bucket)
        '''
        key = None
        is_image = False
        upload_slug = None
        file_name = file_slug.split('/')[-1]
        if file_slug[0] == '/':
            upload_slug = file_slug[1:]
        else:
            upload_slug = file_slug

        # Xét xem file có dc hỗ trợ không 
        file_type = self.get_file_type(file_name)
        if not file_type:
            return HandleReturn().response(500, False, 'Định dạng file không hỗ trợ')
        else:
            if file_type != 'image':
                key = file_type+'/'+upload_slug
            elif file_type == 'image':
                key = file_type+'/'
                is_image = True

        extra_args = {
            'ContentType': self.content_types[file_type]
        }
        if public_access:
            extra_args['ACL'] = 'public-read'
        
        result = self.upload_to_s3(
            file_slug=upload_slug, 
            bucket_name=bucket_name, 
            key=key, 
            extra_args=extra_args,
            is_image=is_image
        )
        return result

            
    def upload_to_s3(self, file_slug, bucket_name, key, extra_args, is_image=False):
        try:
            file_name = file_slug.split('/')[-1]
            write_file(file_slug)
            if is_image:
                image = Image.open(file_name)
                image_resized_PC = image.resize((1170, 1654))
                image_resized_MOBILE = image.resize((640, 905))

                image_resized_PC_name = 'PC_'+file_name
                image_resized_MOBILE_name = 'MOBILE_'+file_name

                image_resized_PC.save(image_resized_PC_name)
                image_resized_MOBILE.save(image_resized_MOBILE_name)
                self.__s3.meta.client.upload_file(
                    image_resized_PC_name, 
                    bucket_name, 
                    f'{key}PC/{file_slug}',
                    ExtraArgs=extra_args
                )
                self.__s3.meta.client.upload_file(
                    image_resized_MOBILE_name, 
                    bucket_name, 
                    f'{key}MOBILE/{file_slug}',
                    ExtraArgs=extra_args
                )
            else:
                self.__s3.meta.client.upload_file(
                    file_name, 
                    bucket_name, 
                    key,
                    ExtraArgs=extra_args
                )
            return HandleReturn().response(200, True, 'Tải lên thành công')
        except Exception:
            return HandleReturn().response(500, False, 'Somewhere went wrong')
        finally:
            if is_image:
                delete_file(image_resized_PC_name)
                delete_file(image_resized_MOBILE_name)
            delete_file(file_name)

    
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
        
            
    def get_presigned_url(self, file_slug, expire_time=60, size=None):
        
        bucket_name = config('BUCKET_NAME')
        file_name = file_slug.split('/')[-1]
        key = None
        
        file_type = self.get_file_type(file_name)
        if not file_type:
            return HandleReturn().response(500, False, 'Định dạng file không hỗ trợ')
        else:
            if file_type != 'image':
                key = file_type+'/'+file_slug
            elif file_type == 'image':
                if size != 'PC' and size != 'MOBILE':
                    return HandleReturn().response(500, False, "Size ảnh phải là 1 trong các giá trị sau: 'PC', 'MOBILE' ")
                else:
                    key = f'{file_type}/{size}/{file_slug}'

        url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object', 
            Params={
                'Bucket': bucket_name, 
                'Key': key
            },
            ExpiresIn=expire_time #second
        )
        
        return HandleReturn().response(200, True, url)

    

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
        
        # if file_extension == 'doc' or file_extension == 'docx':
        #     return 'word'
        # elif file_extension == 'xls' or file_extension == 'xlsx':
        #     return 'excel'
        if file_extension == 'jpeg' or file_extension == 'png' or file_extension == 'jpg' or file_extension == 'PNG':
            return 'image'
        elif file_extension == 'mp4':
            return 'video'
        elif file_extension == 'mp3':
            return 'sound'
        else:
            return False