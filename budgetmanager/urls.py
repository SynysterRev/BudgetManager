"""
URL configuration for budgetmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import include, path

from expenses.views import DashboardView, ExpenseView, CategoryView, CategoryCreateView, \
    CategoryDeleteView, CategoryEditView, ExpenseCreateView, ExpenseEditView, \
    ExpenseDeleteView, ExpenseExportCSV
from users.forms import LoginForm
from users.views import SignupView, SettingsView, DeleteUserView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", SignupView.as_view(), name="signup"),
    path(
        "login/",
        LoginView.as_view(
            template_name="users/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", DashboardView.as_view(), name="dashboard"),
    path("expenses/", ExpenseView.as_view(), name="expenses"),
    path("expenses/create/", ExpenseCreateView.as_view(), name="create_expense"),
    path("expenses/<int:expense_id>/edit/", ExpenseEditView.as_view(),
         name="edit_expense"),
    path("expenses/<int:expense_id>/delete/", ExpenseDeleteView.as_view(),
         name="delete_expense"),
    path("categories/", CategoryView.as_view(), name="categories"),
    path("categories/create/", CategoryCreateView.as_view(),
         name="create_category"),
    path("categories/<str:name>/edit/", CategoryEditView.as_view(),
         name="edit_category"),
    path("categories/<str:name>/delete/", CategoryDeleteView.as_view(),
         name="delete_category"),
    path("expenses/export_csv/", ExpenseExportCSV.as_view(), name="export_csv"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path('settings/delete-account/', DeleteUserView.as_view(), name='delete_account'),
    path("__reload__/", include("django_browser_reload.urls")),
]
