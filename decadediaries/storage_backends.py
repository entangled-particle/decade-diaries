from __future__ import annotations

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    S3-backed storage for user-uploaded media.

    Bucket + auth are configured via Django settings:
    - AWS_STORAGE_BUCKET_NAME (required)
    - AWS_S3_REGION_NAME / AWS_S3_ENDPOINT_URL / AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY (optional)
    """

    location = "media"
    default_acl = None
    file_overwrite = False
