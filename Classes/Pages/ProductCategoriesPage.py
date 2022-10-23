from pprint import pprint
import PySimpleGUI as sg
from Classes.GUIButtons import gui_button
from Classes.ProductSelection import product_selection

def ProductCategories():
    """Brings up the main menu for the program, with options for different GPU selections. Once a product stack is
    selected, it calls for the submenu for the individual card. Once that choice is returned, the function returns
    to the previous function."""
    array_of_buttons = get_category_buttons()
    array_of_buttons.insert(0, [sg.Text('Select the GPU Category you want:')])
    
    layout = array_of_buttons
    # column2 = [[gui_button('Custom URL')], [gui_button('Credentials Manager')]]
    # layout = [[sg.Column(column1), sg.VSeparator(), sg.Column(column2)]]
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
    
