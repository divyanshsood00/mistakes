# Searching
from .models import Blog, Tag
from django.db.models import Q
# Paginating
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchBlogs(request):
    search_query = request.GET.get('search_query') or ""
    # A bug here, Doesn't work with some author searches *_*
    tags = Tag.objects.filter(name__icontains=search_query)
    blogs = Blog.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(author__name__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(tags__in=tags)
    )

    return blogs, search_query


def paginateBlogs(request, blogs, results):
    page = request.GET.get('page')
    paginator = Paginator(blogs, results)

    try:
        blogs = paginator.page(page)
    # First time
    except PageNotAnInteger:
        page = 1
        blogs = paginator.page(page)
    # Page=1000000
    except EmptyPage:
        page = paginator.num_pages
        blogs = paginator.page(page)
    page_multiplier = int(page)//5

    left_index, right_index = min(
        5*page_multiplier+1, int(page)), min(5*page_multiplier+6, int(paginator.num_pages)+1)

    custom_range = range(left_index, right_index)

    return blogs, custom_range, paginator
