import os
import shutil
import boto3
import time


def write_file(file):
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        
def delete_file(filename):
    os.remove(filename)
    

def download_file(bucket_name, file, download_location):
    boto3.client('s3').download_file(bucket_name, file, download_location)

    
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