class ProductValidator:
    def __init__(self):
        """
        Initialize platform-specific rules.
        """
        self.platform_rules = {
            "naver": {"name_min_length": 3, "max_price": 1000000},
            "coupang": {"name_min_length": 3, "max_price": 5000000},
            "cafe24": {"name_min_length": 2, "max_price": 10000000}
        }

    def validate(self, product, platform):
        """
        Validate the product data against platform-specific rules.
        :param product: Dictionary containing product details.
        :param platform: Platform name for validation (e.g., 'naver', 'coupang', 'cafe24').
        :return: True if valid, False otherwise.
        """
        rules = self.platform_rules.get(platform.lower())
        if not rules:
            print(f"No validation rules defined for platform: {platform}")
            return False

        if not product["name"] or len(product["name"]) < rules["name_min_length"]:
            print(f"Product name must be at least {rules['name_min_length']} characters long for {platform}.")
            return False
        if product["price"] <= 0 or product["price"] > rules["max_price"]:
            print(f"Price must be between 0 and {rules['max_price']} for {platform}.")
            return False
        if product["stock"] < 0:
            print("Stock quantity cannot be negative.")
            return False
        if not product["image_path"]:
            print("Image path must not be empty.")
            return False
        return True
