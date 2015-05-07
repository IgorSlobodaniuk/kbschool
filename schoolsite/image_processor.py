# -*- coding: utf-8 -*-
import PIL
from PIL import Image
import os 
import urllib
import requests





def handle_uploaded_file(f, title):
    with open('edusite/media/images/original/' + title + '.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    resize_min(title)
    resize_max(title)
    return True


def save_file(f, tutorial_name):
    with open('edusite/media/tutorials/' + tutorial_name + '.pdf', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    path = '/media/tutorials/' + tutorial_name + '.pdf'
    return path

def save_news_side_picture(p, name):
    with open('edusite/media/images/for_news/news_side_picture/' + name, 'wb+') as destination:
        for chunk in p.chunks():
            destination.write(chunk)
    resize_250(name)
    return True

def resize_250(name):
    basewidth = 250
    img = Image.open('edusite/media/images/for_news/news_side_picture/' + name)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
    img.save('edusite/media/images/for_news/news_side_picture/' + name) 


def save_presentation(f, fileName):
    with open('edusite/media/presentations/' + fileName, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    path = '/media/presentations/' + fileName
    return path


def resize_min(title):
    basewidth = 200
    img = Image.open('edusite/media/images/original/' + title + '.jpg')
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
    img.save('edusite/media/images/min/' + title + '_min' +  '.jpg')


def resize_max(title):
    basewidth = 800
    img = Image.open('edusite/media/images/original/' + title + '.jpg')
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    img.save('edusite/media/images/max/' + title + '_max' +   '.jpg')

def get_all_img():
    directory = 'edusite/media/images/original' 
    images = os.listdir(directory)
    images.sort(key = lambda item: os.path.getmtime('edusite/media/images/original/' + item ))
    return images



def get_img_from_net(url, title):
    folderName = 'edusite/media/images/original/'
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    try:
        r = requests.head(url)
        if r.status_code == 200:
            l_slesh = url.rfind('/') + 1
            dot = url.rfind('.')
            if not title:
                title = url[l_slesh:dot]
            urllib.urlretrieve(url, folderName + title + '.jpg')
            resize_min(title)
            resize_max(title)
            return True
        else: 
            raise IOError
    except IOError:
        return False



def del_images(images):
    for img in images:
        os.remove('edusite/media/images/min/' + img + '_min.jpg')
        os.remove('edusite/media/images/max/' + img + '_max.jpg')
        os.remove('edusite/media/images/original/' + img + '.jpg')
    return True


def get_all_photo(directory): 
    images = os.listdir(directory)
    images.sort(key = lambda item: os.path.getmtime(directory + item ))
    return images


def add_photo(f, title, directory):
    with open(directory + title + '.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    resize_300(title, directory)

    return True


def resize_300(title, directory):
    basewidth = 300
    img = Image.open(directory + title + '.jpg')
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
    img.save(directory + title +  '.jpg')

def add_banner_image(f, title, directory):
    with open(directory + title + '.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    resize_1920(title, directory)
    return True

def resize_1920(title, directory):
    basewidth = 1920
    img = Image.open(directory + title + '.jpg')
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    img.save(directory + title + '.jpg')


def get_all_banner_photo(directory): 
    images = os.listdir(directory)
    return images




def del_photo(images, directory):
    for img in images:
        os.remove(directory + img + '')
    return True



def get_all_news_photos(code):
    directory = 'edusite/media/images/for_news/' + code
    images = os.listdir(directory)
    return images



def add_news_images(f, title, code):
    with open('edusite/media/images/for_news/'+ code + '/'+ title + '.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    resize_700(title, code)
    return True

def resize_700(title, code):
    basewidth = 700
    path = 'edusite/media/images/for_news/'+ code + '/'+ title + '.jpg'
    img = Image.open(path)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
    img.save(path) 



def get_news_img_from_net(url, title, code):
    folderName = 'edusite/media/images/for_news/' + code + '/'
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    try:
        r = requests.head(url)
        if r.status_code == 200:
            l_slesh = url.rfind('/') + 1
            dot = url.rfind('.')
            if not title:
                title = url[l_slesh:dot]
            urllib.urlretrieve(url, folderName + title + '.jpg')
            resize_700(title, code)
            return True
        else: 
            raise IOError
    except IOError:
        return False

def del_news_images(images, code):
    for img in images:
        os.remove('edusite/media/images/for_news/' + code + '/' + img)
    return True

def poster_exists():
    if os.path.exists('edusite/media/images/poster/poster_min.jpg'):
        return True
    else:
        return False

def add_new_poster(f):
    with open('edusite/media/images/poster/poster.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk) 
    resize_poster_700()
    resize_poster_250()
    return True


def resize_poster_700():
    basewidth = 700
    img = Image.open('edusite/media/images/poster/poster.jpg')
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
    img.save('edusite/media/images/poster/poster_max.jpg')


def resize_poster_250():
    basewidth = 250
    img = Image.open('edusite/media/images/poster/poster.jpg')
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
    img.save('edusite/media/images/poster/poster_min.jpg')


def del_old_poster():
    if os.path.exists('edusite/media/images/poster/poster_min.jpg'):
        os.remove('edusite/media/images/poster/poster.jpg')
        os.remove('edusite/media/images/poster/poster_min.jpg')
        os.remove('edusite/media/images/poster/poster_max.jpg')
        return True
    else:
        return False



