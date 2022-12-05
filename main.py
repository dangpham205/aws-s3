import boto3
from decouple import config

# có khi tạo user (IAM)
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
# *Cách 1
# result = s3.meta.client.upload_file(upload_file, 
#                                     bucket_name, 
#                                     upload_location,
#                                     # ExtraArgs={'ACL': 'public-read'}
#                                     )
# print(result)

# *Cách 2
# data = open('test.jpg', 'rb')
# my_bucket.put_object(Key='test.jpg', Body=data)


# XÓA
# *Cách 1
# xóa file riêng lẻ, không thể xóa folder
# result = s3.meta.client.delete_object(Bucket=bucket_name, Key='dd')
# print(result)

# *Cách 1
# xóa folder
# bucket.object_versions.all().delete()
# for key in my_bucket.objects.all():
#     # get all files
#     print(key.key)
#     if key.key == 'Contract_Manager.png':
#         key.delete()

# *Cách 2
# result = my_bucket.object_versions.filter(Prefix="textfiles/").delete()
# print(result)

# *Cách 3
# s3.Object('your-bucket', 'your-key').delete()


# RENAME 
# Trong S3 không có rename, nên sẽ copy và xóa file cũ
# Có thể sự dụng để move file

# *Cách 1
s3.Object(bucket_name,'newfolder/aha.jpg').copy_from(CopySource=upload_location)
s3.Object(bucket_name,upload_location).delete()

# *Cách 2
# s3.meta.client.copy_object(Bucket=bucket_name, CopySource=upload_location, Key="newfolder/aha.jpg")
# s3.meta.client.delete_object(Bucket=bucket_name, Key=upload_location)