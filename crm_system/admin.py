from django.contrib import admin
from .models import Customer, Product, Employee, TaskBoard


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock')
    search_fields = ('name',)
    list_filter = ('price',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'email')
    search_fields = ('name', 'position')
    list_filter = ('position',)


@admin.register(TaskBoard)
class TaskBoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'assigned_to')
    search_fields = ('title',)
    list_filter = ('status',)
