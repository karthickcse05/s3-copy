import boto3
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    source_bucket = os.environ['SOURCE_BUCKET']
    destination_bucket = os.environ['DESTINATION_BUCKET']
    source_prefix = os.environ['SOURCE_PREFIX']  # The folder/key/path in the source bucket

    # List objects in the source bucket with the specified prefix
    response = s3.list_objects_v2(Bucket=source_bucket, Prefix=source_prefix)

    if 'Contents' in response:
        for obj in response['Contents']:
            copy_source = {'Bucket': source_bucket, 'Key': obj['Key']}
            destination_key = obj['Key']  # You can modify this if you want to change the destination key

            # Copy object to the destination bucket
            s3.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=destination_key)

            # Optionally, delete the object from the source bucket
            # s3.delete_object(Bucket=source_bucket, Key=obj['Key'])
    
    return {
        'statusCode': 200,
        'body': 'Transfer complete'
    }

#if __name__ == "__main__":
#    main()
