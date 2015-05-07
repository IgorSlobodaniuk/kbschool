from menu_processor import navigation_menu
from django.template import RequestContext
from schoolsite.queries import get_guests_count
from schoolsite.queries import get_news_title_and_date
from schoolsite.date_processor import get_curent_day
from django.core.context_processors import csrf
from forms import *


def add_user_info_and_menu(view):
    def wrapper(request, *args, **kwargs):
        context = navigation_menu(request)
        context['path'] = RequestContext(request)
        context['title_and_date'] = get_news_title_and_date()
        curent_holiday = get_curent_day()
        context['curent_holiday'] = curent_holiday
        lform = LoginForm()
        context['lform'] = lform
        context.update(csrf(request))
        args += (context,)
        if request.user.is_superuser:
        	context['aunt'] = True
        else:
        	context['aunt'] = False
        return view(request, *args, **kwargs)
    return wrapper

