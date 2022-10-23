from pprint import pprint
from Classes.Credentials import credentials
from Classes.Pages.LandingPage import LandingPage
from Classes.Pages.ProductCategoriesPage import ProductCategories
from Classes.ProductSelection import product_selection

def main():
    # pprint([[products.url for products in product.products] for product in product_selection.product_list])
    # pprint(vars(credentials).items())
    # ProductCategories()
    LandingPage()
    

if __name__ == '__main__':
    main()