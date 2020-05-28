from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
# Create your views here.

# retrieve all pulished posts
def post_list(request):
    object_lst = Post.published.all()
    paginator = Paginator(object_lst,3) # 3 posts per page
    page = request.GET.get('page') # get the current page
    try:
        posts = paginator.page(page) # try to display the current page
    except PageNotAnInteger:
        posts = paginator.page(1) # If the page number is not an integer or below page range
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'blog/post/list.html',{'page':page,'posts':posts})

#retrieve a single published post
def post_detail(request,year,month,day,slug_name):
    post =  get_object_or_404(Post,
    slug = slug_name,publish__year = year, publish__month = month, publish__day = day)
    return render(request,'blog/post/detail.html',{'post':post})
