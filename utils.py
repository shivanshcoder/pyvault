import base64
import json
import os
from base64 import b64encode,b64decode

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
config = {}

def read_config():
    global config
    try:
        with open("config.json", "r") as file:
            config = json.loads(file.read())
    except:
        config = {}

    ## Check if salt exists
    if "salt" in config:
        config['salt'] = b64decode(config['salt'])
    else:
        config['salt'] = os.urandom(16)

    write_config()

def write_config():
    global config
    copy_config=config.copy()
    with open("config.json", "w", encoding='utf-8') as file:
        copy_config['salt'] = b64encode(config['salt'])
        # print(copy_config)
        # print(json.dumps(config))

def create_key(pass_phrase):
    # print(config['salt'])
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=config['salt'],
        # salt=os.urandom(16),
        iterations=10000
    )
    key = base64.urlsafe_b64encode(kdf.derive(pass_phrase.encode()))
    return key



from cryptography.fernet import Fernet
if __name__ == "__main__":
    read_config()
    key = create_key("pass")
    key1 = create_key("pass22")
    f = Fernet(key)
    f1 = Fernet(key1)
    token = f.encrypt(b"Hellow")
    print(token)
    try:
        print(f.decrypt(token))
        print(f1.decrypt(token))
    except:
        pass
    write_config()
