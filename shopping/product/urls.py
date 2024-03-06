from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("product/list/", views.ProductListView.as_view(), name="product_list"),
    path("product/detail/<int:pk>/",views.ProductDetailView.as_view(),name="product_detail"),
    path("category/woman/", views.WomanCategoryListView.as_view(), name="woman_category"),
    path("category/man/", views.ManCategoryListView.as_view(), name="man_category"),
    path("category/child/",views.ChildrenCategoryListView.as_view(),name="child_category"),
    path("category/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("man/",views.CategoryDetailView.as_view(),{"pk": 3},name="man_category_detail",),
    path("woman/",views.CategoryDetailView.as_view(),{"pk": 1},name="woman_category_detail",),
    path("add/order/", views.AddToCartView.as_view(), name="add_product_to_session"),
    path("product/api/", views.ProductAPIView.as_view(), name="product_api_view"),
    path("products/", views.ProductTemplateView.as_view(), name="product_template"),
    path("update_quantity/", views.UpdateQuantityView.as_view(), name="update_quantity"),
    path("search/",views.product_search,name="product_search")

]
