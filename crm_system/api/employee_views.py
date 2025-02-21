from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crm_system.dao.employee_dao import EmployeeDAO
from crm_system.serializers import EmployeeSerializer


class EmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Lấy danh sách nhân viên hoặc chi tiết nhân viên",
        description="Trả về danh sách tất cả nhân viên hoặc thông tin một nhân viên nếu cung cấp `employee_id`.",
        parameters=[
            OpenApiParameter(
                name="employee_id",
                description="ID của nhân viên (tùy chọn, nếu muốn lấy 1 nhân viên cụ thể)",
                required=False,
                type=int
            )
        ],
        responses={
            200: EmployeeSerializer(many=True),
            401: OpenApiResponse(description="Unauthorized - Yêu cầu token hợp lệ"),
        }
    )
    def get(self, request, employee_id=None):
        if employee_id:
            employee = EmployeeDAO.get_employee_by_id(employee_id)
            serializer = EmployeeSerializer(employee)
        else:
            employees = EmployeeDAO.get_all_employees()
            serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Thêm mới nhân viên",
        description="Tạo một nhân viên mới với thông tin cần thiết.",
        request=EmployeeSerializer,
        responses={
            201: EmployeeSerializer,
            401: OpenApiResponse(description="Unauthorized - Yêu cầu token hợp lệ"),
        }
    )
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

    @extend_schema(
        summary="Cập nhật thông tin nhân viên",
        description="Cập nhật thông tin của một nhân viên theo ID.",
        parameters=[
            OpenApiParameter(
                name="employee_id",
                description="ID của nhân viên cần cập nhật",
                required=True,
                type=int
            )
        ],
        request=EmployeeSerializer,
        responses={
            200: EmployeeSerializer,
            401: OpenApiResponse(description="Unauthorized - Yêu cầu token hợp lệ"),
        }
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

    @extend_schema(
        summary="Xóa nhân viên",
        description="Xóa một nhân viên theo ID.",
        parameters=[
            OpenApiParameter(
                name="employee_id",
                description="ID của nhân viên cần xóa",
                required=True,
                type=int
            )
        ],
        responses={
            204: None,
            401: OpenApiResponse(description="Unauthorized - Yêu cầu token hợp lệ"),
        }
    )
    def delete(self, request, employee_id):
        if EmployeeDAO.delete_employee(employee_id):
            return Response(
                {"message": "Employee deleted successfully"},
                status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Delete failed employee"},
            status=status.HTTP_400_BAD_REQUEST)






