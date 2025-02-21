from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from crm_system.dao.task_board_dao import TaskBoardDAO
from crm_system.serializers import TaskBoardSerializer


class TaskBoardFilterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Lọc danh sách task",
        description="Trả về danh sách task theo trạng thái hoặc người được giao.",
        parameters=[
            OpenApiParameter(
                name="status",
                description="Trạng thái của task (ví dụ: 'pending', 'completed')",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="assigned_to",
                description="ID của người được giao task",
                required=False,
                type=int
            )
        ],
        responses={200: TaskBoardSerializer(many=True)}
    )
    def get(self, request):
        status_filter = request.GET.get("status", None)
        assigned_to_filter = request.GET.get("assigned_to", None)

        tasks = TaskBoardDAO.filter_tasks(
            status=status_filter,
            assigned_to=assigned_to_filter
        )

        serializer = TaskBoardSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
