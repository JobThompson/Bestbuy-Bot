import helium as h
import PySimpleGUI as sg
import time
import json
import logging
import datetime
import traceback

"""CONSTANTS AND CONFIGS"""
PRODUCT_FILE = 'config/Info.json'
CREDENTIALS = 'config/default_credentials.json'
CURRENT = 'config/current.json'
LOG_FOLDER = 'Logs/'
with open(PRODUCT_FILE) as f:  # Pulls product info from JSON file and sets variables equal to specified arrays
    variables = json.load(f)
LISTS = variables['LISTS']
sg.theme('Dark Grey 5')
menu_button_size_1 = (10, 4)
submenu_button_size = (19, 4)
submenu_button_size2 = (35, 2)
color1 = 'white'
color2 = 'black'
color3 = 'white'
color4 = 'black'


"""BUTTON LAYOUTS"""


def gui_button(button_text):
    return sg.Button(button_text, size=menu_button_size_1, button_color=(color1, color2))


def submenu_button(button_text):
    return sg.Button(button_text, size=submenu_button_size, button_color=(color3, color4))


def submenu_button2(button_text):
    return sg.Button(button_text, size=submenu_button_size2, button_color=(color3, color4))


def back_button():
    return sg.Button('Back', button_color=('black', 'darkred'), font=("Helvetica", 15), size=(7, 1))


def submit_button():
    return sg.Submit(button_color=('black', 'green'), font=("Helvetica", 15), size=(7, 1))


"""LOGGING FUNCTIONS"""


def write_to_log(info):
    """Outputs info string to the log file that is set upon initial script execution."""
    # on exception, This needs to write the traceback information as well as the failure message.
    logging.info(str(datetime.datetime.now())+': '+info)  # Writes time and date as well as the info string to log file.
    return


def create_logfile():
    """Creates a new Log file with a date Identifier. If there is an existing log file with that identifier,
    the function adds an iterative number to the end of the file name until it gets to a file name that doesn't exist."""
    date = str(datetime.datetime.now().strftime("%m_%d_%Y"))
    # sets date to a variable
    logfile = ('Log_' + date + '.log')
    # creates a new file name using date variable set above as the identifier
    multiple = 1
    while True:  # compares the last log file to the created file name
        try:
            open(LOG_FOLDER + logfile, "x")
            # creates a new file using the new log file name
            break
        except Exception:  # if the file name is the same, it adds an iterating number to the end
            logfile = ('Log_' + date + '_' + str(multiple) + '.log')
            multiple += 1  # iterates the number at the end of the file
    logfile = (LOG_FOLDER + logfile)
    # sets logfile to the full filepath.
    logging.basicConfig(filename=logfile, level=logging.INFO)
    # sets the logging file as the newly created file.
    return logfile


"""CREDENTIALS MANAGEMENT"""


def credentials_manager():
    """This function sets default credentials to an external JSON file, so that the program can pull the info for later
    runs. It also allows the user to clear the existing credentials from the file, allowing them to set new ones."""
    email, password, cvv, head = read_current_creds()
    if email == "" or password == "":
        load_defaults()
    # loads default creds into current file
    email, password, cvv, head = read_current_creds()
    # gets credentials from current file
    column1 = [[sg.Text('EMAIL:')], [sg.Text('PASSWORD:')], [sg.Text('CVV:')], [sg.Text(' ')]]
    column2 = [[sg.InputText(email)], [sg.InputText(password)], [sg.InputText(cvv)],
               [sg.Checkbox('Run script without browser?')]]
    layout = [[sg.Text('Credentials Manager:')], [sg.Text('Current Credentials:')],
              [sg.Column(column1), sg.Column(column2)], [sg.Text(' ')],  [sg.Text(' ')],
              [sg.Button('Clear Defaults', size=(15, 2)),
              sg.Button('Set as Default', size=(15, 2))],
              [sg.Text(' ')], [back_button(), submit_button()]]
    window = sg.Window('Credentials Manager', layout, size=(400, 400), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit_clause()
        elif event == 'Back':
            window.close()
            break
        while True:
            if event == 'Clear Defaults':  # Removed credential information from default_credentials
                write_to_log('Defaults Cleared.')
                clear_defaults()
                sg.popup_ok('Default Credentials Cleared!')
                window.close()
                email, password, cvv, head = credentials_manager()
                return email, password, cvv, head
            elif event == 'Set as Default':  # Dumps credential information into default_credentials for later use.
                write_to_log('Default Credentials Set.')
                email, password, cvv, head = set_cred_variables(values)
                if email == '' and password == '' and cvv == '':
                    sg.popup_error('Please Provide Credentials to Set.')
                    email, password, cvv, head = credentials_manager()
                    break
                else:
                    with open(CREDENTIALS, "r") as creds:
                        data = json.load(creds)
                        data["Email"] = email
                        data["Password"] = password
                        data["CVV"] = cvv
                        data["head"] = head
                    with open(CREDENTIALS, "w") as creds:
                        json.dump(data, creds)
                    set_current_creds(email, password, cvv, head)
                    break
            elif event == 'Submit':  # Writes the credentials to the current file. doesn't write to defaults.
                write_to_log('Credentials Submitted.')
                email, password, cvv, head = set_cred_variables(values)
                if email == "" or password == "" or cvv == "":
                    sg.popup_error('No Credentials Submitted.')
                    write_to_log('Issue with submitted credentials.')
                else:
                    set_current_creds(email, password, cvv, head)
                break
        break
    window.close()
    return email, password, cvv, head


def set_cred_variables(values):
    """Sets variables from the values list. returns email, password, cvv, head"""
    email = values[0]
    password = values[1]
    cvv = values[2]
    head = values[3]
    return email, password, cvv, head


def load_defaults():
    """Reads credentials from the credentials file, and writes those to the current folder if they arnt blank."""
    with open(CREDENTIALS) as creds:
        defaults = json.load(creds)
        email = defaults["Email"]
        password = defaults["Password"]
        cvv = defaults["CVV"]
        head = defaults["head"]
    if email != "" and password != "":
        set_current_creds(email, password, cvv, head)
        return
    else:
        set_current_creds(email, password, cvv, head)
        return email, password, cvv, head


def set_current_creds(email, password, cvv, head):
    """This function sets variables as credentials into the current cookie."""
    with open(CURRENT, "r") as creds:
        data = json.load(creds)
        data["Email"] = email
        data["Password"] = password
        data["CVV"] = cvv
        data["head"] = head
    with open(CURRENT, "w") as creds:
        json.dump(data, creds)
    return


def read_current_creds():
    """This function retrieves credentials from the current cookie."""
    with open(CURRENT) as creds:
        defaults = json.load(creds)
        email = defaults["Email"]
        password = defaults["Password"]
        cvv = defaults["CVV"]
        head = defaults["head"]
    return email, password, cvv, head


def clear_current():
    """This function deletes all data in the current cookie."""
    with open(CURRENT, "r") as creds:
        data = json.load(creds)
        data["Email"] = ""
        data["Password"] = ""
        data["CVV"] = ""
        data["head"] = False
    with open(CURRENT, "w") as creds:
        json.dump(data, creds)
    return


def clear_defaults():
    """This function deletes all data in the current cookie."""
    with open(CREDENTIALS, "r") as creds:
        data = json.load(creds)
        data["Email"] = ""
        data["Password"] = ""
        data["CVV"] = ""
        data["head"] = False
    with open(CREDENTIALS, "w") as creds:
        json.dump(data, creds)
    clear_current()
    return


"""FUNCTIONS"""


def button_number(choice, display):
    """Creates the columns for the custom layout for the submenu pages, depending on how many entries there are per
    selection choice."""
    column_1 = [[sg.Text(str(choice) + "'s:")], [sg.Text('')]]
    i = 0
    while True:  # adds a button for each entry in the display array.
        try:
            column_1.append([submenu_button2(display[i])])
            i += 1  # moves to the next array
        except Exception:
            break
    column_2 = [[sg.Button('Back', button_color=('black', 'darkred'), font=("Helvetica", 15), size=(7, 4))]]
    return column_1, column_2


def exit_clause():
    """Exit Clause for closing the program."""
    clear_current()
    exit()


def select_another_option():
    """Pops up error message, invalid option."""
    sg.popup_error('Please select a different option!')
    return


def gui():
    """Brings up the main menu for the program, with options for different GPU selections. Once a product stack is
    selected, it calls for the submenu for the individual card. Once that choice is returned, the function returns
    to the previous function."""
    column1 = [[sg.Text('Select the GPU Category you want:')], [gui_button('RTX 3080'),
               gui_button('RTX 3070 TI')],
               [gui_button('RTX 3070'), gui_button('RTX 3060 TI')],
               [gui_button('RTX 3060'), gui_button('GTX 1660 TI')]]
    column2 = [[gui_button('Custom URL')], [gui_button('Credentials Manager')]]
    layout = [[sg.Column(column1), sg.VSeparator(), sg.Column(column2)]]
    window = sg.Window("GPU Selection", layout, size=(400, 305), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit_clause()
        elif event == 'Credentials Manager':
            window.close()
            credentials_manager()
            product = gui()
            break
        else:
            choice = event
            if choice == 'Custom URL':
                window.close()
                product = url_input()
                break
            else:
                window.close()
                product = display_list(choice)
                break
    return product


def display_list(choice):
    """Displays a list of the individual GPU's from the selected product stack."""
    selection_list = LISTS[choice]  # Sets the GPU list to a variable
    display = list(selection_list.keys())  # sets the GPU names to a list variable
    column_1, column_2 = button_number(choice, display)
    layout = [[sg.Column(column_1), sg.VSeparator(), sg.Column(column_2)]]
    window = sg.Window(str(choice), layout, size=(500, 500), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit_clause()
        elif event == 'Back':
            window.close()
            product = gui()
            break
        elif selection_list[event] == 0:  # checks for null value from placeholder button
            select_another_option()
        else:
            window.close()
            product = selection_list[event]  # sets variable to the URL associated with the user choice.
            break
    return product


def url_input():
    """Allows freeform input if the product the user wants is not listed as an option in the buttons.
    returns URL variable as string."""
    layout = [[sg.Text('Enter the URL for the product:')], [sg.InputText('')], [sg.Text(' ')], [sg.Text(' ')],
              [sg.Text(' ')], [sg.Text(' ')], [sg.Text(' ')], [sg.Text(' ')], [sg.Text(' ')], [sg.Text(' ')],
              [sg.Text(' ')], [sg.Text(' ')], [sg.Text(' ')], [back_button(), submit_button()]]
    window = sg.Window("URL Selection", layout, size=(400, 400), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit_clause()
        elif event == 'Back':
            window.close()
            url = gui()
            break
        elif event == 'Submit':
            write_to_log('Custom URL Submitted.')
            url = values[0]  # Sets input from field to url variable
            break
        #elif event == 'Clear Recent Searches':
    window.close()
    return url


def buy_product(product, email, password, cvv, head):
    """This function is the bot that opens a firefox browser, signs into the BestBuy site, then calls the product URL.
    If the product is in stock, it purchases the product. If the product is not in stock, it refreshes the page until
    it is."""
    h.start_firefox('https://www.bestbuy.com/identity/global/signin', headless=head)
    # Starts firefox instance, headless = True wont come up as a intractable window
    h.write(email, into='Email Address')
    # Enters Email address into email input box from Info file
    h.write(password, into='Password')
    # Enters password into password input box from Info file
    h.click(h.S('.btn-secondary'))
    # Clicks log in
    h.go_to(product)
    # Directs the browser to pull up the specified product page.
    attempts = 0
    # Sets retrieval attempts to 0, not really necessary
    h.Config.implicit_wait_secs = 2
    # Sets the amount of time the script will wait for an element to load to 2 seconds
    while True:
        while True:
            h.Config.implicit_wait_secs = 2
            try:
                h.click(h.Button('Add To Cart'))
                # Attempts to click add to cart button
                write_to_log('Button: Add to Cart.')
                break
                # Breaks out of While Loop
            except:
                attempts += 1
                # Add 1 to the attempt number
                print('failed:', attempts)
                # Prints the failed attempt number
                write_to_log('Button: Out Of Stock. Attempt Number ' + str(attempts) + ' Failed.')
                h.refresh()
                # Refreshes the product webpage
        h.Config.implicit_wait_secs = 7
        if h.Text('not in Cart.').exists():
            # Checks for bestbuy anti bot message
            write_to_log('Item was not added to cart')
            h.refresh()
            pass
        elif h.Text('Error').exists():
            # Checks for error messages on webpage
            write_to_log('Webpage returned an error.')
            h.click(h.Button('Add To Cart'))
            pass
        elif h.Text('Added to Cart').exists():
            # Verifies that the product was added to cart
            write_to_log('Item successfully added to cart.')
            break
        else:
            pass
    h.Config.implicit_wait_secs = 100
    # Sets the amount of time the script will wait for an element to load to 5 seconds
    h.go_to('https://www.bestbuy.com/cart')
    # Sends browser to card
    h.click(h.Button('Checkout'))
    # Clicks on checkout button
    h.go_to('https://www.bestbuy.com/checkout/r/fast-track')
    # Sends browser to checkout page
    try:
        h.write(cvv, into=h.S('#credit-card-cvv'))
        # Attempts to find CVV input, if doesnt show up within 5 seconds, passes on to next command
    except Exception:
        pass
    h.click(h.Button('Place Your Order'))
    # Clicks the place order button
    time.sleep(30)
    h.kill_browser()
    # Closes the browser instance
    return attempts


def item_purchased(attempts):
    """This function calls a success window to let the user know that the product was successfully purchased."""
    write_to_log('Item was successfully purchased.')
    layout = [[sg.Text("Congratulations!")], [sg.Text("You're Item has been purchased!")],
              [sg.Text('It took '+str(attempts)+' Attempts!')], [sg.Ok()]]
    window = sg.Window('Congratulations!', layout, size=(400, 400), element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Ok':
            break
    exit()


def main():
    """Main function that initiates the program. Calls GUI function for product choice, then checks for default login
     credentials. If no credentials exist, it will prompt for them. If they do exist, it will launch the buy_product
     function, and pass the default credentials on to the function. Once the buy_product returns an attempts variable,
     it displays a success window and ends the program."""
    try:
        load_defaults()  # loads credentials into current cookie
        product = gui()  # opens GUI interface and gets product choice from user
        email, password, cvv, head = read_current_creds()  # gets credentials from current cookie
        if email == "" or password == "":  # if the creds are blank, prompts user for creds
            while True:
                email, password, cvv, head = credentials_manager()
                if email == "" or password == "" or cvv == "":
                    write_to_log('Attempt to purchase without credentials.')
                    sg.popup_error('Credentials Are Required')
                else:
                    print('Passed')
                    break
        else:
            pass
        clear_current()  # clears the current cookie of all credentials
        attempts = buy_product(product, email, password, cvv, head)  # opens the bot, returns attempts
        item_purchased(attempts)  # opens success screen
    except Exception as e:
        write_to_log(str(e))
        logging.error(traceback.format_exc())


if __name__ == '__main__':
    create_logfile()
    write_to_log('Program Started.')
    main()
