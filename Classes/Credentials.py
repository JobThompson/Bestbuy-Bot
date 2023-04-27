from pprint import pprint
from cryptography.fernet import Fernet
from Classes.Config import instanceConfig
import json

class Credentials ():
    def __init__(self) -> None:
        self.email = ''
        self.password = ''
        self.card_number = ''
        self.card_expr_date = ''
        self.card_cvv = ''
        self.encryption_key = ''
        self.get_creds_from_file()
        # self.fernet_instance = self.get_fernet_instance()
        
    def get_creds_from_file(self):
        creds_file = self.get_persistent_creds_file()
        self.email = creds_file["Email"]
        self.password = creds_file["Password"]
        self.card_number = creds_file["CardNumber"]
        self.card_expr_date = creds_file["CardExprDate"]
        self.card_cvv = creds_file["CardCVV"]
        return
    
    def write_all_values_to_persistent_storage(self):
        self.write_to_persistent_creds_file('Email', self.email)
        self.write_to_persistent_creds_file('Password', self.password)
        self.write_to_persistent_creds_file('CardNumber', self.card_number)
        self.write_to_persistent_creds_file('CardExprDate', self.card_expr_date)
        self.write_to_persistent_creds_file('CardCVV', self.card_cvv)
        return
    
    def wipe_all_values_from_persistent_storage(self):
        self.write_to_persistent_creds_file('Email', '')
        self.write_to_persistent_creds_file('Password', '')
        self.write_to_persistent_creds_file('CardNumber', '')
        self.write_to_persistent_creds_file('CardExprDate', '')
        self.write_to_persistent_creds_file('CardCVV', '')
        return
    
    def wipe_all_values_from_memory(self):
        self.email = ''
        self.password = ''
        self.card_number = ''
        self.card_expr_date = ''
        self.card_cvv = ''
        
    def set_email(self, email):
        self.email = email
        return
    
    def set_password(self, password):
        self.password = password
        return
    
    def set_card_number(self, card_number):
        self.card_number = card_number
        return
    
    def set_card_expiration_date(self, expiration_date):
        self.card_expr_date = expiration_date
        return
    
    def set_card_cvv(self, cvv):
        self.card_cvv = cvv
        return
    
    def get_persistent_creds_file(self):
        try:
            with open(instanceConfig.credentials_file) as f:
                creds_file = json.load(f)
            return creds_file
        except Exception as e:
            print(e)
            raise Exception("Error reading credentials file. Please check the file path and try again.")
    
    def write_to_persistent_creds_file(self, key, value):
        creds_file = self.get_persistent_creds_file()
        creds_file[key] = value
        
        with open(instanceConfig.credentials_file, "w") as f:
            f.write(json.dumps(creds_file))
        return
    
    def get_fernet_instance(self): # https://pavan581.medium.com/save-passwords-to-json-file-with-encryption-using-python-9fb9430f22c3
        fernet = Fernet(self.encryption_key)
        return fernet
    
    def write_encrypted_value_to_persistent_storage(self, key, value):
        encrypted_value = self.fernet_instance.encrypt(value.encode())
        self.write_to_persistent_creds_file(key, encrypted_value)        
        return
    
    def read_encrypted_value_to_persistent_storage(self, key):
        creds_file = self.get_persistent_creds_file()
        encrypted_value = creds_file[key]
        value = self.fernet_instance.decrypt(encrypted_value).decode()
        return value
