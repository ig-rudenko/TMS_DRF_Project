from django.urls import path

from . import views


# /api/v1/posts/

urlpatterns = [
    path("", views.PostsGenericListCreateAPIView.as_view()),
    # path("<int:post_id>", views.post_api_view),
]
