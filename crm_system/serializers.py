from rest_framework import serializers
from .models import Customer, Product, Employee, TaskBoard


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class TaskBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskBoard
        fields = '__all__'
