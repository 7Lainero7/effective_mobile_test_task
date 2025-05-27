from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from .models import Ad, ExchangeProposal
from .serializers import (
    AdSerializer,
    AdCreateSerializer,
    ExchangeProposalSerializer,
    ExchangeProposalUpdateSerializer,
    UserSerializer
)
from .permissions import IsOwnerOrReadOnly, IsReceiverOrReadOnly
from .filters import AdFilter


User = get_user_model()


class AdViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с объявлениями.
    Поддерживает создание, просмотр, обновление и удаление объявлений.
    """
    queryset = Ad.objects.all().order_by('-created_at')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AdFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']  # Сортировка по умолчанию

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AdCreateSerializer
        return AdSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def my_ads(self, request):
        """Получение списка объявлений текущего пользователя"""
        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def proposals(self, request, pk=None):
        """Получение предложений для конкретного объявления"""
        ad = self.get_object()
        if ad.user != request.user:
            raise PermissionDenied("Вы не являетесь автором этого объявления.")
        proposals = ExchangeProposal.objects.filter(ad_receiver=ad)
        serializer = ExchangeProposalSerializer(proposals, many=True)
        return Response(serializer.data)


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с предложениями обмена.
    Поддерживает создание, просмотр и обновление предложений.
    """
    queryset = ExchangeProposal.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'ad_sender', 'ad_receiver']
    ordering_fields = ['created_at']
    ordering = ['-created_at']  # Сортировка по умолчанию

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsReceiverOrReadOnly()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ExchangeProposalUpdateSerializer
        return ExchangeProposalSerializer

    def perform_create(self, serializer):
        ad_receiver = serializer.validated_data.get('ad_receiver')
        # Проверка: нельзя отправить предложение на свой товар
        if ad_receiver.user == self.request.user:
            raise PermissionDenied("Вы не можете отправить предложение на свой товар.")
        serializer.save(status='pending')

    def destroy(self, request, *args, **kwargs):
        """Удаление предложения (только для отправителя)"""
        instance = self.get_object()
        if instance.ad_sender.user != request.user:
            raise PermissionDenied("Вы можете удалять только свои предложения.")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def sent(self, request):
        """Список отправленных пользователем предложений"""
        queryset = self.filter_queryset(
            self.get_queryset().filter(ad_sender__user=request.user)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def received(self, request):
        """Список полученных пользователем предложений"""
        queryset = self.filter_queryset(
            self.get_queryset().filter(ad_receiver__user=request.user)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с пользователями (только чтение)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
