from django.core.mail import EmailMessage
from django.contrib import messages
from typing import Any
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView

from .forms import ContactForm, PostForm
from .models import Blog

# Create your views here.
class IndexView(ListView):
    template_name = 'myblog/index.html'

    # take data from database and return it back to template
    def get_queryset(self):
        queryset = Blog.objects.order_by('-posted_at')
        return queryset
    
    # this is to set the text size
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)    
    #    context ['mydata'] = self.request.GET.get('mydata')
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
 
        #ログインしているユーザーのデータを取得
        context['current_user'] = self.request.user
 
        return context

class DetailContentView(DetailView):
    template_name = "myblog/detail_content.html"
    model = Blog

class AboutView(TemplateView):
    template_name = 'myblog/about.html'

class ContactView(FormView):
    template_name = 'myblog/contact.html'
    form_class = ContactForm

    success_url = reverse_lazy('home:contact')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     context['current_user'] = self.request.user
    #     return 

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phoneNumber = form.cleaned_data['phoneNumber']
        message = form.cleaned_data['message']

        #subject = 'conttact via phone {}'.format(phoneNumber)
        subject = f'contact via phone {phoneNumber}'
        message = f'1. Name: {name}\n2. Email: {email}\n3. Message: {message}'
        from_email = 'kakakoko0233@gmail.com'
        to_list = ['kakakoko0233@gmail.com']

        message = EmailMessage(subject = subject, body = message, from_email = from_email , to = to_list)

        message.send()

        messages.success(self.request, 'Email has been sent successfully')
        

        return super().form_valid(form)
    

class PostView(TemplateView):
    template_name = 'myblog/post.html'

@method_decorator(login_required, name='dispatch')
class CreatePostView(CreateView):
    form_class = PostForm
    template_name = 'myblog/create-post.html'
    success_url = reverse_lazy('home:myblog/create-post-done')

    def form_valid(self, form):
        postdata = form.save(commit=False)

        postdata.user = self.request.user

        postdata.save()

        return super().form_valid(form)
    

class CreatePostDoneView(TemplateView):
    template_name = 'myblog/create-post-done.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
 
        #ログインしているユーザーのデータを取得
        context['current_user'] = self.request.user
 
        return context