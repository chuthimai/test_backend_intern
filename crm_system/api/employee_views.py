from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crm_system.dao.employee_dao import EmployeeDAO
from crm_system.serializers import EmployeeSerializer


class EmployeeAPIView(APIView):
    def get(self, request, employee_id=None):
        if employee_id:
            employee = EmployeeDAO.get_employee_by_id(employee_id)
            serializer = EmployeeSerializer(employee)
        else:
            employees = EmployeeDAO.get_all_employees()
            serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        employee = EmployeeDAO.create_employee(**request.data)
        if employee:
            return Response(
                EmployeeSerializer(employee).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": "Add failed employee"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, employee_id):
        employee = EmployeeDAO.update_employee(employee_id, **request.data)
        if employee:
            return Response(
                EmployeeSerializer(employee).data,
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Update failed employee"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, employee_id):
        if EmployeeDAO.delete_employee(employee_id):
            return Response(
                {"message": "Employee deleted successfully"},
                status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Delete failed employee"},
            status=status.HTTP_400_BAD_REQUEST)






