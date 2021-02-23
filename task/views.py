import datetime
import calendar

from datetime import date
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from .forms import *
from .models import *
from .permissions import *
from .utils import *


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, ListView):
    """Вывод календаря на месяц с заметками и задачами"""
    login_url = 'login_page'
    template_name = 'task/calendar.html'

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = CalendarUtil(d.year, d.month)
        html_cal = cal.formattmonth(withyear=True, theyear=d.year, themonth=d.month,
                                    tasks=Task.objects.filter(start_date__year=d.year,
                                                              start_date__month=d.month,
                                                              author=self.request.user),
                                    notes=Note.objects.filter(date__year=d.year,
                                                              date__month=d.month,
                                                              author=self.request.user))
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


class ArticleListView(ListView):
    """Список статей"""
    model = Article
    queryset = Article.objects.filter(draft=False)


class ArticleDetailView(DetailView):
    """Полная информация об статье"""
    model = Article


class NoteListView(LoginRequiredMixin, ListView):
    """Список заметок"""
    model = Note
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)


class NoteCreate(LoginRequiredMixin, CreateView):
    """Создание заметки"""
    model = Note
    fields = ['name', 'description', 'category']
    template_name = 'task/note_list.html'
    success_url = '/notes/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteDetailView(AuthorPermissionMixin, DetailView):
    """Полная информация об заметке"""
    model = Note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class NoteUpdate(AuthorPermissionMixin, UpdateView):
    """Редактирование заметки"""
    model = Note
    fields = ['name', 'description', 'category']
    template_name = 'task/note_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.success_url = self.request.POST.get('previous_page')
        return super().form_valid(form)


class NoteDelete(AuthorPermissionMixin, DeleteView):
    """Удаление заметки"""
    model = Note
    success_url = reverse_lazy('note_list')
    template_name = 'task/note_detail.html'


class TaskListView(LoginRequiredMixin, ListView):
    """Список задач"""
    model = Task
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)


class TaskCreateView(CreateView):
    """Создание задачи"""
    model = Task
    fields = ['name', 'description', 'end_date', 'category']
    template_name = 'task/task_list.html'
    success_url = '/tasks/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(AuthorPermissionMixin, DetailView):
    """Полная информация о задаче"""
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class TaskUpdateView(AuthorPermissionMixin, UpdateView):
    """Изменение задачи"""
    model = Task
    fields = ['name', 'description', 'end_date', 'category', 'completed']
    template_name = 'task/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.success_url = self.request.POST.get('previous_page')
        return super().form_valid(form)


class TaskDeleteView(AuthorPermissionMixin, DeleteView):
    """Удаление задачи"""
    model = Task
    success_url = reverse_lazy('task_list')
    template_name = 'task/task_detail.html'


class UserLoginView(LoginView):
    """Авторизация пользователя"""
    form_class = AuthUserForm
    success_url = reverse_lazy('article_list')
    template_name = 'account/login.html'

    def get_success_url(self):
        return self.success_url


class RegisterUserView(CreateView):
    """Вывод страницы для регистрации пользователя"""
    model = User
    template_name = 'account/register_page.html'
    success_url = reverse_lazy('article_list')
    form_class = RegisterUserForm

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('article_list')
