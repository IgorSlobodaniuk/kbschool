# -*- coding: utf-8 -*-
from django.conf.urls.static import  static
from django.conf.urls import patterns, include, url
from schoolsite import views
#from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.views.generic import RedirectView
#dajaxice_autodiscover()
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'edusite.views.home', name='home'),
    # url(r'^edusite/', include('edusite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='/index/')),
    url(r'^index/$', views.index_page),
    url(r'^login/$', views.admin_login),
    url(r'^logout/$', views.user_logout),
    url(r'^news/$', views.news_page),
    url(r'^news_full/$', views.news_full_page),
    url(r'^add_news/$', views.add_news),
    url(r'^del_news/$', views.del_news),
    url(r'^news_(\d{10})/$', views.news_item),
    url(r'^add_news_image(\d{10})/$', views.news_item_add_photos),
    url(r'^add_news_image_from_net(\d{10})/$', views.news_item_add_photos_from_net),
    url(r'^del_news_image(\d{10})/$', views.news_item_del_photos),
    url(r'^photogallery/$', views.photogallery_page),
    url(r'^videogallery/$', views.videogallery_page),
    url(r'^add_video/$', views.add_video),
    url(r'^del_video/$', views.del_video),
    url(r'^team/$', views.team_start_page),
    url(r'^team/kaf=(.+)/$', views.team_page),
    url(r'^history/$', views.history_page),
    url(r'^images_for_photogallery/$', views.images_for_photogallery_page),
    url(r'^images_for_admins/$', views.images_for_admins_page),
    url(r'^images_for_news/$', views.images_for_news_page),
    url(r'^images_for_banner/$', views.images_for_banner_page),
    url(r'^add_admins_photo/$', views.add_admins_photo),
    url(r'^del_admins_photo/$', views.del_admins_photo),
    url(r'^add_team_photo/$', views.add_team_photo),
    url(r'^del_team_photo/$', views.del_team_photo),
    url(r'^add_banner_photo/$', views.add_banner_photo),
    url(r'^del_banner_photo/$', views.del_banner_photo),
    url(r'^images_for_team/$', views.images_for_team_page),
    url(r'^add_images_dir/$', views.add_images_dir),
    url(r'^add_images_from_net_dir/$', views.add_images_from_net_dir),
    url(r'^del_images_dir/$', views.del_images_dir),
    url(r'^poster/$', views.poster_page),
    url(r'^add_poster/$', views.add_poster),
    url(r'^del_poster/$', views.del_poster),
    url(r'^schedule/$', views.schedule_start_page),
    url(r'^schedule_add/$', views.schedule_add),
    url(r'^schedule_del/$', views.schedule_del),
    url(r'^schedule_add_forms/$', views.schedule_add_forms),
    url(r'^schedule_del_forms/$', views.schedule_del_forms),
    url(r'^schedule_del_forms_all/$', views.schedule_del_forms_all),
    url(r'^schedule_del_all/$', views.schedule_del_all),
    url(r'^team_add_members/$', views.team_add_members),
    url(r'^team_del_members/$', views.team_del_members),
    url(r'^admins/$', views.admins_page),
    url(r'^admins_add_members/$', views.admins_add_members),
    url(r'^admins_del_members/$', views.admins_del_members), 
    url(ur'^schedule/form=([5-9]|10|11|12)-?([АБВГ])?/$', views.schedule_page),
    url(r'^tutorials/$', views.tutorials_page),
    url(r'^add_tutorial/$', views.add_tutorial),
    url(r'^del_tutorial/$', views.del_tutorial),
    url(r'^presentation/$', views.presentation_page),
    url(r'^add_presentation/$', views.add_presentation),
    url(r'^del_presentation/$', views.del_presentation),
    url(r'^useful_links/$', views.useful_links_page),
    url(r'^add_link/$', views.add_link),
    url(r'^del_link/$', views.del_link),



    #url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
