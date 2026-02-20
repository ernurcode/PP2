class Product:
    def __init__(self, name, price, num=0):
        self.name = name
        self.price = price
        self.num = num

    def get_info(self):
        print(f"Name: {self.name}, Price: {self.price}$")

    def get_total_products(self):
        
        print(f"Total Products: {self.num}")


class Digital_Product(Product):
    def __init__(self, name, price, file_size, num=0):
        super().__init__(name, price, num)
        self.file_size = file_size

    def get_info(self):
        print(f"Name: {self.name}, Price: {self.price}$, File Size: {self.file_size} GB")
    

class Physical_Product(Product):
    def __init__(self, name, price, weight, num=0):
        super().__init__(name, price, num)
        self.weight = weight

    def get_info(self):
        print(f"Name: {self.name}, Price: {self.price}$, Weight: {self.weight} KG")



digital = Digital_Product("Document", 100, 4, 2)
digital.get_info()
digital.get_total_products()


physical = Physical_Product("Apple", 1, 30, 2)
physical.get_info()
physical.get_total_products()