from crm_system.dao.employee_dao import EmployeeDAO
from crm_system.models import TaskBoard, Employee


class TaskBoardDAO:
    @staticmethod
    def create_task(
            title: str,
            assigned_to: int,
            status: str = 'todo',
            description: str = None
    ):
        try:
            employee = EmployeeDAO.get_employee_by_id(assigned_to)
            task = TaskBoard(
                title=title,
                description=description,
                assigned_to=employee,
                status=status
            )
            task.save()
            return task
        except Employee.DoesNotExist:
            return None

    @staticmethod
    def get_all_tasks():
        return TaskBoard.objects.all()

    @staticmethod
    def get_task_by_id(task_id: int):
        return TaskBoard.objects.get(id=task_id).first()

    @staticmethod
    def update_task(
            task_id: int,
            title: str = None,
            description: str = None,
            assigned_to=None,
            status: str = None
    ):
        task = TaskBoardDAO.get_task_by_id(task_id)
        if not task:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if assigned_to is not None:
            task.assigned_to = assigned_to
        if status is not None:
            task.status = status

        task.save()
        return task

    @staticmethod
    def delete_task(task_id: int):
        task = TaskBoardDAO.get_task_by_id(task_id)
        if task:
            task.delete()
            return True
        return False

    @staticmethod
    def filter_tasks(status: str = None, assigned_to=None):
        if status and assigned_to:
            tasks = TaskBoard.objects.filter(status=status, assigned_to=assigned_to)
        elif status:
            tasks = TaskBoard.objects.filter(status=status)
        else:
            tasks = TaskBoard.objects.filter(assigned_to=assigned_to)
        return tasks
