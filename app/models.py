from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.tasks import some_task


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag, blank=True)

    def short_content(self):
        return self.content[:10]

    def __str__(self):
        return f"Post: {self.title}; {self.short_content()}"


@receiver(post_save, sender=Post)
def test_signal_func(sender, instance, created, **kwargs):
    some_task.delay(instance.id)
