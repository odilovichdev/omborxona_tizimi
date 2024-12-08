from django.urls import path

from product.views import ProductMaterialInfoAPIView

urlpatterns = [
    path("product/", ProductMaterialInfoAPIView.as_view()),
]