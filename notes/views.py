from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .filters import NoteFilter


class UserLogin(LoginView) :
    template_name = 'notes/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self) :
        return reverse_lazy('notes')

class RegisterPage(FormView) : 
    template_name = 'notes/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        user = form.save()
        if user is not None :
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs) :
        if self.request.user.is_authenticated :
            return redirect('notes')
        return super(RegisterPage, self).get(*args, **kwargs)

class NoteList(LoginRequiredMixin, ListView) :
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    filter_set = NoteFilter

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user = self.request.user)
        context['filter'] = NoteFilter(self.request.GET, queryset = self.get_queryset())
        

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['notes'] = context['notes'].filter(
                title__contains = search_input)

        context['search_input'] = search_input

        return context

class NoteDetail(LoginRequiredMixin, DetailView) :
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'

class CreateNote(LoginRequiredMixin, CreateView) :
    model = Note
    fields = ['title', 'note']
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateNote, self).form_valid(form)

class UpdateNote(LoginRequiredMixin, UpdateView) :
    model = Note
    fields = ['title', 'note']
    success_url = reverse_lazy('notes')

class DeleteNote(LoginRequiredMixin, DeleteView) :
    model = Note
    context_object_name = 'note'
    success_url = reverse_lazy('notes')