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
    def get_context_data(self, **kwargs):
        # Gọi phương thức get_context_data của lớp cha để lấy context ban đầu
        context = super().get_context_data(**kwargs)

        # Thêm tất cả các đối tượng Category vào context với khóa 'categories'
        context["categories"] = Category.objects.all()

        # Trả về context đã được bổ sung
        return context

class IndexView(AllCategoryMixin, ListView):
    # Template sẽ được render cho trang chính
    template_name = 'myblog/index.html'

    # Số lượng bài đăng hiển thị trên mỗi trang (phân trang)
    paginate_by = 3

    def get_queryset(self):
        # Truy vấn các bài đăng từ cơ sở dữ liệu, sắp xếp theo ngày đăng (mới nhất lên đầu)
        queryset = Post.objects.order_by('-posted_at')
        
        # Trả về queryset các bài đăng đã được sắp xếp
        return queryset

    def get_context_data(self, **kwargs):
        # Lấy các context cơ bản từ phương thức cha (ListView)
        context = super().get_context_data(**kwargs)

        # Thêm thông tin người dùng hiện tại vào context
        context['current_user'] = self.request.user

        return context
    
class CategorySearchView(AllCategoryMixin, ListView):
    # Template sẽ hiển thị kết quả tìm kiếm theo danh mục
    template_name = "myblog/search-result.html"

    def get_queryset(self):
        # Lấy ID danh mục từ URL kwargs (chắc chắn rằng URL được cấu hình đúng)
        c_id = self.kwargs["category"]

        # Lọc các bài đăng (Post) có category_id trùng với ID danh mục
        products = Post.objects.filter(category_id=c_id)

        # Trả về danh sách bài đăng thuộc danh mục đó
        return products

class PostDetailView(DetailView):
    # Template để render chi tiết bài đăng
    template_name = "myblog/post-detail.html"
    
    # Model mà view này sẽ làm việc, ở đây là Post
    model = Post

    # Phương thức POST để xử lý khi người dùng gửi bình luận
    def post(self, request, *args, **kwargs):
        # Lấy bài đăng hiện tại từ URL (pk)
        post = self.get_object()

        # Khởi tạo form từ dữ liệu POST
        form = CommentForm(request.POST)

        # Kiểm tra nếu form hợp lệ
        if form.is_valid():
            # Tạo đối tượng bình luận nhưng chưa lưu vào DB
            comment = form.save(commit=False)

            # Gán bài đăng và người dùng vào bình luận
            comment.post = post
            comment.user = request.user

            # Lưu bình luận vào cơ sở dữ liệu
            comment.save()

            # Sau khi lưu bình luận thành công, chuyển hướng lại về trang chi tiết bài đăng
            return redirect('myblog:post-detail', pk=post.pk) 

        # Nếu form không hợp lệ, render lại trang chi tiết bài đăng cùng với form bình luận
        return render(request, self.template_name, {'form': form, 'post': post})

    # Phương thức để thêm các context vào template, bao gồm các thông tin về bài đăng và bình luận
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['current_user'] = self.request.user

        # Thêm tất cả các bình luận của bài đăng vào context
        context['comments'] = self.object.comments.all()

        # Khởi tạo form bình luận trống để hiển thị trên trang
        context['form'] = CommentForm()

        return context

class AboutView(TemplateView):
    template_name = 'myblog/about.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #ログインしているユーザーのデータを取得
        context['current_user'] = self.request.user

        return context

class ContactView(FormView):
    # Template HTML sẽ render form liên hệ cho người dùng nhập liệu
    template_name = 'myblog/contact.html'

    # Form sẽ sử dụng trong view này, là ContactForm
    form_class = ContactForm

    # Đường dẫn chuyển hướng sau khi gửi form thành công
    success_url = reverse_lazy("myblog:contact")

    def form_valid(self, form):
        # Lấy dữ liệu từ các trường của form sau khi được validate (hợp lệ)
        name = form.cleaned_data['name']  # Tên người gửi
        email = form.cleaned_data['email']  # Email của người gửi
        phonenumber = form.cleaned_data['phonenumber']  # Số điện thoại
        message = form.cleaned_data['message']  # Nội dung lời nhắn

        # Cách ghi 1 (sử dụng .format())
        # subject = 'Liên hệ: {}'.format(phonenumber)

        # Cách ghi 2 (sử dụng f-string')
        subject = f'Liên hệ: {phonenumber}'  # Tiêu đề email

        # Nội dung của email, sử dụng f-string để dễ đọc hơn
        message = f'Tên người gửi: {name}\nEmail: {email}\nSố điện thoại:{phonenumber}\nLời nhắn:\n{message}' 

        # Địa chỉ email của người gửi
        from_email = 'caonguyen26032001@gmail.com'

        # Danh sách email người nhận (có thể gửi tới nhiều email)
        to_list = ['caonguyen26032001@gmail.com']

        # Tạo một EmailMessage với tiêu đề, nội dung, người gửi, và người nhận
        message = EmailMessage(
            subject=subject,  # Tiêu đề của email
            body=message,  # Nội dung của email
            from_email=from_email,  # Địa chỉ email của người gửi
            to=to_list,  # Danh sách địa chỉ email cần gửi tới
        )
        
        # Gửi email
        message.send()

        # Hiển thị thông báo thành công trên giao diện
        messages.success(self.request, 'Đã gửi thành công!')

        # Chuyển hướng người dùng đến success_url sau khi gửi thành công
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #ログインしているユーザーのデータを取得
        context['current_user'] = self.request.user

        return context

class CreatePostView(CreateView):
    # Khai báo form sẽ sử dụng trong view này, ở đây là PostForm
    form_class = PostForm

    # Template sẽ render form cho người dùng nhập liệu
    template_name = 'myblog/create-post.html'

    # Đường dẫn sẽ chuyển hướng đến sau khi bài đăng được tạo thành công
    success_url = reverse_lazy('myblog:myblog/create-post-done')

    def form_valid(self, form):
        # Tạo một instance của model Post từ form mà không lưu vào DB ngay lập tức
        postdata = form.save(commit=False)

        # Gán người dùng hiện tại làm tác giả của bài đăng
        postdata.user = self.request.user

        # Lưu instance vào DB sau khi đã gán thuộc tính user
        postdata.save()

        # Gọi phương thức form_valid của CreateView để xử lý chuyển hướng
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
    

    
    
