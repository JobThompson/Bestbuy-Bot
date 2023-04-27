import json
from Classes.Config import instanceConfig

class ProductSelection():
    def __init__(self, file) -> None:
        self.product_list_file = file
        self.product_list = []
        self.import_product_list()

    def import_product_list(self):
        with open(self.product_list_file) as f:
            products = json.load(f)
        for product_cat in products:
            category = self.add_product_category(product_cat)
            for product in products[product_cat]:
                category.add_product(Product(product, products[product_cat][product]))
        
    def add_product_category(self, category_name):
        for category in self.product_list:
            if (category_name == category.name):
                return category
        self.product_list.append(ProductCategory(category_name))
        return self.product_list[-1]
        

class ProductCategory():
    def __init__(self, name) -> None:
        self.name = name
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        return


class Product():
    def __init__(self, name, url) -> None:
        self.name = name
        self.url = url
        
product_selection = ProductSelection(instanceConfig.product_list_file)