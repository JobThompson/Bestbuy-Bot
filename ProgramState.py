from Classes.Credentials import Credentials

ACTIONS = []


class ProgramState:
    def __init__(self) -> None:
        self.CustomUrl = None
        self.Action = None
        self.SelectedProduct = None
        self.HasCredentials = False
        self.Credentials = Credentials()
        
    def set_custom_URL(self, custom_URL):
        self.CustomUrl = custom_URL
    
    def set_action(self, action):
        try:
            self.Action = ACTIONS[f'{action}']
            return True
        except Exception as e:
            print(e)
            return False
        
    def set_selected_product(self, product):
        self.SelectedProduct = product
    
    def set_has_credentials(self, value):
        self.HasCredentials = bool(value)
    
    
programState = ProgramState()