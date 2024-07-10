import base64
import hashlib
import secrets
import argparse


from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


arg = argparse.ArgumentParser()
arg.add_argument("--action", type=str, help="Upload, get")
arg.add_argument("--usb", type=str, help="The usb that you want to use")
arg.add_argument("--file", type=str, help="The file that you want to trensfer or get")
arg.add_argument("--key", type=str, help="That key you want to use (32)")

parser = arg.parse_args()


class Data:
    @staticmethod
    def encrypt(data: bytes, key: bytes) -> bytes:
        iv = secrets.token_bytes(16)
        aes = AES.new(key=base64.b64decode(key), mode=AES.MODE_CBC, iv=iv)

        return iv[0:8] + aes.encrypt(pad(data, 16)) + iv[8:]

    @staticmethod
    def decrypt(data: bytes, key: bytes) -> bytes:
        iv = data[0:8] + data[len(data) - 8 :]
        aes = AES.new(key=base64.b64decode(key), mode=AES.MODE_CBC, iv=iv)
        return unpad(aes.decrypt(data[8 : len(data) - 8]), 16)


def main():
    if parser.action == "upload":
        secret_name = hashlib.sha256(parser.file.encode()).hexdigest()

        with open(parser.file, "rb") as read_file_upload, open(
            f"/media/wassoky/{parser.usb}/{secret_name}", "wb"
        ) as write_file_upload:
            data_upload = read_file_upload.read()
            write_file_upload.write(
                Data.encrypt(data=data_upload, key=parser.key.encode())
            )

        print(f"{secret_name}:{parser.file} saved in {parser.usb}")

    elif parser.action == "get":
        secret_name = hashlib.sha256(parser.file.encode()).hexdigest()
        with open(
            f"/media/wassoky/{parser.usb}/{secret_name}", "rb"
        ) as read_file_get, open(parser.file, "wb") as write_file_get:
            data_get = Data.decrypt(data=read_file_get.read(), key=parser.key.encode())
            write_file_get.write(data_get)

        print(f"{secret_name}:{parser.file} has been getted succesfuly")
    else:
        print(f"{parser.action} not found")


if __name__ == "__main__":
    main()
