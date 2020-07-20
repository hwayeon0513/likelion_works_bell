from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog

from django.utils import timezone

from .forms import BlogUpdate
from django.core.paginator import Paginator

from faker import Faker

def delete(request, blog_id):
    Blog.objects.get(id=blog_id).delete()
    return redirect('/')

def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/blog/' + str(blog.id))

def simple(request):
    blogs = Blog.objects
    return render(request, 'simple.html', {'blogs': blogs})


# Create your views here.
def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog': blog_detail})

def blog(request):
    blogs = Blog.objects

    #blog를 쿼리셋으로 가져옴
    blog_list = Blog.objects.all()

    #그걸 몇개씩 잘라서 페이지를 만들어줘
    paginator = Paginator(blog_list,10)

    #실제로 페이지에 들어가는 내용을 가져와줘
    page = request.GET.get('page')

    #그걸 뿌릴 수 있게 바꿔저
    articles = paginator.get_page(page)

    return render(request, 'blog.html', {'blogs': blogs,'articles':articles})

def new(request):
    return render(request, 'new.html')

def update(request, blog_id):
    blog = Blog.objects.get(id=blog_id)

    if request.method =='POST':
        form = BlogUpdate(request.POST)
        if form.is_valid():
            blog.title = form.cleaned_data['title']
            blog.body = form.cleaned_data['body']
            blog.pub_date=timezone.now()
            blog.save()
            return redirect('/blog/' + str(blog.id))
    else:
        form = BlogUpdate(instance = blog)
 
        return render(request,'update.html', {'form':form})

def fake(request):
    for i in range(10):
      blog = Blog()
      fake = Faker()
      blog.title = fake.name()
      blog.body = fake.sentence()
      blog.pub_date = timezone.datetime.now()
      blog.save()
    return redirect('/')