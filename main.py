from pprint import pprint
from Classes.Logging import handle_exit, create_logfile
from Classes.Pages.LandingPage import LandingPage
from Classes.Pages.ProductCategoriesPage import ProductCategories
from Classes.ProductSelection import product_selection
from ProgramState import programState

def check_for_credentials():
    if(programState.Credentials.email != '' and programState.Credentials.password != '' and programState.Credentials.card_cvv != ''):
        programState.set_has_credentials(True)
    else:
        programState.set_has_credentials(False)

def main():
    create_logfile()
    check_for_credentials()
    LandingPage()
    # ExecuteAction()
    handle_exit()
    
if __name__ == '__main__':
    main()