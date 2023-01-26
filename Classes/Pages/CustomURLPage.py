import PySimpleGUI as sg
from Classes.Logging import handle_exit
from Classes.GUIButtons import gui_button, back_button, submit_button
from Classes.ProductSelection import product_selection

def handle_submit(submitted_url):
    pass

def custom_URL_page():
    layout = [[sg.Text('Enter the URL for the product:')], [back_button(), submit_button()]]
    window = sg.Window("URL Selection", layout, size=(400, 400), element_justification='c')

    while True:
        event, values = window.read()
        
        match event:
            case sg.WIN_CLOSED:
                handle_exit()
            
            case 'Back':
                break
            
            case 'Submit':
                handle_submit(values[0])
                break
            
            case _:
                break
            
    window.close()
    return