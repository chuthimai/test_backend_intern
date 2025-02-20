from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Customer, Product, Employee, TaskBoard
from .serializers import CustomerSerializer, ProductSerializer, EmployeeSerializer, TaskBoardSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class TaskBoardViewSet(viewsets.ModelViewSet):
    queryset = TaskBoard.objects.all()
    serializer_class = TaskBoardSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status', 'assigned_to__name']

    @action(detail=False, methods=['get'])
    def filter_by_status(self, request):
        status = request.query_params.get('status', None)
        if status:
            tasks = self.queryset.filter(status=status)
        else:
            tasks = self.queryset
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
