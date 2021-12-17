# CALL THIS WHATEVER
# IT MAKES AUXILARY FUNCTIONS TO BE CALLED IN OTEHR PLACES
# MAINLY VIEWS
from .models import Profile, Interests
from django.db.models import Q

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProfiles(request):
    search_query = request.GET.get('search_query') or ""
    interests = Interests.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(interests__in=interests)
    )
    return profiles, search_query


def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    # First time
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    # Page=1000000
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    page_multiplier = int(page)//5

    left_index, right_index = min(
        5*page_multiplier+1, int(page)), min(5*page_multiplier+6, int(paginator.num_pages)+1)

    custom_range = range(left_index, right_index)

    return profiles, custom_range, paginator
