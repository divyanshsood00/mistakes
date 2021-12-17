from django.contrib import messages
from django.shortcuts import redirect, render
from blogs.forms import BlogForm, ReviewForm
from django.contrib.auth.decorators import login_required
from blogs.models import Blog, Tag
from blogs.utils import paginateBlogs, searchBlogs


def blog(request, pk):
    blog = Blog.objects.get(id=pk)
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.blog = blog
            review.author = request.user.profile
            try:
                review.save()
                blog.getVoteCount
                messages.success(
                    request, "Yeah, added your valuable advice :))")
                return redirect('blog', pk=blog.id)

            except:
                messages.error(request, "You can give only give one review")
        else:
            messages.error(request, "Something went wrong, Try Again")
        # update project vote count

    props = {'blog': blog, 'form': form}
    return render(request, 'blogs/blog.html', props)


def blogs(request):
    # Searching
    blogs, search_query = searchBlogs(request)
    # Pagination
    results = 3
    blogs, custom_range, paginator = paginateBlogs(request, blogs, results)

    props = {'blogs': blogs, 'search_query': search_query,
             'custom_range': custom_range}
    # passing object to html
    return render(request, 'blogs/blogs.html', props)


@login_required(login_url="login")
def createBlog(request):
    profile = request.user.profile
    form = BlogForm()
    if request.method == 'POST':
        # Request.FILES added for images later onnn also check html of blog-form, settings.py.tail
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = profile
            # newtags = request.POST.get('newtags')
            # if newtags:
            #     newtags = newtags.split(',')
            # for tag in newtags:
            #     try:
            #         ntag = Tag.objects.get(
            #             name=tag.strip().capitalize())
            #     except:
            #         ntag = Tag.objects.create(
            #             name=tag.strip().capitalize())
            #     blog.tags.add(ntag)
            blog.save()
            messages.success(request, "Mistake Created")
            return redirect('account')
        else:
            messages.error(
                request, "An eRRor occured while processing your request")
    props = {'form': form}
    return render(request, 'blogs/blog_form.html', props)


@login_required(login_url="login")
def updateBlog(request, pk):
    profile = request.user.profile
    blog = profile.blog_set.get(id=pk)
    form = BlogForm(instance=blog)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            # blog.tags = [tag.lower() for tag in blog.tags]
            newtags = request.POST.get('newtags').split(',')
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(
                    name=tag.strip().capitalize())
                blog.tags.add(tag)

            blog.save()
            messages.success(request, "Wallah Habibi, Mistake Updated")
            return redirect('account')
        else:
            messages.error(
                request, "An eRRor occured while processing your request")

    props = {'form': form, 'blog': blog}
    return render(request, 'blogs/blog_form.html', props)


@login_required(login_url="login")
def deleteBlog(request, pk):
    profile = request.user.profile
    blog = profile.blog_set.get(id=pk)
    if request.method == 'POST':
        if blog:
            blog.delete()
            messages.success(request, "Mistake is No More :'(")
        else:
            messages.error(
                request, "An eRRor occured while processing your request")
        return redirect('account')

    return render(request, 'blogs/delete_obj.html', {'name': blog.title})
