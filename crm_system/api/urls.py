from django.urls import path

from crm_system.api.customer_views import CustomerAPIView
from crm_system.api.employee_views import EmployeeAPIView
from crm_system.api.product_views import ProductAPIView
from crm_system.api.task_board_filter_views import TaskBoardFilterAPIView
from crm_system.api.task_board_views import TaskBoardAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("customers/", CustomerAPIView.as_view()),
    path("customers/<int:customer_id>/", CustomerAPIView.as_view()),
    path("employees/", EmployeeAPIView.as_view()),
    path("employees/<int:employee_id>/", EmployeeAPIView.as_view()),
    path("products/", ProductAPIView.as_view()),
    path("products/<int:product_id>/", ProductAPIView.as_view()),
    path("tasks/", TaskBoardAPIView.as_view()),
    path("tasks/<int:task_id>/", TaskBoardAPIView.as_view()),
    path("tasks/filter/", TaskBoardFilterAPIView.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # Endpoint để lấy schema OpenAPI
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # Redoc UI (tùy chọn)
]