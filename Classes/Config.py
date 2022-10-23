import json

class ConfigObject():
    def __init__(self, config_file) -> None:
        self.config_file = config_file
        self.credentials_file = ""
        self.product_list_file = ""
        self.log_directory = ""
        self.script_timeout = 0
        self.isHeadlessFlag = ""
        self.get_config_values()
        
    def get_config_values(self):
        with open(self.config_file) as f:
            config_file = json.load(f)
        self.credentials_file = config_file["CredentialsFile"]
        self.product_list_file = config_file["ProductListFile"]
        self.log_directory = config_file["LogDirectory"]
        self.script_timeout = int(config_file["ScriptTimeoutInSeconds"]) * 1000 # convert to milliseconds
        self.isHeadlessFlag = config_file["IsHeadlessFlag"]
        return
    
    def set_credentials_file(self, credentials_file):
        self.credentials_file = credentials_file
        return
    
    def set_product_list_file(self, product_list_file):
        self.product_list_file = product_list_file
        return
    
    def set_log_directory(self, log_directory):
        self.log_directory = log_directory
        return
    
    def set_headless_flag(self, isHeadlessFlag):
        self.isHeadlessFlag = isHeadlessFlag
        return


instanceConfig = ConfigObject('./config_files/config.json')