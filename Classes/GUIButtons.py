import PySimpleGUI as sg
from Classes.ColorConfig import colorConfig

landing_page_button_size = (20, 2)
menu_button_size_1 = (10, 4)
submenu_button_size = (19, 4)
submenu_button_size2 = (35, 2)

def landing_page_button(button_text):
    return sg.Button(button_text, size=landing_page_button_size, button_color=(colorConfig.color1, colorConfig.color2))

def gui_button(button_text):
    return sg.Button(button_text, size=menu_button_size_1, button_color=(colorConfig.color1, colorConfig.color2))


def submenu_button(button_text):
    return sg.Button(button_text, size=submenu_button_size, button_color=(colorConfig.color3, colorConfig.color4))


def submenu_button2(button_text):
    return sg.Button(button_text, size=submenu_button_size2, button_color=(colorConfig.color3, colorConfig.color4))


def back_button():
    return sg.Button('Back', button_color=('black', 'darkred'), font=("Helvetica", 15), size=(7, 1))


def submit_button():
    return sg.Submit(button_color=('black', 'green'), font=("Helvetica", 15), size=(7, 1))