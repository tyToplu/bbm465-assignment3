import os.path
import re, uuid
import requests

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA


class Client:
    def __init__(self, username, serialNumber, mac):
        self.serverUrl = "http://localhost:5000"
        self.publickeyPath = "public.pem"
        self.licensePath = "license.txt"
        self.username = username
        self.serialNumber = serialNumber
        self.MAC = mac
        self.signature = self.create_signature()

    def create_signature(self):
        return "{}${}${}".format(self.username, self.serialNumber, self.MAC)

    def check_license_file_exists(self):
        return os.path.exists(self.licensePath)

    def encrypt(self):
        key = RSA.import_key(open(self.publickeyPath).read())
        cipher = PKCS1_OAEP.new(key)
        signature = self.create_signature()
        return cipher.encrypt(signature.encode())

    def run(self):
        print("Client started...")
        print("My username: " + self.username)
        print("My serial number: " + self.serialNumber)
        print("My MAC: " + self.MAC)
        print(self.check_license_file_exists())
        if self.check_license_file_exists():
            pass
        else:
            pass
        print("Client -- Raw License Text: " + self.create_signature())
        print("Client -- Encrypted License Text: ", end="")
        print(self.encrypt())
        print(self.hashing(self.encrypt()))
        print(self.send_request())

    def hashing(self,plaintext: bytes):
        h = MD5.new()
        h.update(plaintext)
        return h.hexdigest()

    def send_request(self):
        url = 'http://localhost:5000/hash/'

        byte_data = self.encrypt()
        url += byte_data.hex()
        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response.text
            else:
                return response.status_code, response.text

        except requests.exceptions.RequestException as e:
            print('Request error:', e)


def get_mac_address():
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))


if __name__ == "__main__":
    username = "abt"
    serialNumber = "1234-5678-9012"
    MAC = get_mac_address()
    client = Client(username, serialNumber, MAC)
    client.run()
