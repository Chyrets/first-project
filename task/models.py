import random
import string

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class Category(models.Model):
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание", max_length=5000)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание", max_length=5000, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task")
    start_date = models.DateField("Начало", auto_now_add=True)
    end_date = models.DateField("Конец", blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, blank=True, null=True)
    completed = models.BooleanField("Завершена", default=False)
    slug = models.SlugField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"slug": self.slug})

    @property
    def get_html_url(self):
        url = reverse("task_detail", kwargs={"slug": self.slug})
        return f'<a href="{url}"> {self.name} </a>'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug())
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Note(models.Model):
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание", max_length=5000, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="note")
    date = models.DateField("Дата", auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse("note_detail", kwargs={"slug": self.slug})

    @property
    def get_html_url(self):
        url = reverse("note_detail", kwargs={"slug": self.slug})
        return f'<a href="{url}"> {self.name} </a>'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.name)
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    poster = models.ImageField("Постер", upload_to='poster/')
    about = models.TextField("Основное", max_length=1000)
    description = models.TextField("Описание")
    date = models.DateField("Дата", auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, blank=True, null=True)
    draft = models.BooleanField("Черновик", default=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title
