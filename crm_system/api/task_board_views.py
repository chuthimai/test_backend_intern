from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crm_system.dao.task_board_dao import TaskBoardDAO
from crm_system.serializers import TaskBoardSerializer


class TaskBoardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Lấy danh sách task hoặc task cụ thể",
        description="Lấy danh sách tất cả các task hoặc task theo `task_id`.",
        parameters=[
            OpenApiParameter(
                name="task_id",
                description="ID của task cần lấy thông tin",
                required=False,
                type=int
            )
        ],
        responses={
            200: TaskBoardSerializer(many=True),
            401: OpenApiResponse(description="Unauthorized - Yêu cầu token hợp lệ"),
        }
    )
    def get(self, request, task_id=None):
        if task_id:
            task = TaskBoardDAO.get_task_by_id(task_id)
            serializer = TaskBoardSerializer(task)
        else:
            tasks = TaskBoardDAO.get_all_tasks()
            serializer = TaskBoardSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Tạo mới một task",
        description="Thêm một task mới vào hệ thống.",
        request=TaskBoardSerializer,
        responses={
            201: TaskBoardSerializer,
            401: OpenApiResponse(description="Unauthorized - Yêu cầu token hợp lệ"),
        }
    )
    def post(self, request):
        task = TaskBoardDAO.create_task(**request.data)
        if task:
            return Response(
                TaskBoardSerializer(task).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": "Add failed task"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        summary="Cập nhật thông tin một task",
        description="Cập nhật thông tin của task theo `task_id`.",
        parameters=[
            OpenApiParameter(
                name="task_id",
                description="ID của task cần cập nhật",
                required=True,
                type=int
            )
        ],
        request=TaskBoardSerializer,
        responses={
            200: TaskBoardSerializer,
            401: OpenApiResponse(description="Unauthorized - Yêu cầu token hợp lệ"),
        }
    )
    def put(self, request, task_id):
        task = TaskBoardDAO.update_task(task_id, **request.data)
        if task:
            return Response(
                TaskBoardSerializer(task).data,
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Update failed task"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        summary="Xóa một task",
        description="Xóa task theo `task_id` khỏi hệ thống.",
        parameters=[
            OpenApiParameter(
                name="task_id",
                description="ID của task cần xóa",
                required=True,
                type=int
            )
        ],
        responses={
            204: None,
            401: OpenApiResponse(description="Unauthorized - Yêu cầu token hợp lệ"),
        }
    )
    def delete(self, request, task_id):
        if TaskBoardDAO.delete_task(task_id):
            return Response(
                {"message": "Task deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"error": "Delete failed task"},
            status=status.HTTP_400_BAD_REQUEST
        )