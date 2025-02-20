from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from crm_system.dao.task_board_dao import TaskBoardDAO
from crm_system.serializers import TaskBoardSerializer


class TaskBoardFilterAPIView(APIView):
    def get(self, request):
        status_filter = request.GET.get("status", None)
        assigned_to_filter = request.GET.get("assigned_to", None)

        tasks = TaskBoardDAO.filter_tasks(
            status=status_filter,
            assigned_to=assigned_to_filter
        )

        serializer = TaskBoardSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
