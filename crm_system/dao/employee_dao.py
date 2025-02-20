from django.db import IntegrityError

from crm_system.models import Employee


class EmployeeDAO:
    @staticmethod
    def create_employee(name: str, phone: str, position: str, address: str = None):
        try:
            employee = Employee(name=name, phone=phone, position=position, address=address)
            employee.save()
            return employee
        except IntegrityError:
            return None

    @staticmethod
    def get_all_employees():
        return Employee.objects.all()

    @staticmethod
    def get_employee_by_id(employee_id: int):
        return Employee.objects.filter(id=employee_id).first()

    @staticmethod
    def update_employee(
            employee_id: int,
            name: str = None,
            phone: str = None,
            position: str = None,
            address: str = None
    ):
        employee = EmployeeDAO.get_employee_by_id(employee_id)
        if employee:
            if name:
                employee.name = name
            if phone:
                employee.phone = phone
            if position:
                employee.position = position
            if address:
                employee.address = address
            employee.save()
            return employee
        return None

    @staticmethod
    def delete_employee(employee_id: int):
        employee = EmployeeDAO.get_employee_by_id(employee_id)
        if employee:
            employee.delete()
            return True
        return False
