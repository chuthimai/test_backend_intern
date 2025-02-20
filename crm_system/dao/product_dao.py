from django.db import IntegrityError

from crm_system.models import Product


class ProductDAO:
    @staticmethod
    def create_product(name: str, price: float, description: str = None):
        try:
            product = Product(name=name, price=price, description=description)
            product.save()
            return product
        except IntegrityError:
            return None

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_product_by_id(product_id: int):
        return Product.objects.filter(id=product_id).first()

    @staticmethod
    def update_product(product_id: int, name: str = None, price: float = None, description: str = None):
        product = ProductDAO.get_product_by_id(product_id)
        if product:
            if name:
                product.name = name
            if price:
                product.price = price
            if description:
                product.description = description
            product.save()
            return product
        return None

    @staticmethod
    def delete_product(product_id: int):
        product = ProductDAO.get_product_by_id(product_id)
        if product:
            product.delete()
            return True
        return False
