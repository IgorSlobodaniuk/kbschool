# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout 
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from schoolsite.queries import *
from schoolsite.image_processor import *
from schoolsite.date_processor import *
from django.contrib.auth.decorators import login_required
from decorators import add_user_info_and_menu
from forms import *
import re


def admin_login(request):
	lform = LoginForm(request.POST)
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return HttpResponseRedirect('/index/')
		else:
			msg = '*Неправильний логін або пароль'
			return HttpResponse(msg)
	else:
		msg = '*Неправильний логін або пароль'
		return HttpResponse(msg)



def user_logout(request):
    '''User logout.'''
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/index/')


@add_user_info_and_menu
def index_page(request, *args):
	context = args[0]
	directory = 'edusite/media/images/banner_photo/'
	banner_photos = get_all_banner_photo(directory)
	context['banner_photos'] = banner_photos
	context['banner'] = 'yes'
	return render_to_response('index.html', context)


@add_user_info_and_menu
def news_page(request, *args):
	context = args[0]
	data = get_all_news_data()
	context['data'] = data
	if request.user.is_superuser:
		addform = AddNewsForm()
		delform = DelNewsForm()
		data = get_all_news_data()
		context['addform'] = addform
		context['delform'] = delform
		context['data'] = data
		context.update(csrf(request))
		return render_to_response('news_dir.html', context)
	else:
		return render_to_response('news.html', context)



@add_user_info_and_menu
def news_full_page(request, *args):
	context = args[0]
	return render_to_response('news_item_full.html', context)

def add_news(request):
	if request.method == 'POST':
		addform = AddNewsForm(request.POST, request.FILES)
		if addform.is_valid():
			title = addform.cleaned_data['title']
			content = addform.cleaned_data['content_field']
			side_picture = request.FILES['side_picture_field']
			side_picture_name = request.FILES['side_picture_field'].name
			side_picture_path = '/media/images/for_news/news_side_picture/' + side_picture_name
			save_news_side_picture(side_picture, side_picture_name)
			res = add_news_it(title, side_picture_path, content)
			if res:
				msg = u'*Публікацію' + ' "' + title + '" ' + u'додано'
				return render_to_response('green_message.html', {'msg': msg})
			else:
				msg = u'*Публікацію' + ' "' + title + '" ' + u'не вдалося додати'
				return render_to_response('red_message.html', {'msg': msg})
		else:
			msg = u"*Потрібно заповнити всі поля"
			return render_to_response('red_message.html', {'msg': msg})


def del_news(request):
	if request.method == 'POST':
		delform = DelNewsForm(request.POST)
		if delform.is_valid():
			code = delform.cleaned_data['code']
			del_news_it(code)
			msg = u'*Публікацію' + ' "' + code + '" ' + u'видалено'
			return render_to_response('green_message.html', {'msg': msg})


@add_user_info_and_menu
def news_item(request, code, *args):
	context = args[0]
	if request.user.is_superuser:
		addform = UploadImageForm()
		addfromnetform = UploadImageFromNetForm()
		delform = DelImageForm()
		context['addform'] = addform
		context['addfromnetform'] = addfromnetform
		context['delform'] = delform
		context['code_url'] = 'add_news_image' + code
		context['code_url_net'] = 'add_news_image_from_net' + code
		context['code_url_del'] = 'del_news_image' + code
		data = get_news_item_data(code)
		context['data'] = data
		context['super'] = 'yes'
		photos = get_all_news_photos(code)
		all_imgs = []
		for i in photos:
			all_imgs.append('/media/images/for_news/' + code + '/' + i)
		context['photos'] = all_imgs
		context.update(csrf(request))
		return render_to_response('news_item_full.html', context)
	else:
		data = get_news_item_data(code)
		photos = get_all_news_photos(code)
		directory = '/media/images/for_news/' + code + '/'
		imgsPath = []
		for image in photos:
			imgsPath.append(directory + image)
		context['data'] = data
		context['photos'] = imgsPath
		return render_to_response('news_item_full.html', context)




@add_user_info_and_menu
def news_item_add_photos(request, code, *args):
	context = args[0]
	addform = UploadImageForm()
	addfromnetform = UploadImageFromNetForm()
	delform = DelImageForm()
	context['addform'] = addform
	context['addfromnetform'] = addfromnetform
	context['delform'] = delform	
	context['code_url'] = 'add_news_image' + code
	context['code_url_net'] = 'add_news_image_from_net' + code
	context['code_url_del'] = 'del_news_image' + code
	context.update(csrf(request))
	if request.method == 'POST':
		addform = UploadImageForm(request.POST, request.FILES)
        if addform.is_valid():
        	image_title = addform.cleaned_data['title'].replace(' ', '_')
        	image = request.FILES['image']
        	if not image_title:
        		image_title = image.name
        	add_news_images(request.FILES['image'], image_title, code)
        	msg_add = u'*Зображення' + ' "'+ image_title +'" ' +u'додано'
        	context['msg_add'] = msg_add
        	data = get_news_item_data(code)
        	photos = get_all_news_photos(code)
        	all_imgs = []
        	for i in photos:
        		all_imgs.append("/media/images/for_news/" + code + '/' + i)

        	directory = '/media/images/for_news/' + code + '/'
        	imgsPath = []
        	for image in photos:
        		imgsPath.append(directory + image)
        	context['photos'] = imgsPath
        	context['data'] = data
        	return render_to_response('images_for_news_dir.html', context)
        else:
        	msg_add  = u'*Зображення не вибране або має неправильний тип'
        	return HttpResponse(msg_add)



@add_user_info_and_menu
def news_item_add_photos_from_net(request, code, *args):
	context = args[0]
	addform = UploadImageForm()
	addfromnetform = UploadImageFromNetForm()
	delform = DelImageForm()
	context['addform'] = addform
	context['addfromnetform'] = addfromnetform
	context['delform'] = delform	
	context['code_url'] = 'add_news_image' + code
	context['code_url_net'] = 'add_news_image_from_net' + code
	context['code_url_del'] = 'del_news_image' + code
	context.update(csrf(request))
	if request.method == 'POST':
		addfromnetform = UploadImageFromNetForm(request.POST)
        if addfromnetform.is_valid():
        	image_title = addfromnetform.cleaned_data['title'].replace(' ', '_')
        	link = addfromnetform.cleaned_data['image_link']
        	s = link.rfind('/') + 1
        	d = link.rfind('.')
        	img_title = link[s:d]
        	if not image_title:
        		image_title = img_title
        	img = get_news_img_from_net(link, image_title, code)
        	if not img:
        		msg_add2 = u'*Неможливо відкрити URL'
        		context['msg_add2'] = msg_add2
        		return HttpResponse(msg_add2)
        	else:
        		msg_add2 = u'*Зображення ' + '"'+ image_title +'"'+ u' додано'
        		context['msg_add2'] = msg_add2
        		data = get_news_item_data(code)
        		photos = get_all_news_photos(code)
        		all_imgs = []
        		for i in photos:
        			all_imgs.append("/media/images/for_news/" + code + '/' + i)
        		context['photos'] = all_imgs
        		directory = '/media/images/for_news/' + code + '/'
        		imgsPath = []
        		for image in photos:
        			imgsPath.append(directory + image)
        		return render_to_response('images_for_news_dir.html', context)
        else:
        	msg_add2 = u'*Не вказаний або неправильний URL'
        	return HttpResponse(msg_add2)



@add_user_info_and_menu
def news_item_del_photos(request, code, *args):
	context = args[0]
	addform = UploadImageForm()
	addfromnetform = UploadImageFromNetForm()
	delform = DelImageForm()
	context['addform'] = addform
	context['addfromnetform'] = addfromnetform
	context['delform'] = delform	
	context['code_url'] = 'add_news_image' + code
	context['code_url_net'] = 'add_news_image_from_net' + code
	context['code_url_del'] = 'del_news_image' + code
	context.update(csrf(request))
	if request.method == 'POST':
		delForm = DelImageForm(request.POST)
        if delForm.is_valid():
        	image_for_del = request.POST.getlist('checkb_for_del')
        	image_names = []
        	for i in image_for_del:
        		s = i.rfind('/') + 1
        		image_names.append(i[s:])
        	if not image_names:
        		msg = u'*Не вибрано жодного зображення'
        		return HttpResponse(msg)
        	res = del_news_images(image_names, code)
        	if not res:
        		msg = u"*Неможливо видалити зображення"
        		return HttpResponse(msg)
        	else:
        		data = get_news_item_data(code)
        		photos = get_all_news_photos(code)
        		all_imgs = []
        		for i in photos:
        			all_imgs.append("/media/images/for_news/" + code + '/' + i)
        		directory = '/media/images/for_news/' + code + '/'
        		imgsPath = []
        		for image in photos:
        			imgsPath.append(directory + image)
        		context['all_imgs'] = all_imgs
        		context['photos'] = imgsPath
        		context['data'] = data
        		img_str = u''
        		for im in image_names:
        			img_str += im + u', '
        		img_str = img_str[:-2]
        		msg = u'*Зображення ' + '"' + img_str + '"' + u' видалено'
        		context['msg'] = msg
        		return render_to_response('images_for_news_dir.html', context)




@add_user_info_and_menu
def history_page(request, *args):
	context = args[0]
	data = 'hello'
	return render_to_response('history.html', context)


@add_user_info_and_menu
def photogallery_page(request, *args):
	context = args[0]
	img_link_min = []
	img_link_max = []
	img_title = []
	images = get_all_img()
	for img in images:
		img_min = "/media/images/min/" + img[:-4] + "_min.jpg"
		img_max = "/media/images/max/" + img[:-4] + "_max.jpg"
		img_link_min.append(img_min)
		img_link_max.append(img_max)
		img_title.append(img[:-4])
	img_link = zip(img_link_min, img_link_max, img_title)
	context['img_link'] = img_link
	return render_to_response('photogallery.html', context)


@add_user_info_and_menu
def videogallery_page(request, *args):
	context = args[0]
	if request.user.is_superuser:
		addform = AddVideoForm()
		delform = DelVideoForm()
		context['addform'] = addform
		context['delform'] = delform
		videos = get_all_videos()
		context['videos'] = videos
		context.update(csrf(request))
		return render_to_response('videogallery_dir.html', context)
	else:
		videos = get_all_videos()
		context['videos'] = videos
		return render_to_response('videogallery.html', context)


def add_video(request, *args):
	if request.method == 'POST':
		addform = AddVideoForm(request.POST)
		if addform.is_valid():
			video_name = addform.cleaned_data['title']
			video_link = addform.cleaned_data['video_link']
			if not video_name:
				video_name = u'Відео'
			res = add_video_to_database(video_name, video_link)
			if res:
				msg = u'*Відео' + ' "' + video_name + '" ' + u'додано'
				return render_to_response('green_message.html', {'msg': msg})
			else:
				msg = u'*Відео' + ' "' + video_name + '" ' + u'не вдалося додати'
				return render_to_response('red_message.html', {'msg': msg})
		else:
			msg = u'Неправильний або порожній URL'
			return render_to_response('red_message.html', {'msg': msg})


def del_video(request, *args):
	if request.method == 'POST':
		delform = DelVideoForm(request.POST)
		if delform.is_valid():
			video_name = delform.cleaned_data['video_name_field']
			res = del_video_from_database(video_name)
			if res:
				msg = u'*Відео' + ' "' + video_name + '" ' + u'видалено'
				return render_to_response('green_message.html', {'msg': msg})
			else:
				msg = u'*Відео' + ' "' + video_name + '" ' + u'не вдалося видалити'
				return render_to_response('red_message.html', {'msg': msg})


@add_user_info_and_menu
def images_for_photogallery_page(request, *args):
	context = args[0]
	if request.user.is_superuser:
		addform = UploadImageForm()
		addfromnetform = UploadImageFromNetForm()
		delform = DelImageForm()
		context['addform'] = addform
		context['addfromnetform'] = addfromnetform
		context['delform'] = delform
		all_images = get_all_img()
		all_imgs = []
		for i in all_images:
			all_imgs.append("/media/images/min/" + i[:-4] + "_min.jpg")
		context['all_imgs'] = all_imgs
		context.update(csrf(request))
		return render_to_response('images_for_photogallery.html', context)
	else:
		return HttpResponseRedirect('/index/')


@add_user_info_and_menu
def add_images_dir(request, *args):
	context = args[0]
	addform = UploadImageForm()
	addfromnetform = UploadImageFromNetForm()
	delform = DelImageForm()
	context['addform'] = addform
	context['addfromnetform'] = addfromnetform
	context['delform'] = delform
	context.update(csrf(request))
	if request.method == 'POST':
		addform = UploadImageForm(request.POST, request.FILES)
        if addform.is_valid():
        	image_title = addform.cleaned_data['title'].replace(' ', '_')
        	image = request.FILES['image']
        	if not image_title:
        		image_title = image.name.replace(' ', '_')
        		d = image_title.index('.')
        		image_title = image_title[:d]
        	handle_uploaded_file(request.FILES['image'], image_title)
        	msg_add = u'*Зображення' + ' "'+ image_title +'" ' +u'додано'
        	context['msg_add'] = msg_add
        	all_images = get_all_img()
        	all_imgs = []
        	for i in all_images:
        		all_imgs.append("/media/images/min/" + i[:-4] + "_min.jpg")
        		context['all_imgs'] = all_imgs
        	return render_to_response('images_for_photogallery_dir.html', context)
        else:
        	msg_add  = u'*Зображення не вибране або має неправильний тип'
        	return HttpResponse(msg_add)


@add_user_info_and_menu
def add_images_from_net_dir(request, *args):
	context = args[0]
	addform = UploadImageForm()
	addfromnetform = UploadImageFromNetForm()
	delform = DelImageForm()
	context['addform'] = addform
	context['addfromnetform'] = addfromnetform
	context['delform'] = delform
	context.update(csrf(request))
	if request.method == 'POST':
		addfromnetform = UploadImageFromNetForm(request.POST)
        if addfromnetform.is_valid():
        	image_title = addfromnetform.cleaned_data['title'].replace(' ', '_')
        	link = addfromnetform.cleaned_data['image_link']
        	s = link.rfind('/') + 1
        	d = link.rfind('.')
        	img_title = link[s:d]
        	if not image_title:
        		image_title = img_title
        	img = get_img_from_net(link, image_title)
        	if not img:
        		msg_add2 = u'*Неможливо відкрити URL'
        		context['msg_add2'] = msg_add2
        		return HttpResponse(msg_add2)
        	else:
        		msg_add2 = u'*Зображення ' + '"'+ img_title +'"'+ u' додано'
        		context['msg_add2'] = msg_add2
        		all_images = get_all_img()
        		all_imgs = []
        		for i in all_images:
        			all_imgs.append("/media/images/min/" + i[:-4] + "_min.jpg")
        		context['all_imgs'] = all_imgs
        		return render_to_response('images_for_photogallery_dir.html', context)
        else:
        	msg_add2 = u'*Не вказаний або неправильний URL'
           	return HttpResponse(msg_add2)



@add_user_info_and_menu
def del_images_dir(request, *args):
	context = args[0]
	addform = UploadImageForm()
	addfromnetform = UploadImageFromNetForm()
	delform = DelImageForm()
	context['addform'] = addform
	context['addfromnetform'] = addfromnetform
	context['delform'] = delform
	all_images = get_all_img()
	all_imgs = []
	for i in all_images:
		all_imgs.append("/media/images/min/" + i[:-4] + "_min.jpg")
		context['all_imgs'] = all_imgs
		context.update(csrf(request))
	if request.method == 'POST':
		delForm = DelImageForm(request.POST)
        if delForm.is_valid():
        	image_for_del = request.POST.getlist('checkb_for_del')
        	image_names = []
        	for i in image_for_del:
        		s = i.rfind('/') + 1
        		d = i.rfind('.') - 4
        		image_names.append(i[s:d])
        	if not image_names:
        		msg = u'*Не вибрано жодного зображення'
        		return HttpResponse(msg)
        	res = del_images(image_names)
        	if not res:
        		msg = u"*Неможливо видалити зображення"
        		return HttpResponse(msg)
        	else:
        		all_images = get_all_img()
        		all_imgs = []
        		for i in all_images:
        			all_imgs.append("/media/images/min/" + i[:-4] + "_min.jpg")
        			context['all_imgs'] = all_imgs
        		img_str = u''
        		for im in image_names:
        			img_str += im + u', '
        		img_str = img_str[:-2]
        		msg = u'*Зображення ' + '"' + img_str + '"' + u' видалено'
        		context['msg'] = msg
        		return render_to_response('images_for_photogallery_dir.html', context)



@add_user_info_and_menu
def images_for_admins_page(request, *args):
	context = args[0]
	if request.user.is_superuser:
		addform = UploadImageForm()
		delform = DelImageForm()
		context['addform'] = addform
		context['delform'] = delform
		directory = 'edusite/media/images/admins_photo/'
		all_photo = get_all_photo(directory)
		all_imgs = []
		for i in all_photo:
			all_imgs.append("/media/images/admins_photo/" + i)
		context['all_imgs'] = all_imgs
		context.update(csrf(request))
		return render_to_response('images_for_admins.html', context)
	else:
		return HttpResponseRedirect('/index/')



@add_user_info_and_menu
def add_admins_photo(request, *args):
	context = args[0]
	addform = UploadImageForm()
	delform = DelImageForm()
	context['addform'] = addform
	context['delform'] = delform
	context.update(csrf(request))
	if request.method == 'POST':
		addform = UploadImageForm(request.POST, request.FILES)
        if addform.is_valid():
        	photo_title = addform.cleaned_data['title'].replace(' ', '_')
        	photo = request.FILES['image']
        	if not photo_title:
        		photo_title = photo.name.replace(' ', '_')
        		d = photo_title.index('.')
        		photo_title = photo_title[:d]
        	directory = 'edusite/media/images/admins_photo/'
        	add_photo(request.FILES['image'], photo_title, directory)
        	msg_add = u'*Фото' + ' "'+ photo_title +'" ' +u'додано'
        	context['msg_add'] = msg_add
        	all_photo = get_all_photo(directory)
        	all_imgs = []
        	for i in all_photo:
        		all_imgs.append("/media/images/admins_photo/" + i)
        		context['all_imgs'] = all_imgs
        	return render_to_response('images_for_admins_dir.html', context)
        else:
        	msg_add  = u'*Фото не вибране або має неправильний тип'
        	return HttpResponse(msg_add)



@add_user_info_and_menu
def del_admins_photo(request, *args):
	context = args[0]
	addform = UploadImageForm()
	delform = DelImageForm()
	context['addform'] = addform
	context['delform'] = delform
	directory = 'edusite/media/images/admins_photo/'
	all_photo = get_all_photo(directory)
	all_imgs = []
	for i in all_photo:
		all_imgs.append("/media/images/admins_photo/" + i)
		context['all_imgs'] = all_imgs
		context.update(csrf(request))
	if request.method == 'POST':
		delForm = DelImageForm(request.POST)
        if delForm.is_valid():
        	photo_for_del = request.POST.getlist('checkb_for_del')
        	photo_names = []
        	for i in photo_for_del:
        		s = i.rfind('/') + 1
        		photo_names.append(i[s:])
        	if not photo_names:
        		msg = u'*Не вибрано жодного фото'
        		return HttpResponse(msg)
        	res = del_photo(photo_names, directory)
        	if not res:
        		msg = u"*Неможливо видалити фото"
        		return HttpResponse(msg)
        	else:
        		all_photos = get_all_photo(directory)
        		all_imgs = []
        		for i in all_photos:
        			all_imgs.append("/media/images/admins_photo/" + i)
        			context['all_imgs'] = all_imgs
        		img_str = u''
        		for im in photo_names:
        			img_str += im + u', '
        		img_str = img_str[:-2]
        		msg = u'*Фото ' + '"' + img_str + '"' + u' видалено'
        		context['msg'] = msg
        		return render_to_response('images_for_admins_dir.html', context)



@add_user_info_and_menu
def images_for_team_page(request, *args):
	context = args[0]
	if request.user.is_superuser:
		addform = UploadImageForm()	
		delform = DelImageForm()
		context['addform'] = addform
		context['delform'] = delform
		directory = 'edusite/media/images/team_photo/'
		all_photo = get_all_photo(directory)
		all_imgs = []
		for i in all_photo:
			all_imgs.append("/media/images/team_photo/" + i)
		context['all_imgs'] = all_imgs
		context.update(csrf(request))
		return render_to_response('images_for_team.html', context)
	else:
		return HttpResponseRedirect('/index/')


@add_user_info_and_menu
def add_team_photo(request, *args):
	context = args[0]
	addform = UploadImageForm()
	delform = DelImageForm()
	context['addform'] = addform
	context['delform'] = delform
	context.update(csrf(request))
	if request.method == 'POST':
		addform = UploadImageForm(request.POST, request.FILES)
        if addform.is_valid():
        	photo_title = addform.cleaned_data['title'].replace(' ', '_')
        	photo = request.FILES['image']
        	if not photo_title:
        		photo_title = photo.name.replace(' ', '_')
        		d = photo_title.index('.')
        		photo_title = photo_title[:d]
        	directory = 'edusite/media/images/team_photo/'
        	add_photo(request.FILES['image'], photo_title, directory)
        	msg_add = u'*Фото' + ' "'+ photo_title +'" ' +u'додано'
        	context['msg_add'] = msg_add
        	all_photo = get_all_photo(directory)
        	all_imgs = []
        	for i in all_photo:
        		all_imgs.append("/media/images/team_photo/" + i)
        		context['all_imgs'] = all_imgs
        	return render_to_response('images_for_team_dir.html', context)
        else:
        	msg_add  = u'*Фото не вибране або має неправильний тип'
        	return HttpResponse(msg_add)



@add_user_info_and_menu
def del_team_photo(request, *args):
	context = args[0]
	addform = UploadImageForm()
	delform = DelImageForm()
	context['addform'] = addform
	context['delform'] = delform
	directory = 'edusite/media/images/team_photo/'
	all_photo = get_all_photo(directory)
	all_imgs = []
	for i in all_photo:
		all_imgs.append("/media/images/team_photo/" + i)
		context['all_imgs'] = all_imgs
		context.update(csrf(request))
	if request.method == 'POST':
		delForm = DelImageForm(request.POST)
        if delForm.is_valid():
        	photo_for_del = request.POST.getlist('checkb_for_del')
        	photo_names = []
        	for i in photo_for_del:
        		s = i.rfind('/') + 1
        		photo_names.append(i[s:])
        	if not photo_names:
        		msg = u'*Не вибрано жодного фото'
        		return HttpResponse(msg)
        	res = del_photo(photo_names, directory)
        	if not res:
        		msg = u"*Неможливо видалити фото"
        		return HttpResponse(msg)
        	else:
        		all_photos = get_all_photo(directory)
        		all_imgs = []
        		for i in all_photos:
        			all_imgs.append("/media/images/team_photo/" + i)
        			context['all_imgs'] = all_imgs
        		img_str = u''
        		for im in photo_names:
        			img_str += im + u', '
        		img_str = img_str[:-2]
        		msg = u'*Фото ' + '"' + img_str + '"' + u' видалено'
        		context['msg'] = msg
        		return render_to_response('images_for_team_dir.html', context)


@add_user_info_and_menu
def images_for_banner_page(request, *args):
	context = args[0]
	if request.user.is_superuser:
		addform = UploadImageForm()	
		delform = DelImageForm()
		context['addform'] = addform
		context['delform'] = delform
		directory = 'edusite/media/images/banner_photo/'
		all_photo = get_all_photo(directory)
		all_imgs = []
		for i in all_photo:
			all_imgs.append("/media/images/banner_photo/" + i)
		context['all_imgs'] = all_imgs
		context.update(csrf(request))
		return render_to_response('images_for_banner.html', context)
	else:
		return HttpResponseRedirect('/index/')


@add_user_info_and_menu
def add_banner_photo(request, *args):
	context = args[0]
	addform = UploadImageForm()
	delform = DelImageForm()
	context['addform'] = addform
	context['delform'] = delform
	context.update(csrf(request))
	if request.method == 'POST':
		addform = UploadImageForm(request.POST, request.FILES)
        if addform.is_valid():
        	photo_title = addform.cleaned_data['title'].replace(' ', '_')
        	photo = request.FILES['image']
        	if not photo_title:
        		photo_title = photo.name.replace(' ', '_')
        		d = photo_title.index('.')
        		photo_title = photo_title[:d]
        	directory = 'edusite/media/images/banner_photo/'
        	add_banner_image(request.FILES['image'], photo_title, directory)
        	msg_add = u'*Фото' + ' "'+ photo_title +'" ' +u'додано'
        	context['msg_add'] = msg_add
        	all_photo = get_all_photo(directory)
        	all_imgs = []
        	for i in all_photo:
        		all_imgs.append("/media/images/banner_photo/" + i)
        		context['all_imgs'] = all_imgs
        	return render_to_response('images_for_banner_dir.html', context)
        else:
        	msg_add  = u'*Фото не вибране або має неправильний тип'
        	return HttpResponse(msg_add)



@add_user_info_and_menu
def del_banner_photo(request, *args):
	context = args[0]
	addform = UploadImageForm()
	delform = DelImageForm()
	context['addform'] = addform
	context['delform'] = delform
	directory = 'edusite/media/images/banner_photo/'
	all_photo = get_all_photo(directory)
	all_imgs = []
	for i in all_photo:
		all_imgs.append("/media/images/banner_photo/" + i)
		context['all_imgs'] = all_imgs
		context.update(csrf(request))
	if request.method == 'POST':
		delForm = DelImageForm(request.POST)
        if delForm.is_valid():
        	photo_for_del = request.POST.getlist('checkb_for_del')
        	photo_names = []
        	for i in photo_for_del:
        		s = i.rfind('/') + 1
        		photo_names.append(i[s:])
        	if not photo_names:
        		msg = u'*Не вибрано жодного фото'
        		return HttpResponse(msg)
        	res = del_photo(photo_names, directory)
        	if not res:
        		msg = u"*Неможливо видалити фото"
        		return HttpResponse(msg)
        	else:
        		all_photos = get_all_photo(directory)
        		all_imgs = []
        		for i in all_photos:
        			all_imgs.append("/media/images/banner_photo/" + i)
        			context['all_imgs'] = all_imgs
        		img_str = u''
        		for im in photo_names:
        			img_str += im + u', '
        		img_str = img_str[:-2]
        		msg = u'*Фото ' + '"' + img_str + '"' + u' видалено'
        		context['msg'] = msg
        		return render_to_response('images_for_banner_dir.html', context)

@add_user_info_and_menu
def poster_page(request, *args):
	context = args[0]
	if request.user.is_superuser:
		addform = UploadImageForm()	
		context['addform'] = addform
		poster_img = '/media/images/poster/poster_min.jpg'
		poster_exs = poster_exists()
		if poster_exs:
			context['posterimg'] = poster_img
		context.update(csrf(request))
		return render_to_response('image_for_poster.html', context)
	else:
		return HttpResponseRedirect('/index/')


@add_user_info_and_menu
def add_poster(request, *args):
	context = args[0]
	addform = UploadImageForm()
	context['addform'] = addform
	poster_img = '/media/images/poster/poster_min.jpg'
	context.update(csrf(request))
	if request.method == 'POST':
		addform = UploadImageForm(request.POST, request.FILES)
        if addform.is_valid():
        	photo = request.FILES['image']
        	add_new_poster(request.FILES['image'])
        	poster_exs = poster_exists()
        	if poster_exs:
        		context['posterimg'] = poster_img
        	msg_add = u'*Афішу додано'
        	context['msg_add'] = msg_add
        	return render_to_response('image_for_poster_dir.html', context)
        else:
        	msg_add  = u'*Зображення не вибране або має неправильний тип'
        	return HttpResponse(msg_add)


@add_user_info_and_menu
def del_poster(request, *args):
	context = args[0]
	addform = UploadImageForm()
	context['addform'] = addform
	poster_img = '/media/images/poster/poster_min.jpg'
	context.update(csrf(request))
	if request.method == 'GET':
		poster_exs = poster_exists()
		if poster_exs:
			context['posterimg'] = poster_img
		p = del_old_poster()
		if not p:
			msg = u'*Немає даних для видалення'
			context['msg'] = msg
			return HttpResponse(msg)
		else:
			msg = u'*Афішу видалено'
			context['msg'] = msg
		return render_to_response('image_for_poster_dir.html', context)






@add_user_info_and_menu
def images_for_news_page(request, *args):
	context = args[0]
	if request.user.is_superuser:
		select_news_form = SelectNewsImagesFolderForm()
		context['select_news_form'] = select_news_form
		context.update(csrf(request))
		return render_to_response('images_for_news.html', context)
	else:
		return HttpResponseRedirect('/index/')
		


@add_user_info_and_menu
def admins_page(request, *args):
	context = args[0]
	if request.user.is_superuser:	
		form_add = AddMember()
		form_del = DelAdmin()
		context['form_add'] = form_add
		context['form_del'] = form_del
		data = get_all_admins()
		context['data'] = data
		context.update(csrf(request))
		return render_to_response('admins_dir.html', context)
	else:
		data = get_all_admins()
		context['data'] = data
		return render_to_response('admins.html', context)


@add_user_info_and_menu
def team_start_page(request, *args):
	context = args[0]
	if request.user.is_superuser:	
		form_add = AddMember()
		form_del = DelMember()
		context['form_add'] = form_add
		context['form_del'] = form_del
		
		context.update(csrf(request))
		return render_to_response('team_dir.html', context)
	else:
		context.update(csrf(request))
		return render_to_response('team.html', context)

def team_page(request, kafedra): 
	data = get_members(kafedra)
	kafedra = kafedra.replace('_', ' ')
	return render_to_response('team_for_ajax.html', {'data': data,
													'kaf': kafedra})


@add_user_info_and_menu
def schedule_start_page(request, *args):
	context = args[0]
	if request.user.is_superuser:	
		form = ChangeSchedule()
		form_del = DelSchedule()
		form_add_forms = AddForms()
		form_del_forms = DelForms()
		context['form'] = form
		context['form_del'] = form_del
		context['form_add_forms'] = form_add_forms
		context['form_del_forms'] = form_del_forms
		context['season'] = get_season()
		sf = select_forms_for_sch()
		nsf = []
		for i in sf:
			url = "loadXMLDoc2('/schedule/form=" + i  + "/'" + ")"
			nsf.append(url)
		sfl = zip(sf, nsf)
		context['forms_name'] = sfl
		context.update(csrf(request))
		return render_to_response('schedule_dir.html', context)
	else:
		sf = select_forms_for_sch()
		nsf = []
		for i in sf:
			url = "loadXMLDoc('/schedule/form=" + i  + "/'" + ")"
			nsf.append(url)
		sfl = zip(sf, nsf)
		context['forms_name'] = sfl
		context['season'] = get_season()
		return render_to_response('schedule.html', context)


def schedule_page(request, formlevel, formversion): 
	if not formversion:
		formversion = u'го'
		form = formlevel
	else:
		form = formlevel +'-'+ formversion
	monday = get_shedule(form, 'monday')
	tuesday = get_shedule(form, 'tuesday')
	wednesday = get_shedule(form, 'wednesday')
	thursday = get_shedule(form, 'thursday')
	friday = get_shedule(form, 'friday')
	season = get_season()
	season_style = 'shedule_for_' + season + '_day'
	return render_to_response('schedule _for_ajax.html', {'monday': monday,
		                                        'tuesday': tuesday, 
		                                        'wednesday': wednesday, 
		                                        'thursday': thursday, 
		                                        'friday': friday, 
		                                        "form": form,
		                                        "formlevel": formlevel,
		                                        "formversion": formversion,
		                                        "season_style": season_style,
		                                        })
    

@add_user_info_and_menu
def tutorials_page(request, *args):
	context = args[0]
	if request.user.is_superuser:
		form_add = AddTutorialsForm()
		form_del = DelTutorialsForm()
		context['form_add'] = form_add
		context['form_del'] = form_del
		data = get_all_tutorials()
		context['data'] = data
		context.update(csrf(request))
		return render_to_response('tutorials_dir.html', context)
	else:
		data = get_all_tutorials()
		context['data'] = data
		return render_to_response('tutorials.html', context)

def add_tutorial(request):
	if request.method == 'POST':
		add_form = AddTutorialsForm(request.POST, request.FILES)
		if add_form.is_valid():
			form = add_form.cleaned_data['form']
			tutorial_name = add_form.cleaned_data['tutorial_name']
			author = add_form.cleaned_data['author']
			reproduction_house = add_form.cleaned_data['reproduction_house']
			year = add_form.cleaned_data['year']
			filePDF = request.FILES['filePDF']
			fileURL = save_file(filePDF, tutorial_name)
			add_tutorials_data(tutorial_name, form, author, reproduction_house, year, fileURL)
			msg = u'*Підручник "'+  tutorial_name + u'" ' + form + u'-го класу додано'
			return render_to_response('green_message.html', {'msg': msg})
		else:
			msg = u'*Не правильно заповнені або порожні поля'
			return render_to_response('red_message.html', {'msg': msg})


def del_tutorial(request):
	if request.method == 'POST':
		del_form = DelTutorialsForm(request.POST)
		if del_form.is_valid():
			form = del_form.cleaned_data['form']
			tutorial_name = del_form.cleaned_data['tutorial_name']
			author = del_form.cleaned_data['author']
			reproduction_house = del_form.cleaned_data['reproduction_house']
			year = del_form.cleaned_data['year']
			res = del_tutorials_data(tutorial_name, form, author, reproduction_house, year)
			if res:
				msg = u'*Підручник "'+  tutorial_name + u'" ' + form + u'-го класу видалено'
				return render_to_response('green_message.html', {'msg': msg})
			else:
				msg = u'*Помилка видалення'
				return render_to_response('red_message.html', {'msg': msg})	
		else:
			msg = u'*Не правильно заповнені або порожні поля'
			return render_to_response('red_message.html', {'msg': msg})	



def schedule_add(request):
	if request.method == 'POST':
		form = ChangeSchedule(request.POST)
        if form.is_valid():
        	forms_name = form.cleaned_data['forms_name_field']
        	day = form.cleaned_data['day_field']
        	lesson_number = form.cleaned_data['lesson_number_field']
        	subject = form.cleaned_data['subject_field']
        	del_old = del_subject(forms_name, day, lesson_number)
        	if not del_old:
        		pass
        	add_subject(forms_name, day, lesson_number, subject)
        	if day == 'monday':
        		day = u'Понеділок'
        	elif day == 'tuesday':
        		day = u'Вівторок'
        	elif day == 'wednesday':
        		day = u'Середа'
        	elif day == 'thursday':
        		day = u'Четвер'
        	elif day == 'friday':
        		day = u'П’ятниця'
        	msg = u"""*Додано в росклад: клас: '%s', день: '%s', Номер уроку: '%s', 
        	           Предмет: '%s' """ %(forms_name, day, lesson_number, subject)
        	return render_to_response('green_message.html', {'msg': msg})
        else:
        	msg = u'*Введіть назву уроку'
        	return render_to_response('red_message.html', {'msg': msg})


def schedule_del(request):
	if request.method == 'POST':
		form_del = DelSchedule(request.POST)
        if form_del.is_valid():
        	forms_name = form_del.cleaned_data['forms_name_field']
        	day = form_del.cleaned_data['day_field']
        	lesson_number = form_del.cleaned_data['lesson_number_field']
        	del_old = del_subject(forms_name, day, lesson_number)
        	if day == 'monday':
        		day = u'Понеділок'
        	elif day == 'tuesday':
        		day = u'Вівторок'
        	elif day == 'wednesday':
        		day = u'Середа'
        	elif day == 'thursday':
        		day = u'Четвер'
        	elif day == 'friday':
        		day = u'П’ятниця'
        	msg = u"""*Видалено з роскладу: \n клас: '%s', день: '%s', Номер уроку: '%s'
        		   """ %(forms_name, day, lesson_number)
        	return render_to_response('green_message.html', {'msg': msg})
        	if not del_old:
        		msg = u"*Немає даних для видалення" 
        	return render_to_response('red_message.html', {'msg': msg})


def schedule_del_all(request):
	if del_all():
		msg = u'*Розклад очищено'
		return render_to_response('green_message.html', {'msg': msg})
	else:
		msg = u"*Немає даних для видалення"
		return render_to_response('red_message.html', {'msg': msg})


def schedule_add_forms(request):
	if request.method == 'POST':
		form_add_forms = AddForms(request.POST)
        if form_add_forms.is_valid():
        	forms_name_add = form_add_forms.cleaned_data['forms_name_field']
        	match = re.search(ur'^[5-9]|10|11-?[АБВ]?/$', forms_name_add)
        	print match 
        	if not match:
        		msg = u"*Не існує такого класу, як '%s'" % forms_name_add
        		return render_to_response('red_message.html', {'msg': msg})    
        	data =  add_forms(forms_name_add)
        	if data:
        		msg = u"*Додано клас '%s'" % forms_name_add
        		return render_to_response('green_message.html', {'msg': msg})
        	else:
        		msg = u"*Клас '%s' Вже існує " % forms_name_add
        		return render_to_response('red_message.html', {'msg': msg})  
        else:
        	msg = u"*Дані не введено"
        	return render_to_response('red_message.html', {'msg': msg})



def schedule_del_forms(request):
	if request.method == 'POST':
		form_add_forms = DelForms(request.POST)
        if form_add_forms.is_valid():
        	forms_name_del = form_add_forms.cleaned_data['forms_name_field2']
        	data = del_forms(forms_name_del)
        	if data:
        		msg = u"*Видалено клас '%s' " % forms_name_del
        		return render_to_response('green_message.html', {'msg': msg})
        	else:
        		msg = u"*Немає даних для видалення"
        		return render_to_response('red_message.html', {'msg': msg})
        msg = u"*Цей клас вже видалений, перезавантажте сторінку"
        return render_to_response('red_message.html', {'msg': msg})


def schedule_del_forms_all(request):
	data = del_forms_all()
        if data:
        	msg = u"*Видалено всі класи"
        	return render_to_response('green_message.html', {'msg': msg})
        else:
        	msg = u"*Немає даних для видалення"
        	return render_to_response('red_message.html', {'msg': msg})

def team_add_members(request, *args):
	if request.method == 'POST':
		form_add = AddMember(request.POST)
        if form_add.is_valid():
        	member_name = form_add.cleaned_data['member_name_field']
        	photo_link = form_add.cleaned_data['photo_link_field']
        	info = form_add.cleaned_data['info_field']
        	kafedra = form_add.cleaned_data['kafedra_field']
        	level = form_add.cleaned_data['level_field']
        	add_data = add_member(member_name, photo_link, kafedra, info, level)
        	if add_data:
        		msg = u"Додано '%s'" % member_name
        		return render_to_response('green_message.html', {'msg': msg})
        	else:
        		msg = u"*Не вдалося додати"
        		return render_to_response('red_message.html', {'msg': msg})
        else:
        	msg = u"*Потрібно заповнити всі поля"
        	return render_to_response('red_message.html', {'msg': msg})


def team_del_members(request, *args):
	if request.method == 'POST':
		form_del = DelMember(request.POST)
		if form_del.is_valid():
			member_name = form_del.cleaned_data['member_name_field2']
			del_data = del_member(member_name)
			if del_data:
				msg = u"Видалено '%s'" % member_name
				return render_to_response('green_message.html', {'msg': msg})


def admins_add_members(request, *args):
	if request.method == 'POST':
		form_add = AddMember(request.POST)
        if form_add.is_valid():
        	member_name = form_add.cleaned_data['member_name_field']
        	photo_link = form_add.cleaned_data['photo_link_field']
        	info = form_add.cleaned_data['info_field']
        	level = form_add.cleaned_data['level_field']
        	add_data = add_admin(member_name, photo_link, info, level)
        	if add_data:
        		msg = u"Додано '%s'" % member_name
        		return render_to_response('green_message.html', {'msg': msg})
        	else:
        		msg = u"*Не вдалося додати"
        		return render_to_response('red_message.html', {'msg': msg})
        else:
        	msg = u"*Потрібно заповнити всі поля"
        	return render_to_response('red_message.html', {'msg': msg})


def admins_del_members(request, *args):
	if request.method == 'POST':
		form_del = DelAdmin(request.POST)
		if form_del.is_valid():
			member_name = form_del.cleaned_data['member_name_field2']
			del_data = del_admin(member_name)
			if del_data:
				msg = u"Видалено '%s'" % member_name
				return render_to_response('green_message.html', {'msg': msg})
			


@add_user_info_and_menu
def presentation_page(request, *args):
	context = args[0]
	pr = get_all_presentation()
	context['pr'] = pr
	if request.user.is_superuser:	
		addform = AddPresentationForm()
		delform = DelPresentationForm()		
		context['addform'] = addform
		context['delform'] = delform
		context.update(csrf(request))
		return render_to_response('presentation_dir.html', context)
	else:
		return render_to_response('presentation.html', context)


def add_presentation(request):
	if request.method == 'POST':
		add_form = AddPresentationForm(request.POST, request.FILES)
		if add_form.is_valid():
			name_prezentation = add_form.cleaned_data['name_prezentation']
			description_pr = add_form.cleaned_data['description_pr']
			filePresent = request.FILES['filePresent']
			fileName = request.FILES['filePresent'].name
			fileURL = save_presentation(filePresent, fileName)
			add_presentation_data(name_prezentation, description_pr, fileURL)
			msg = u'*Презентація "'+  fileName + u'" додана'
			return render_to_response('green_message.html', {'msg': msg})
		else:
			msg = u'*Не правильно заповнені або порожні поля'
			return render_to_response('red_message.html', {'msg': msg})


def del_presentation(request):
	if request.method == 'POST':
		del_form = DelPresentationForm(request.POST)
		if del_form.is_valid():
			name_prezentation = del_form.cleaned_data['prezentations']		
			del_presentation_data(name_prezentation)
			msg = u'*Презентацію "'+  name_prezentation + u'" видалено'
			return render_to_response('green_message.html', {'msg': msg})
		else:
			msg = u'*Презентацію не вдалося видалити'
			return render_to_response('red_message.html', {'msg': msg})



@add_user_info_and_menu
def useful_links_page(request, *args):
	context = args[0]
	data = get_all_useful_links()
	context['data'] = data
	if request.user.is_superuser:	
		addform = AddUsefulLinksForm()
		delform = DelUsefulLinksForm()	
		context['addform'] = addform
		context['delform'] = delform
		context.update(csrf(request))
		return render_to_response('useful_links_dir.html', context)
	else:
		return render_to_response('useful_links.html', context)



def add_link(request):
	if request.method == 'POST':
		add_form = AddUsefulLinksForm(request.POST)
		if add_form.is_valid():
			name_link = add_form.cleaned_data['name_link']
			link = add_form.cleaned_data['link']
			description_l = add_form.cleaned_data['description_l']
			add_links(name_link, description_l, link)
			msg = u'*Посилання "'+  name_link + u'" додано'
			return render_to_response('green_message.html', {'msg': msg})
		else:
			msg = u'*Не правильно заповнені або порожні поля'
			return render_to_response('red_message.html', {'msg': msg})


def del_link(request):
	if request.method == 'POST':
		del_form = DelUsefulLinksForm(request.POST)
		if del_form.is_valid():
			link_for_del = del_form.cleaned_data['link_for_del']		
			del_links(link_for_del)
			msg = u'*Посилання "'+  link_for_del + u'" видалено'
			return render_to_response('green_message.html', {'msg': msg})
		else:
			msg = u'*Посилання не вдалося видалити'
			return render_to_response('red_message.html', {'msg': msg})