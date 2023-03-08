import PySimpleGUI as sg
from Classes.Logging import handle_exit
from Classes.GUIButtons import gui_button, back_button, submit_button
from Classes.ProductSelection import product_selection
from ProgramState import programState

def handle_submit(submitted_url):
    programState.CustomUrl = submitted_url
    programState.set_action('BuyScript')

def custom_URL_page():
    
    layout = [[
                [sg.Text('Enter the URL for the product:', justification='left')], [sg.InputText('', key='url_input')], 
                sg.HSeparator(),
                [back_button(), submit_button()],
            ]]
    window = sg.Window("URL Selection", layout, size=(400, 400), element_justification='c')

    while True:
        event, values = window.read()
        
        match event:
            case sg.WIN_CLOSED:
                handle_exit()
            
            case 'Back':
                break
            
            case 'Submit':
                handle_submit(values['url_input'])
                break
            
            case _:
                break
            
    window.close()
    return