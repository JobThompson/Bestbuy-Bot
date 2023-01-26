from pprint import pprint
import PySimpleGUI as sg
from Classes.Logging import handle_exit
from Classes.GUIButtons import landing_page_button
from Classes.ProductSelection import product_selection
from Classes.Pages.CredentialsManagerPage import credentials_manager
from Classes.Pages.CustomURLPage import custom_URL_page
from Classes.Pages.ProductCategoriesPage import ProductCategories

def handle_credentials_manager():
    credentials_manager()

def handle_get_GPU_from_list():
    ProductCategories()

def handle_custom_URL():
    custom_URL_page()

def LandingPage():
    layout = [[landing_page_button('Get GPU from List')], [landing_page_button('Custom URL')], [landing_page_button('Credentials Manager')]]
    layout.insert(0, [sg.Text('Select Function')])
    window = sg.Window("GPU Selection", layout, size=(400, 305), element_justification='c')
    while True:
        event, _ = window.read()
        match event:
            case sg.WIN_CLOSED: 
                handle_exit()
                
            case 'Credentials Manager':
                handle_credentials_manager()
                
            case 'Get GPU from List':
                handle_get_GPU_from_list()
                break
                
            case 'Custom URL':
                handle_custom_URL()
                break
                
            case _:
                window.close()
                # product = display_list(choice)
                exit()
                
    window.close()      
    return

