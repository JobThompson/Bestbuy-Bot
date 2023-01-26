import PySimpleGUI as sg
from Classes.GUIButtons import back_button, submit_button
from ProgramState import programState
from Classes.Logging import write_to_log

def handle_submit(values):
    programState.Credentials.set_email(values[0])
    programState.Credentials.set_password(values[1])
    programState.Credentials.set_card_cvv(values[2])
    programState.Credentials.set_card_number(values[3])
    programState.Credentials.set_card_expiration_date(values[4])    

def handle_clear_defaults():
    write_to_log('INFO', 'Defaults Cleared.')
    programState.Credentials.wipe_all_values_from_persistent_storage()
    sg.popup_ok('Default Credentials Cleared!')

def handle_set_as_default(values):
    programState.Credentials.set_email(values[0])
    programState.Credentials.set_password(values[1])
    programState.Credentials.set_card_cvv(values[2])
    programState.Credentials.set_card_number(values[3])
    programState.Credentials.set_card_expiration_date(values[4])
    programState.Credentials.write_all_values_to_persistent_storage()


def credentials_manager():
    """This function sets default credentials to an external JSON file, so that the program can pull the info for later
    runs. It also allows the user to clear the existing credentials from the file, allowing them to set new ones."""
    localCredentials = type('obj', (object,), {
        'email': programState.Credentials.email,
        'password': programState.Credentials.password,
        'cvv': programState.Credentials.card_cvv,
        'card_number': programState.Credentials.card_number,
        'card_expr_date': programState.Credentials.card_expr_date,
    })
        
    column1 = [[sg.Text('EMAIL:')], [sg.Text('PASSWORD:')], [sg.Text('CARD NUMBER:')], [sg.Text('EXPIRATION DATE:')], [sg.Text('CVV:')], [sg.Text(' ')]]
    column2 = [[sg.InputText(localCredentials.email)], [sg.InputText(localCredentials.password)], [sg.InputText(localCredentials.card_number)], [sg.InputText(localCredentials.card_expr_date)], [sg.InputText(localCredentials.cvv)],
               [sg.Checkbox('Run script without browser?')]]
    layout = [[sg.Text('Credentials Manager:')], [sg.Text('Current Credentials:')],
              [sg.Column(column1), sg.Column(column2)], [sg.Text(' ')],  [sg.Text(' ')],
              [sg.Button('Clear Defaults', size=(15, 2)),
              sg.Button('Set as Default', size=(15, 2))],
              [sg.Text(' ')], [back_button(), submit_button()]]
    window = sg.Window('Credentials Manager', layout, size=(400, 400), element_justification='c')
    
    while True:
        event, values = window.read()
        match event:
            case sg.WIN_CLOSED:
                exit(0)
            
            case 'Back':
                break
                
            case 'Submit':
                if all(x=='' for x in values):
                    sg.popup_error('No Credentials Submitted.')
                    write_to_log('ERROR', 'Issue with submitted credentials.')
                else: 
                    handle_submit(values)
                    break
                
            case 'Clear Defaults':
                handle_clear_defaults()
                break
                
            case 'Set as Default':
                if all(x=='' for x in values):
                    sg.popup_error('Please Provide Credentials to Set.')
                else:
                    handle_set_as_default(values)
                    break
            
            case _:
                break

    window.close()
    return