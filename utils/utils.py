import os
import shutil
import boto3
import time
import urllib.request
from decouple import config
import mutagen
from mutagen.wave import WAVE
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

def write_file(file):
    # domain = config('RESOURCE_URL')
    # source_url = domain+file_slug
    # urllib.request.urlretrieve(source_url , source_url.split('/')[-1])

    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        
def delete_file(filename):
    os.remove(filename)
    

def download_file(bucket_name, file, download_location):
    boto3.client('s3').download_file(bucket_name, file, download_location)

def get_file_duration(file_name):
    file_extension = file_name.split('.')[-1]
    audio1 = ['mp3', 'MP3']
    audio2 = ['wav']
    video = ['mp4', 'MP4']
    if file_extension in audio1:
        file = MP3(file_name)
    elif file_extension in audio2:
        file = WAVE(file_name)
    elif file_extension in video:
        file = MP4(file_name)

    file_info = file.info
    length = int(file_info.length)
    seconds = length + 2  # cộng 2s to be safe
    return seconds
    
def create_cloudfront_invalidation(key, distribution_id):
    client = boto3.client('cloudfront')
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
    invalidation_id = res['Invalidation']['Id']
    return invalidation_id

# def get_bucket(bucket_name):
#     for bucket in self.__s3.buckets.all():
#         # print(bucket.name)
#         if bucket.name == bucket_name:
#             my_bucket = self.__s3.Bucket(bucket.name)
#             return my_bucket
#     return False

# def clear_bucket(self, bucket_name):
#     bucket = self.get_bucket(bucket_name)
#     if bucket:
#         try:
#             for key in bucket.objects.all():
#                 key.delete()
#             return True
#         except Exception:
#             return False
#     return False