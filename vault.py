import os

import prompt_toolkit
from prompt_toolkit import completion
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.formatted_text import HTML

from utils import *
from crypto import *




class vault:


    def __init__(self):
        # self.master_password = toggle_input("Master Password> ")
        # self.storage_path = get_path_prompt("Select a Storage directory: ", 
                                            # placeholder=HTML('<style color="#888888">Place the old data file in the same directory(named pass.json), if copied from other system</style>'))
        self.storage_path = "./"
        self.master_password = "MYpass"
        self.read_vault()
    

    def read_vault(self):

        file_path = os.path.join(self.storage_path, "vault.json")

        try:
            with open(file_path, "r") as f:
                data = f.read()
                data_dict = json.loads(data)
        except:
            data_dict = {}


        decrypted_data = crypto(self.master_password, **data_dict).decrypt().to_dict()
        """decrypted_data of type dict

            {
                'salt':the_salt,
                'data':decrypted_data
            }
        """

        
        self.vault_dict = json.loads(decrypted_data['data'])
        print(self.vault_dict)

        # Passwords are still encrypted, they will be decrypted on fly when we ask for the password only
        # Same Master Password will be used for 
        


v = vault()