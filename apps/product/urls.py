from django.urls import path

from apps.product.views import ImageListView, ImageDetailView

urlpatterns = [
    path('images/', ImageListView.as_view(), name='image-list'),
    path('images/<int:pk>/', ImageDetailView.as_view(), name='image-detail'),
]
