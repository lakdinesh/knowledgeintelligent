import boto3
from botocore.exceptions import ClientError
from config import Config
from botocore.exceptions import ClientError

class S3Storage:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY,
            region_name=Config.AWS_REGION
        )

        self.bucket = Config.AWS_BUCKET_NAME


    def upload_file(self, file_obj, filename):
        try:
            # 🔍 Validate inputs
            if file_obj is None:
                raise ValueError("file_obj is None")

            if not self.bucket:
                raise ValueError("S3 bucket name is None or empty")

            if not filename:
                raise ValueError("filename (S3 key) is None or empty")

            # 🔍 Ensure file_obj is file-like
            if not hasattr(file_obj, "read"):
                raise TypeError("file_obj must be a file-like object with a .read() method")

            # Optional: reset pointer (important!)
            try:
                file_obj.seek(0)
            except Exception:
                pass  # ignore if not seekable

            # 🚀 Upload
            self.s3.upload_fileobj(file_obj, self.bucket, filename)

            return True

        except (ClientError, ValueError, TypeError) as e:
            print(f"Error uploading file: {e}")
            return False  

    # def upload_file(self, file_obj, filename):
    #     try: 
    #         self.s3.upload_fileobj(file_obj, self.bucket, filename)
    #         return True
    #     except ClientError as e:
    #         print(f"Error uploading file: {e}")
    #         return False
        
    
    def get_file(self, filename):
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=filename)
            return response['Body']
        except ClientError as e:
            print(f"Error retrieving file: {e}")
            return None

