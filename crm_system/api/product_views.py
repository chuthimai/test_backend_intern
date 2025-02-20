from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crm_system.dao.product_dao import ProductDAO
from crm_system.serializers import ProductSerializer


class ProductAPIView(APIView):
    def get(self, request, product_id=None):
        if product_id:
            product = ProductDAO.get_product_by_id(product_id)
            serializer = ProductSerializer(product)
        else:
            products = ProductDAO.get_all_products()
            serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        product = ProductDAO.create_product(**request.data)
        if product:
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response({"error": "Add failed product"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        product = ProductDAO.update_product(product_id, **request.data)
        if product:
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response({"error": "Update failed product"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        if ProductDAO.delete_product(product_id):
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Delete failed product"}, status=status.HTTP_400_BAD_REQUEST)