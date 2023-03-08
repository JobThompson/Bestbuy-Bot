from Classes.Credentials import Credentials

ACTIONS = [
    "BuyScript",
    "MonitorScript",
]


class ProgramState:
    def __init__(self) -> None:
        self.CustomUrl = None
        self.Action = None
        self.SelectedProduct = None
        self.HasCredentials = False
        self.Credentials = Credentials()
        self.RefreshAttempts = 0
        
    def set_custom_URL(self, custom_URL):
        self.CustomUrl = custom_URL
    
    def set_action(self, action):
        try:
            self.Action = ACTIONS[ACTIONS.index(action)]
            return True
        except Exception as e:
            print(e)
            return False
        
    def set_selected_product(self, product):
        self.SelectedProduct = product
    
    def set_has_credentials(self, value):
        self.HasCredentials = bool(value)
        
    def get_product_url(self):
        if self.CustomUrl:
            return self.CustomUrl
        else:
            return self.SelectedProduct.url
    
    
programState = ProgramState()