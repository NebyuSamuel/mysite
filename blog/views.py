from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .models import Post,Comment
from .forms import EmailPostForm,CommentForm
# Create your views here.

# retrieve all pulished posts
def post_list(request):
    object_lst = Post.published.all()
    paginator = Paginator(object_lst,2) # 2 posts per page
    page = request.GET.get('page') # get the current page
    try:
        posts = paginator.page(page) # try to display the current page
    except PageNotAnInteger:
        posts = paginator.page(1) # If the page number is not an integer or below page range
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'blog/post/list.html',{'page':page,'posts':posts})

#retrieve a single published post
def post_detail(request,post_id,year,month,day,slug_name):
    post =  get_object_or_404(Post, pk = post_id,status = 'published', publish__year = year, publish__month = month, publish__day = day, slug = slug_name)

    # list of active comments using "comments" as a model manager rather than a specific
    # model manager for Comment model
    comments = post.comments.filter(active = True)

    new_comment = None

    # check whether there is a POST request or not
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)

        # check for validation
        if comment_form.is_valid():
            # create a new comment object but not yet saved to the DB
            new_comment = comment_form.save(commit = False)
            # assign the current post to the comment
            new_comment.post = post
            # save the comment
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,'blog/post/detail.html',{'post':post,
    'comments':comments,'new_comment':new_comment,'comment_form':comment_form})

#view for email post form
def post_share(request,post_id):
    post = get_object_or_404(Post, pk = post_id, status = 'published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url} \n\n {cd['name']} comments : {cd['comments']}"
            send_mail(subject,message,cd['email'],[cd['to']])
    else :
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})