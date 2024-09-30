from django.urls import path

from titanic.views import TitanicView

urlpatterns = [
    path("", TitanicView.as_view(), name="titanic-home"),
]
