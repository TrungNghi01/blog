

from django.views.generic import TemplateView, CreateView

from .forms import CustomUserCreationForm

from django.urls import reverse_lazy

from django.contrib import messages


class SignUpView(CreateView):

    form_class = CustomUserCreationForm

    template_name = "signup.html"

    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):

        user = form.save()
        self.object = user

        messages.error(self.request, 'UserName va Password khong khop')
        
        return super().form_valid(form)

    
class SignUpSuccessView(TemplateView):

    template_name = "signup_success.html"