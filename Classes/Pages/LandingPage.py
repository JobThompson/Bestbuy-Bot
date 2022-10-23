from pprint import pprint
import PySimpleGUI as sg
from Classes.GUIButtons import landing_page_button
from Classes.ProductSelection import product_selection

def LandingPage():
    layout = [[landing_page_button('Get GPU from List')], [landing_page_button('Custom URL')], [landing_page_button('Credentials Manager')]]
    layout.insert(0, [sg.Text('Select Function')])
    window = sg.Window("GPU Selection", layout, size=(400, 305), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit(0)
        elif event == 'Credentials Manager':
            window.close()
            # credentials_manager()
            exit()
            product = gui()
            break
        else:
            choice = event
            if choice == 'Custom URL':
                window.close()
                exit()
                # product = url_input()
                break
            else:
                window.close()
                # product = display_list(choice)
                exit()
                break
    return product