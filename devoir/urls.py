from django.urls import path
from .views import DevoirAdd, GetAllDevoir, GestionDevoir , GeneralStatApiView,DevoirStats,DevoirElementStats,SubmitProfStats,SubmitElementStats


urlpatterns = [
    path('', DevoirAdd.as_view()),
    path('all', GetAllDevoir.as_view()),
    path('<int:id>', GestionDevoir.as_view()),
    path('stats', GeneralStatApiView.as_view()),
    path('stats', GeneralStatApiView.as_view()),
    path('devoirstats', DevoirStats.as_view()),
    path('devoirelement/<int:id>', DevoirElementStats.as_view()),
    path('submitdevoir/<int:id>', SubmitProfStats.as_view()),
    path('submitElement/<int:id>', SubmitElementStats.as_view()),


]

