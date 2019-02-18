import oss2
from config.constant import Config

key = Config.OSS_KEY
secret = Config.OSS_SECRET
endpoint = Config.OSS_ENDPOINT
bucket_name = Config.OSS_BUCKET

auth = oss2.Auth(key, secret)
client = oss2.Bucket(auth, endpoint, bucket_name)


def upload_file(key_name, file):
    a = client.put_object(key_name, file)
    return a


def download_file(key_name):
    return client.get_object(key_name)


def generate_url(key_name, expire=300):
    return client.sign_url(method='PUT', key=key_name, expires=expire)