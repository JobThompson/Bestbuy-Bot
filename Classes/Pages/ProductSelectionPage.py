from pprint import pprint
import PySimpleGUI as sg
from Classes.ProductSelection import product_selection
from Classes.GUIButtons import submenu_button2
from ProgramState import programState

def create_button_rows(choice, product_names):
    """Creates the columns for the custom layout for the submenu pages, depending on how many entries there are per
    selection choice."""
    column_1 = [[sg.Text(str(choice) + "'s:")], [sg.Text('')]]
    
    for product in product_names:
        column_1.append([submenu_button2(product)])
    
    column_2 = [[sg.Button('Back', button_color=('black', 'darkred'), font=("Helvetica", 15), size=(7, 4))]]
    return column_1, column_2

def handle_null_selection():
    sg.popup_error('Invalid Selection', 'Please select a valid product.')

def ProductSelectionPage(choice):
    """Displays a list of the individual GPU's from the selected product stack."""
    selection_list = None
    
    for productList in product_selection.product_list:
        if productList.name == choice:
            selection_list = productList.products
    
    product_names = [product.name for product in selection_list]
    
    column_1, column_2 = create_button_rows(choice, product_names)
    layout = [[sg.Column(column_1), sg.VSeparator(), sg.Column(column_2)]]
    window = sg.Window(str(choice), layout, size=(500, 500), element_justification='c')
    while True:
        event, _ = window.read()
        match event:
            case sg.WIN_CLOSED:
                exit(0)
                
            case 'Back':
                break
            
            case _:
                if selection_list[event] == 0:
                    handle_null_selection()
                else:
                    programState.set_selected_product(selection_list[event])
                    break
                
    window.close()
    return
