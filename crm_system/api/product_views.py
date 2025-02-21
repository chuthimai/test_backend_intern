from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crm_system.dao.product_dao import ProductDAO
from crm_system.serializers import ProductSerializer


class ProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Lấy danh sách sản phẩm hoặc chi tiết sản phẩm",
        description="Trả về danh sách tất cả sản phẩm hoặc thông tin một sản phẩm nếu cung cấp `product_id`.",
        parameters=[
            OpenApiParameter(
                name="product_id",
                description="ID của sản phẩm (tùy chọn, nếu muốn lấy 1 sản phẩm cụ thể)",
                required=False,
                type=int
            )
        ],
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request, product_id=None):
        if product_id:
            product = ProductDAO.get_product_by_id(product_id)
            serializer = ProductSerializer(product)
        else:
            products = ProductDAO.get_all_products()
            serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Thêm mới sản phẩm",
        description="Tạo một sản phẩm mới với thông tin cần thiết.",
        request=ProductSerializer,
        responses={201: ProductSerializer}
    )
    def post(self, request):
        product = ProductDAO.create_product(**request.data)
        if product:
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response({"error": "Add failed product"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Cập nhật thông tin sản phẩm",
        description="Cập nhật thông tin của một sản phẩm theo ID.",
        parameters=[
            OpenApiParameter(
                name="product_id",
                description="ID của sản phẩm cần cập nhật",
                required=True,
                type=int
            )
        ],
        request=ProductSerializer,
        responses={200: ProductSerializer}
    )
    def put(self, request, product_id):
        product = ProductDAO.update_product(product_id, **request.data)
        if product:
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response({"error": "Update failed product"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Xóa sản phẩm",
        description="Xóa một sản phẩm theo ID.",
        parameters=[
            OpenApiParameter(
                name="product_id",
                description="ID của sản phẩm cần xóa",
                required=True,
                type=int
            )
        ],
        responses={204: None}
    )
    def delete(self, request, product_id):
        if ProductDAO.delete_product(product_id):
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Delete failed product"}, status=status.HTTP_400_BAD_REQUEST)