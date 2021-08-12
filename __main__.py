
from utils import *
from prompt_toolkit.completion import PathCompleter

def set_storage_path():
    


read_config()

master_pass = toggle_input("Master Password")

text = "This is the text"

key = create_key(master_pass)


with open("out.txt", "r") as file:
    # file.write(encrypt_text(key, text))
    print(decrypt_text(key, file.read()))

# print(encrypt_text(key, text))
# print(decrypt_text(key,encrypt_text(key, text)))