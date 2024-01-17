from EncodeurDecodeur import EncodeurDecodeur
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384
import os
import base64


class Signateur(EncodeurDecodeur):
    def __init__(self, image):
        super().__init__(image)
        self.private_key = None
        self.public_key = None
        self.signer = None
        self.MESSAGE_SPLIT = "$$$$$$$"

    def generate_keys(self):
        print("generating keys...")
        key = RSA.generate(2048)
        self.private_key = key.export_key()
        self.public_key = key.publickey().export_key()

    def save_keys(self):
        file_out = open("private.pem", "wb")
        file_out.write(self.private_key)
        file_out.close()

        file_out = open("public.pem", "wb")
        file_out.write(self.public_key)
        file_out.close()

    def get_key(self, key):
        # try to load keys from file if exists
        if os.path.isfile("private.pem"):
            file_in = open("private.pem", "rb")
            self.private_key = RSA.import_key(file_in.read())
            file_in.close()
        elif (key == 'private'):
            self.generate_keys()
            self.save_keys()

        if os.path.isfile("public.pem"):
            file_in = open("public.pem", "rb")
            self.public_key = RSA.import_key(file_in.read())
            file_in.close()
        elif (key == 'public'):
            raise Exception("public key not found")

    def str_to_bytes(self, message):
        return bytes(message, 'utf-8')

    def encode(self, message, output="output.png"):
        self.get_key('private')
        return self.sign_message(message, output)

    def decode(self):
        self.get_key('public')
        return self.decode_signed()

    def sign_message(self, message, output="output.png"):
        signer = pkcs1_15.new(self.private_key)
        h = SHA384.new(data=self.str_to_bytes(message))
        signature = signer.sign(h)
        # signature as hexdigest
        encoded_sign = signature.hex() + self.MESSAGE_SPLIT + \
            message
        # add signature to message splited by MESSAGE_SPLIT
        return self.write(encoded_sign, output)

    def decode_signed(self):
        encoded_infos = super().read()

        signature = encoded_infos.split(self.MESSAGE_SPLIT)[0]
        message = encoded_infos.split(self.MESSAGE_SPLIT)[1]
        h = SHA384.new(data=self.str_to_bytes(message))
        s_bytes = bytes.fromhex(signature)
        try:
            pkcs1_15.new(self.public_key).verify(h, s_bytes)
            print("The signature is authentic.")
            print("message: ", message)
            return message
        except ValueError:
            print("The signature is not authentic. Message is corrupted.")

    def verify(self, message):
        return self.decode() == message
