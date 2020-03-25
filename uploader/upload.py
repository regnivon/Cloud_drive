import boto3
import os


# create a file path name for the s3 object that is denoted by username and the filename
def get_path(user, obj_name):
    return f"{user.username}/{obj_name}"


class Uploader:

    def __init__(self):
        # get an s3 object from boto, use it to create a bucket
        # or get the bucket should it already exist
        self.s3 = boto3.resource("s3")
        self.bucket = self.s3.create_bucket(Bucket="qcloudtest5517")
        if not os.path.isdir("tmp"):
            os.mkdir("tmp")

    def upload(self, user, file):
        save_path = get_path(user, file)
        with file.open(mode="rb") as up_file:
            self.bucket.upload_fileobj(up_file, save_path)
        return True

    def delete(self, user, filename):
        path = get_path(user, filename)
        self.s3.Object(self.bucket.name, path).delete()

    def download(self, user, filename):
        path = get_path(user, filename)
        self.bucket.download_file(path, f"tmp/{user}/{filename}")

