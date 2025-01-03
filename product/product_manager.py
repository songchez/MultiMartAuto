import csv
from product.validator import ProductValidator

class ProductManager:
    def __init__(self, storage_file='../data/products.csv'):
        """
        Initialize the ProductManager.
        :param storage_file: Path to the CSV file where product data will be stored.
        """
        self.products = []
        self.storage_file = storage_file
        self.validator = ProductValidator()

    def input_product_info(self, platform):
        """
        Input product details and validate them before adding to the product list.
        :param platform: Platform name for validation (e.g., 'naver', 'coupang', 'cafe24').
        """
        product = {
            "name": input("Enter product name: "),
            "price": float(input("Enter product price: ")),
            "category": input("Enter product category: "),
            "stock": int(input("Enter stock quantity: ")),
            "options": input("Enter options (comma-separated): ").split(','),
            "image_path": input("Enter image path: ")
        }
        if self.validator.validate(product, platform):
            self.products.append(product)
            print(f"Product added successfully for {platform}.")
        else:
            print(f"Product validation failed for {platform}. Please check the input values.")

    def save_to_csv(self):
        """
        Save the product list to a CSV file.
        """
        try:
            with open(self.storage_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.products[0].keys())
                writer.writeheader()
                writer.writerows(self.products)
            print(f"Products saved to {self.storage_file} successfully.")
        except Exception as e:
            print(f"Error saving products to file: {e}")

    def display_products(self):
        """
        Display all products currently in the list.
        """
        for idx, product in enumerate(self.products, start=1):
            print(f"\nProduct {idx}:")
            for key, value in product.items():
                print(f"  {key}: {value}")
