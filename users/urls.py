from django.urls import path

from users.views import UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView

# ----------------------------------------------------------------------------------------------------------------------
# Create user urls
urlpatterns = [
    path('', UserListView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('<int:pk>/update/', UserUpdateView.as_view()),
    path('<int:pk>/delete/', UserDeleteView.as_view()),
]
