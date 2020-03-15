import boto3
import os


def create_object_path(user, obj_name):
    return f"{user.username}/{obj_name}"


class Uploader:

    def __init__(self):
        self.s3 = boto3.resource("s3")
        # create bucket or get it if it exists
        self.bucket = self.s3.create_bucket(Bucket="qcloudtest5517")
        if not os.path.isdir("tmp_media"):
            os.mkdir("tmp_media")

    def upload(self, user, file):
        save_path = create_object_path(user, file)
        with file.open(mode="rb") as up_file:
            self.bucket.upload_fileobj(up_file, save_path)
        return True

    def delete(self, user, filename):
        path = create_object_path(user, filename)
        self.s3.Object(self.bucket.name, path).delete()

    def download(self, user, filename):
        path = create_object_path(user, filename)
        self.bucket.download_file(path, f"tmp_media/{user}/{filename}")


if __name__ == '__main__':
    u = Uploader()
    #u.bucket.objects.delete()
    for item in u.bucket.objects.all():
        print(item)


