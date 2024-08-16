from django.db.models.functions.text import Substr
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Post
from .filters import PostFilter
from .serializers import PostSerializer
from .services import get_cached_posts_list, clean_cached_posts_list


# Функция представления на основе декоратора для простого API-запроса
@api_view()
def hello_world(request):
    # Возвращает простой ответ "Hello, world!" в формате JSON
    return Response({"message": "Hello, world!"})


# Класс представления на основе APIView для обработки запросов на получение и создание постов
class PostsListCreateAPIView(APIView):
    # Устанавливаем права доступа: только аутентифицированные пользователи могут создавать записи,
    # а неаутентифицированные могут только читать
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Метод для обработки GET-запросов
    def get(self, request: Request):
        # Получаем все объекты Post из базы данных
        posts = Post.objects.all()
        # Сериализуем данные объектов Post
        serializer = PostSerializer(posts, many=True)
        # Возвращаем сериализованные данные в формате JSON
        return Response(serializer.data)

    # Метод для обработки POST-запросов
    def post(self, request: Request):
        # Получаем данные из запроса
        user_data = request.data

        # Создаем сериализатор с данными из запроса
        serializer = PostSerializer(data=user_data)
        # Проверяем валидность данных, в случае ошибки вызываем исключение
        serializer.is_valid(raise_exception=True)

        # Извлекаем отдельные поля из валидированных данных
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")
        tags = serializer.validated_data.get("tags")

        # Создаем новый объект Post и сохраняем его в базе данных
        post = Post.objects.create(title=title, content=content, user=request.user)
        # Добавляем теги к посту
        post.tags.add(*tags)

        # Сериализуем созданный объект Post
        resp_serializer = PostSerializer(post)

        # Возвращаем сериализованные данные созданного поста и статус HTTP 201 (Created)
        return Response(resp_serializer.data, status=status.HTTP_201_CREATED)


# Класс представления на основе ListCreateAPIView для обработки запросов с пагинацией и фильтрацией
class PostsGenericListCreateAPIView(ListCreateAPIView):
    # Указываем класс сериализатора
    serializer_class = PostSerializer
    # Указываем класс пагинации
    pagination_class = PageNumberPagination
    # Устанавливаем права доступа: только аутентифицированные пользователи могут создавать записи,
    # а неаутентифицированные могут только читать
    permission_classes = [IsAuthenticatedOrReadOnly]
    # Указываем класс фильтрации
    filterset_class = PostFilter

    # Метод для определения класса сериализатора в зависимости от типа запроса
    def get_serializer_class(self):
        # Если метод запроса GET, возвращаем сериализатор для получения данных
        if self.request.method == "GET":
            return PostSerializer
        # Иначе возвращаем сериализатор для создания/обновления данных
        return PostSerializer

    # Метод для получения набора данных (queryset) для запросов
    def get_queryset(self):
        # Возвращаем отфильтрованные объекты Post, связанные с текущим пользователем
        qs = (
            Post.objects.filter(user=self.request.user)
            .annotate(short_content=Substr("content", 1, 10))
            .select_related("user")
            .prefetch_related("tags")
            .only("title", "tags", "user__username", "user__email")
        )
        return qs

    def get(self, request, *args, **kwargs):
        data = get_cached_posts_list(
            self.request,
            lambda: super(PostsGenericListCreateAPIView, self).get(request, *args, **kwargs).data,
        )
        return Response(data)

    # Метод для выполнения дополнительных действий при создании объекта
    def perform_create(self, serializer):
        # Сохраняем объект Post, связывая его с текущим пользователем
        serializer.save(user=self.request.user)
        clean_cached_posts_list(self.request)
