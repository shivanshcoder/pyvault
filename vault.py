import os

import prompt_toolkit
from prompt_toolkit import completion
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.formatted_text import HTML

from utils import *

class vault:

    def set_storage_path(self):
        self.__storage_path = get_path_prompt("Select a Storage directory: ", 
                                            placeholder=HTML('<style color="#888888">Place the old data file in the same directory(named pass.json), if copied from other system</style>'))



    def set_master_password(self):
        self

    def __init__(self):
        self.set_storage_path()
        self.__master_password = toggle_input("Master Password> ")

        self.config = configuration(self.__storage_path, self.__master_password)
        self.config.read_config()

        self.config.create_key()
        aa = self.config.encrypt_text("")
        print(aa)

        print(self.config.decrypt_text(aa).decode())

v = vault()