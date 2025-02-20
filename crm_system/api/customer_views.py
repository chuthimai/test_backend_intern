from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crm_system.dao.customer_dao import CustomerDAO
from crm_system.serializers import CustomerSerializer


class CustomerAPIView(APIView):
    def get(self, request, customer_id=None):
        if customer_id:
            customer = CustomerDAO.get_customer_by_id(customer_id)
            serializer = CustomerSerializer(customer)
        else:
            customers = CustomerDAO.get_all_customers()
            serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        address = request.data.get("address")

        customer = None
        if name and email:
            customer = CustomerDAO.create_customer(
                name=name,
                email=email,
                phone=phone,
                address=address
            )

        if customer:
            return Response(
                CustomerSerializer(customer).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": "Add failed customer"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, customer_id):
        name = request.data.get("name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        address = request.data.get("address")

        customer = CustomerDAO.update_customer(
            customer_id,
            name=name,
            email=email,
            phone=phone,
            address=address
        )

        if customer:
            return Response(
                CustomerSerializer(customer).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": "Update failed customer"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, customer_id):
        is_delete = CustomerDAO.delete_customer(customer_id)
        if is_delete:
            return Response(
                {"message": "Customer deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"error": "Delete failed customer"},
            status=status.HTTP_400_BAD_REQUEST
        )
