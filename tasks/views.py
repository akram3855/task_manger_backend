from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Task
from .serializers import TaskSerializer
from .authentication import APIKeyAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('id')
    serializer_class = TaskSerializer
    authentication_classes = [APIKeyAuthentication]
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['status', 'priority', 'due_date']
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'title']

    def get_queryset(self):
        queryset = super().get_queryset()

        due_before = self.request.query_params.get('due_before')
        due_after = self.request.query_params.get('due_after')
        if due_before:
            queryset = queryset.filter(due_date__lte=due_before)
        if due_after:
            queryset = queryset.filter(due_date__gte=due_after)

        return queryset