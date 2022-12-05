import boto3
from decouple import config

access_key_id = config('ACCESS_KEY_ID')
secret_access_key_id = config('SECRET_ACCESS_KEY_ID')

s3 = boto3.resource('s3', 
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key= secret_access_key_id
                    )
bucket_name = 'haidawng-bucket-1'
upload_file = '/mnt/c/Users/haida/Desktop/web/aws/img.jpg'
upload_location = 'textfiles/img2.jpg'
my_bucket = None

for bucket in s3.buckets.all():
    # print(bucket.name)
    if bucket.name == bucket_name:
        my_bucket = s3.Bucket(bucket.name)

# GHI
# s3.meta.client.upload_file('/mnt/c/Users/haida/Desktop/web/aws/test2.txt', 'haidawng-bucket-1', 'textfiles/test.txt')
# result = s3.meta.client.upload_file(upload_file, 
#                                     bucket_name, 
#                                     upload_location,
#                                     # ExtraArgs={'ACL': 'public-read'}
#                                     )
# print(result)
    
# data = open('test.jpg', 'rb')
# my_bucket.put_object(Key='test.jpg', Body=data)


# XÓA
# xóa file riêng lẻ, không thể xóa folder
# result = s3.meta.client.delete_object(Bucket=bucket_name, Key='dd')
# print(result)

# xóa folder
# bucket.object_versions.all().delete()
for key in my_bucket.objects.all():
    # get all files
    print(key.key)
    if key.key == 'Contract_Manager.png':
        key.delete()

result = my_bucket.object_versions.filter(Prefix="textfiles/").delete()
print(result)
# s3.Object('your-bucket', 'your-key').delete()