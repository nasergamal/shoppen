from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'
urlpatterns = [
    path('' , views.home, name="home"),
    path('new/', views.add_product, name='new_product'),
    path('new/<uuid:id>/update', views.update_product, name='update_product'),
    path('subcat/', views.get_subcategory, name='get_sub'),
    path('cat/<slug:cat_slug>/', views.category, name='category'),
    path('cat/<slug:cat_slug>/<uuid:id>', views.product, name='product'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)