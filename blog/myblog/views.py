from django.core.mail import EmailMessage
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, DeleteView, UpdateView

from .models import Category, Post, Comment

from .forms import ContactForm, PostForm, CommentForm

class AllCategoryMixin:
    '''View này để Mixin nhằm lấy danh sách danh mục (category list)'''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # lấy toàn bộ danh mục gán vào context["categories"]
        context["categories"] = Category.objects.all()

        return context

class IndexView(AllCategoryMixin, ListView):
    '''View này là trang chính'''
    template_name = 'myblog/index.html'
    
    paginate_by = 3

    def get_queryset(self):
        queryset = Post.objects.order_by('-posted_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['current_user'] = self.request.user

        return context
    
class CategorySearchView(AllCategoryMixin, ListView):
    ''' View này để tìm kiếm theo danh mục (search by category)'''
    template_name = "myblog/search-result.html"

    def get_queryset(self):
        c_id = self.kwargs["category"]
        # lấy data mà id category trong Post（ForeignKey:Category）có cùng với c_id
        products = Post.objects.filter(category_id=c_id)
        return products

class PostDetailView(DetailView):
    template_name = "myblog/post-detail.html"
    
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('myblog:post-detail', pk=post.pk) 
        return render(request, self.template_name, {'form': form, 'post': post})

class AboutView(TemplateView):
    template_name = 'myblog/about.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #ログインしているユーザーのデータを取得
        context['current_user'] = self.request.user

        return context

class ContactView(FormView):
    template_name = 'myblog/contact.html'  

    form_class = ContactForm

    success_url = reverse_lazy("myblog:contact") 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #ログインしているユーザーのデータを取得
        context['current_user'] = self.request.user

        return context


    def form_valid(self, form):
        # Đặt biến tạm, lấy data từ forms.py gán vào biến tạm
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phonenumber = form.cleaned_data['phonenumber']
        message = form.cleaned_data['message']   

        # thiết lập định dạng phonenumber
         # cách ghi 1
        # subject = 'Liên hệ: {}'.format(phonenumber)

         # cách ghi 2
        subject = f'Liên hệ: {phonenumber}'

        # thiết lập định dạng dữ liệu nhập vào form
         # cách ghi 1
        # message = 'Tên người gửi: {0}\nEmail: {1}\n Số điện thoại:{2}\n Lời nhắn:\n{3}'.format(name, email, phonenumber, message)
        
         # cách ghi 2
        message = f'Tên người gửi: {name}\nEmail: {email}\nSố điện thoại:{phonenumber}\nLời nhắn:\n{message}' 
        
        # Email của người gửi
        from_email = 'caonguyen26032001@gmail.com'
        # Danh sách địa chỉ email cần gửi
        to_list = ['caonguyen26032001@gmail.com']

        # Tạo object EmailMessage
        message = EmailMessage(subject=subject,#Tiêu đề
                               body=message, #Nội dung
                               from_email=from_email, #mail người gửi
                               to=to_list, #Danh sách địa chỉ email cần gửi tới
                               )
        
        # dùng method .send() của class EmailMessage để gửi mail
        message.send()

        # message sẽ được hiển thị sau khi gửi thành công 
        messages.success(self.request, 'Đã gửi thành công!')

        return super().form_valid(form)

class CreatePostView(CreateView):
    form_class = PostForm
    template_name = 'myblog/create-post.html'
    success_url = reverse_lazy('myblog:myblog/create-post-done')

    def form_valid(self, form):
        
        postdata = form.save(commit=False)

        postdata.user = self.request.user

        print(postdata.category)


        postdata.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
 
        context['current_user'] = self.request.user
 
        return context

@method_decorator(login_required, name='dispatch')
class CreatePostDoneView(TemplateView):
    template_name = 'myblog/create-post-done.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        #ログインしているユーザーのデータを取得
        context['current_user'] = self.request.user

        return context

class PostedByCategoryView(AllCategoryMixin, ListView):
    '''Hiển thị sản phẩm theo category'''
    template_name = 'myblog/index.html'
    paginate_by = 3

    # lấy dữ liệu DB theo dieu kien filter và hiển thị ra index.html
    def get_queryset(self):
        # self.kwargs["category"] ... lấy ID category
        category_id = self.kwargs['category']
        # filter(fieldname＝value)...truy vấn các sản phẩm có category tương ứng
        categories = Post.objects.filter(category=category_id).order_by('-posted_at')
        return categories
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context
    
class PostedByUserView(AllCategoryMixin, ListView):
    '''Hiển thị sản phẩm theo user'''
    template_name = 'myblog/index.html'
    paginate_by = 3

    # lấy dữ liệu DB theo dieu kien filter và hiển thị ra index.html
    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = Post.objects.filter(user=user_id).order_by('-posted_at')
        return user_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context
    
@method_decorator(login_required, name='dispatch')         
class DeletePostView(DeleteView):
    '''View này để xác nhận có xóa đối tượng bài viết từ DB hay không'''

    # Đầu tiên chỉ định model mà chúng ta muốn xóa
    # django sẽ tự động xác định đối tượng cần xóa dựa trên pk (primary key)  được cung cấp trong URL
    model = Post

    # Chỉ định template sẽ được sử dụng để hiển thị trang xác nhận xóa bài viết:
    template_name = 'myblog/delete-post.html'

    # URL chuyển hướng sau khi xóa thành công:
    success_url = reverse_lazy('myblog:myblog/delete-post-done') 

    # Xử lý việc xóa dữ liệu
    # form_valid(self, form) gọi khi biểu mẫu (form) hợp lệ, tức là khi người dùng xác nhận việc xóa.
    def form_valid(self, form):

        # Kiểm tra quyền xóa
        # Kiểm tra xem người dùng hiện tại có phải là tác giả của bài viết không.
        # self.get_object() lấy đối tượng bài viết hiện tại từ URL.
        if self.get_object().user == self.request.user:

            # Thực hiện xóa nếu đủ quyền:
            # Nếu người dùng là tác giả của bài viết, gọi phương thức form_valid của lớp cha để thực hiện việc xóa bài viết.
            return super().form_valid(form)
        else:
            # Chuyển hướng nếu không đủ quyền:
            # Nếu người dùng không phải là tác giả, sẽ chuyển hướng đến trang index
            return HttpResponseRedirect(reverse_lazy("myblog:myblog/index")) 
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context

@method_decorator(login_required, name='dispatch')         
class DeletePostDoneView(TemplateView):
    '''View này để thông báo xóa bài viết thành công'''
    template_name = "myblog/delete-post-done.html"
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        #ログインしているユーザーのデータを取得
        context['current_user'] = self.request.user

        return context
    
@method_decorator(login_required, name='dispatch') 
class MypageView(ListView):
    '''View này để quản lý trang cá nhân của mình'''
    template_name = 'myblog/mypage.html'
    paginate_by = 3

    def get_queryset(self):
        # có 2 cách
        # cách 1:
        # lấy dữ liệu trong Post-database mà user đang đăng nhập đã đăng
        # self.request.user ...là user đang đăng nhập
        queryset = Post.objects.filter(user=self.request.user).order_by('-posted_at')
        # cách 2: tham chiếu ngược
        # lấy danh sách Post tham chiếu ngược với user đang đăng nhập
        # Danh xưng mà ta sẽ tham chiếu ngược -> đặt chữ in thường cho tên Class_set 
        queryset = self.request.user.post_set.all().order_by("-posted_at")

        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user

        return context
    
@method_decorator(login_required, name='dispatch') 
class PostUpdateView(UpdateView):
    '''View này để edit bài viết tại trang cá nhân của mình'''

    model = Post
    form_class = PostForm
    template_name = 'myblog/edit-post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('myblog:mypage')  # Chuyển hướng sau khi cập nhật thành công

    def get_queryset(self):
        # Chỉ cho phép người dùng chỉnh sửa các bài viết mà họ sở hữu
        return Post.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user

        return context
    

    
    
