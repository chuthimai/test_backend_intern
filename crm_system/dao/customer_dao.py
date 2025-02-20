from django.db import IntegrityError

from crm_system.models import Customer


class CustomerDAO:
    @staticmethod
    def create_customer(name: str, email: str, phone: str = None, address: str = None):
        try:
            customer = Customer(name=name, email=email, phone=phone, address=address)
            customer.save()
            return customer
        except IntegrityError:
            return None

    @staticmethod
    def get_all_customers():
        return Customer.objects.all()

    @staticmethod
    def get_customer_by_id(customer_id: int):
        return Customer.objects.filter(id=customer_id).first()

    @staticmethod
    def update_customer(customer_id: int, name: str = None, email: str = None, phone: str = None, address: str = None):
        customer = CustomerDAO.get_customer_by_id(customer_id)
        if customer:
            if name:
                customer.name = name
            if email:
                customer.email = email
            if phone:
                customer.phone = phone
            if address:
                customer.address = address
            customer.save()
            return customer
        return None

    @staticmethod
    def delete_customer(customer_id: int):
        customer = CustomerDAO.get_customer_by_id(customer_id)
        if customer:
            customer.delete()
            return True
        return False
