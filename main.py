

from Classes.Config import ConfigObject
from Classes.ProductSelection import ProductSelection
from pprint import pprint
from Classes.Config import instanceConfig
from Classes.Credentials import credentials

def main():
    product_selection = ProductSelection(instanceConfig.product_list_file)
    pprint(vars(credentials).items())
    

if __name__ == '__main__':
    main()