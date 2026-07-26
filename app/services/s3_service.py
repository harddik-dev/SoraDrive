import uuid

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, status

from ..core.config import settings


class S3Service:
    """Wraps all boto3/S3 calls behind a small interface.

    The FastAPI app authenticates to AWS as a dedicated IAM user whose policy
    is scoped to only s3:PutObject / GetObject / DeleteObject / ListBucket on
    this one bucket - never the account's root credentials.
    """

    def __init__(self):
        self.bucket = settings.s3_bucket_name
        self.expires_in = settings.presigned_url_expire_seconds
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )

    def build_file_key(self, user_id: int, filename: str) -> str:
        # Namespacing by user id keeps objects logically separated in the
        # bucket and makes it easy to reason about / audit per-user storage.
        return f"users/{user_id}/{uuid.uuid4()}-{filename}"

    def generate_upload_url(self, file_key: str, content_type: str) -> str:
        try:
            return self.client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self.bucket,
                    "Key": file_key,
                    "ContentType": content_type,
                },
                ExpiresIn=self.expires_in,
            )
        except ClientError as exc:
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY, f"Could not generate upload URL: {exc}"
            )

    def generate_download_url(self, file_key: str) -> str:
        try:
            return self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": file_key},
                ExpiresIn=self.expires_in,
            )
        except ClientError as exc:
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY, f"Could not generate download URL: {exc}"
            )

    def delete_object(self, file_key: str) -> None:
        try:
            self.client.delete_object(Bucket=self.bucket, Key=file_key)
        except ClientError as exc:
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY, f"Could not delete object: {exc}"
            )
