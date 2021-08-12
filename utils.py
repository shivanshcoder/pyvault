import base64
import json
import os
import threading
from base64 import b64encode,b64decode

from prompt_toolkit import prompt
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings

from prompt_toolkit.validation import Validator
from prompt_toolkit.completion import PathCompleter
 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken


class configuration:
    config = {}
    session_master_password=""
    storage_path = ""


    def __init__(self, storage_path, session_master_password):
        self.storage_path = storage_path
        self.session_master_password = session_master_password

        self.read_config()



    # TODO
    # def session_reset(self):
    #     # Spawns a thread which resets the session_master_password and all the unencrypted data gets thrown away
    #     # 
    #     def deleter(config_ref):
    #         config_ref.
    #     self.__watcher = threading.Thread(target=deleter,args=(self,))
    #     self.__watcher.start() 

    def read_config(self):
        file_path = os.path.join(self.storage_path, "data.json")
        try:
            # Try Opening the configuration file and read the configuration
            with open(file_path, "r") as file:

                # Read using JSON format
                self.config = json.loads(file.read())
        except:
            # Start from scratch
            self.config = {'secret':{}}


        ## Check if salt exists
        if "salt" in self.config:
            self.config['salt'] = b64decode(self.config['salt'])
        else:
            # Create a new salt for the data encryption
            self.config['salt'] = os.urandom(16)

        # If we have created a new salt, write it to config file or started from scratch
        self.write_config()



    def write_config(self):

        file_path = os.path.join(self.storage_path, "data.json")

        # Create a copy, so any change in encoding for writing the data doesn't affect the running program functionality
        copy_config=self.config.copy()

        with open(file_path, "w", encoding='utf-8') as file:
            
            # Make the salt file write friendly
            copy_config['salt'] = b64encode(self.config['salt']).decode()
            
            # Write using JSON format
            file.write(json.dumps(copy_config))


    def create_key(self):
        pass_phrase=self.session_master_password
        # Taken from the website itse
        # https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.config['salt'],
            iterations=10000
        )

        self.__key = base64.urlsafe_b64encode(kdf.derive(pass_phrase.encode()))

        return self.__key

        """Encrypts the data given
        """
    def encrypt_text(self, key, text):
        f = Fernet(key)

        return f.encrypt(text.encode()).decode()

        """Decrypts the data given
        """
    def decrypt_text(self, key, text):
        f = Fernet(key)

        return f.decrypt(text.encode())


def toggle_input(prompt_text=">", initially_hidden=True):
    hidden = [initially_hidden]  
    bindings = KeyBindings()

    @bindings.add("c-t")
    def _(event):
        "When ControlT has been pressed, toggle visibility."
        hidden[0] = not hidden[0]

    input_text = prompt(
        prompt_text, rprompt="Ctrl-T to toggle visibility", is_password=Condition(lambda: hidden[0]), key_bindings=bindings
    )
    return input_text


def get_path_prompt(prompt_text, **kwargs):
    
    validator = Validator.from_callable(
        os.path.isdir,
        error_message="Not a valid path to a directory",
        move_cursor_to_end=True,
    )

    return prompt(
                prompt_text,
                completer=PathCompleter(only_directories=True), 
                rprompt="Press Tab to get suggestions",
                validator=validator,
                validate_while_typing=True, **kwargs)

