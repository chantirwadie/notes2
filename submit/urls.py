from django.urls import path
from .views import SubmitAdd, GetAllSubmit, GestionSubmit
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', SubmitAdd.as_view()),
    path('all', GetAllSubmit.as_view()),
    path('<int:id>', GestionSubmit.as_view()),

]

