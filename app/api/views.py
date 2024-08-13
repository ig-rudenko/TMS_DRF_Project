from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from app.models import Post
from .filters import PostFilter
from .serializers import PostSerializer


@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})


class PostsListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request):
        serializer = PostSerializer(Post.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request: Request):
        user_data = request.data

        print("data", user_data)

        serializer = PostSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")
        tags = serializer.validated_data.get("tags")

        print(tags)

        post = Post.objects.create(title=title, content=content, user=request.user)
        post.tags.add(*tags)

        resp_serializer = PostSerializer(post)

        return Response(resp_serializer.data, status=status.HTTP_201_CREATED)


class PostsGenericListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = PostFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostSerializer
        return PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).select_related("user").prefetch_related("tags")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
