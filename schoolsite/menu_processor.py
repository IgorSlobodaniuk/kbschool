# -*- coding: utf-8 -*-

def navigation_menu(request):
    dic = [
        {(u'Головна'): ['/index']},
        {(u'Новини'): ['/news']},


        {(u'Інформація про школу'): [
            ((u'Історія'), '/history'),
            ((u'Адміністрація'), '/admins'),
            ((u'Педагогічний колектив'), '/team'),

        ]},

        {(u'Мультимедіа'): [
            ((u'Фотогалерея'), '/photogallery'),
            ((u'Відеогалерея'), '/videogallery'),
        ]},
        {(u'Розклад уроків'): ['/schedule']},
        {(u'Каталог файлів'): [
            ((u'Електронні підручники'), '/tutorials'),
            ((u'Презентації'), '/presentation'),
        ]},
        {(u'Корисні посилання'): ['/useful_links']},
    ]
    if request.user.is_superuser:
        dic.append(
            {(u'Всі зображення'): [
                ((u'Для фотогалереї'), '/images_for_photogallery'),
                ((u'Для адміністраціЇ'), '/images_for_admins'),
                ((u'Для колективу'), '/images_for_team'), 
                ((u'Для баннера'), '/images_for_banner'), 
                ((u'Для афіші'), '/poster'), 

                ]}
        )


    menu = {'menu': dic}
    return menu
