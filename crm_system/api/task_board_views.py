from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crm_system.dao.task_board_dao import TaskBoardDAO
from crm_system.serializers import TaskBoardSerializer


class TaskBoardAPIView(APIView):
    def get(self, request, task_id=None):
        if task_id:
            task = TaskBoardDAO.get_task_by_id(task_id)
            serializer = TaskBoardSerializer(task)
        else:
            tasks = TaskBoardDAO.get_all_tasks()
            serializer = TaskBoardSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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