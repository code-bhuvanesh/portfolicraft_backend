from django.urls import path
from .views import LoginView, SignUpView, TestView, home, PortfolioView, CreatePortfolioView, AddProjects
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("",home , name="home"),
    path("login", LoginView.as_view(), name="login"),
    path("signup", SignUpView.as_view(), name="signup"),   
    path("test", TestView.as_view(), name="test"),   
    path("profile", PortfolioView.as_view(), name="profile"),   
    path("createprofile", CreatePortfolioView.as_view(), name="create profile"),   
    path("addprojects", AddProjects.as_view(), name="add projects"),   
    path('refreshtoken', TokenRefreshView.as_view(), name='token_refresh'),   
]
