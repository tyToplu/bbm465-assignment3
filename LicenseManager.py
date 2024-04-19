import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
from flask import Flask

privKeyPath = "private.pem"
publicKeyPath = "public.pem"
app = Flask(__name__)

@app.route("/")
def running():
    return "<p>Server is running</p>"

@app.route("/encrypt/<plaintext>")
def encrypt(plaintext):
    key = RSA.import_key(open(publicKeyPath).read())
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(plaintext.encode())
    print(ciphertext)
    return f"<h1>{ciphertext}</h1>"

@app.route("/hash/<plaintext>")
def hashing(plaintext:str):
    h = MD5.new()
    h.update(str.encode(plaintext))
    return h.hexdigest()


####################################
#       INSERT YOUR CODE HERE      #
####################################


if __name__ == "__main__":
    # DO NOT CHANGE BELOW
    app.run(host='0.0.0.0', port=5000, debug=True)
