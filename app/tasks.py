from celery import shared_task
from django.apps import apps


@shared_task()
def some_task(post_id: int) -> bool:
    Post = apps.get_model("app.Post", require_ready=False)
    try:
        post = Post.objects.get(pk=post_id)
        print(f"Нашли заметку с id = {post_id} и содержимым {post.content}")
    except Post.DoesNotExist:
        print(f"Нет заметки с id = {post_id}")
        return False
    else:
        return True
