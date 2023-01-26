from pprint import pprint
import PySimpleGUI as sg
from Classes.GUIButtons import gui_button
from Classes.ProductSelection import product_selection
from Classes.Logging import write_to_log
from Classes.Pages.ProductSelectionPage import ProductSelectionPage

def ProductCategories():
    """Brings up the main menu for the program, with options for different GPU selections. Once a product stack is
    selected, it calls for the submenu for the individual card. Once that choice is returned, the function returns
    to the previous function."""
    array_of_buttons = get_category_buttons()
    array_of_buttons.insert(0, [sg.Text('Select the GPU Category you want:')])
    
    back_button_column = [[sg.Button('Back', button_color=('black', 'darkred'), font=("Helvetica", 15), size=(7, 4))]]
    
    layout = [[sg.Column(array_of_buttons), sg.VSeparator(), sg.Column(back_button_column)]]
    window = sg.Window("GPU Selection", layout, size=(400, 305), element_justification='c')
    while True:
        event, _ = window.read()
        match event:
            case sg.WIN_CLOSED:
                exit(0)
                
            case 'Back':
                break
            
            case _:
                try:
                    ProductSelectionPage(event)
                    break
                except Exception as e:
                    write_to_log('ERROR', e)
                    break
    window.close()
    return


def get_category_buttons():
    overall_list = []
    array = []
    for product in product_selection.product_list:
        if len(array) == 2:
            overall_list.append(array)
            array = []
        array.append(gui_button(product.name))
    overall_list.append(array)
    
    if len(product_selection.product_list) % 2 != 0:
        array = []
        array.append(gui_button(product_selection.product_list[-1].name))
        overall_list.append(array)
    
    return overall_list
    
