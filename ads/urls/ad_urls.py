from django.urls import path

from ads.views import AdListView, AdCreateView, AdDetailView, AdUpdateView, AdDeleteView, AdUploadImage

# ----------------------------------------------------------------------------------------------------------------------
# Create advertisement urls
urlpatterns = [
    path('', AdListView.as_view()),
    path('create/', AdCreateView.as_view()),
    path('<int:pk>/', AdDetailView.as_view()),
    path('<int:pk>/update/', AdUpdateView.as_view()),
    path('<int:pk>/delete/', AdDeleteView.as_view()),
    path('<int:pk>/upload_image/', AdUploadImage.as_view())
]
