# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from schoolsite.queries import build_select_box
from schoolsite.queries import member_names_for_select_box
from schoolsite.queries import admin_names_for_select_box
from schoolsite.queries import video_names_for_select_box
from schoolsite.queries import get_all_presentations_names
from schoolsite.queries import get_all_useful_links_names
from schoolsite.queries import get_all_news_codes


class LoginForm(AuthenticationForm):
    pass


class ChangeSchedule(forms.Form):
    
    forms_name_field = forms.ChoiceField(
        widget=forms.Select(), 
        choices=(), 
        label=u'Клас')
    def __init__(self, data=None, *args, **kwargs):
        super(ChangeSchedule, self).__init__(data, *args, **kwargs)
        self.fields['forms_name_field'].choices = build_select_box()

    top_field3 = (('monday', 'Понеділок',), 
                  ('tuesday', 'Вівторок',), 
                  ('wednesday', 'Середа',), 
                  ('thursday', 'Четвер',), 
                  ('friday', 'П’ятниця',))
    day_field = forms.ChoiceField(
        widget=forms.Select(),
        choices=top_field3,
        label=u'День тижня')

    top_field2 = (('0', '0',), ('1', '1',), ('2', '2',), ('3', '3',), 
                  ('4', '4',), ('5', '5',), ('6', '6',), ('7', '7',))
    lesson_number_field = forms.ChoiceField(
        widget=forms.Select(),
        choices=top_field2,
        label=u'Номер уроку')

    subject_field = forms.CharField(
        label=u'Предмет',
        max_length=50)





class DelSchedule(forms.Form):
    forms_name_field = forms.ChoiceField(
        widget=forms.Select(), 
        choices=(), 
        label=u'Клас')
    def __init__(self, data=None, *args, **kwargs):
        super(DelSchedule, self).__init__(data, *args, **kwargs)
        self.fields['forms_name_field'].choices = build_select_box()

    top_field3 = (('monday', 'Понеділок',), 
                  ('tuesday', 'Вівторок',), 
                  ('wednesday', 'Середа',), 
                  ('thursday', 'Четвер',), 
                  ('friday', 'П’ятниця',))
    day_field = forms.ChoiceField(
        widget=forms.Select(),
        choices=top_field3,
        label=u'День тижня')

    top_field2 = (('0', '0',), ('1', '1',), ('2', '2',), ('3', '3',), 
                  ('4', '4',), ('5', '5',), ('6', '6',), ('7', '7',))
    lesson_number_field = forms.ChoiceField(
        widget=forms.Select(),
        choices=top_field2,
        label=u'Номер уроку')



class AddForms(forms.Form):
    forms_name_field = forms.CharField(
        label=u'Клас',
        max_length=5)


class DelForms(forms.Form):
    forms_name_field2 = forms.ChoiceField(
        choices=(), 
        label=u'Клас')
    def __init__(self, data=None, *args, **kwargs):
        super(DelForms, self).__init__(data, *args, **kwargs)
        self.fields['forms_name_field2'].choices = build_select_box()


class AddMember(forms.Form):
    member_name_field = forms.CharField(
        label=u'ПІБ',
        max_length=50)

    photo_link_field = forms.CharField(
        label=u'Посилання на зображення')

    info_field = forms.CharField(
        label=u'Спеціалізація')


    kaf_names = (('математики,_інформатики_та_фізики', 'математики, інформатики та фізики',), 
                 ('історії', 'історії',), 
                 ('української_мови_та_літератури', 'української мови та літератури',), 
                 ('початкових_класів', 'початкових класів',),
                 ('іноземних_мов_та_світової_літератури', 'іноземних мов та світової літератури',), 
                 ('геграфії,_біології_та_хімії', 'геграфії, біології та хімії',), 
                 ('фізкультури,_технології_та_музики', 'фізкультури, технології та музики',))


    kafedra_field = forms.ChoiceField(
        choices=kaf_names,
        label=u'Кафедра')



    top_field = (('1', '1',), ('2', '2',), ('3', '3',), ('4', '4',),
                 ('5', '5',), ('6', '6',), ('7', '7',))

    level_field = forms.ChoiceField(
        choices=top_field,
        label=u'Рівень')




class DelMember(forms.Form):
    member_name_field2 = forms.ChoiceField(
        choices=(), 
        label=u'ПІБ')
    def __init__(self, data=None, *args, **kwargs):
        super(DelMember, self).__init__(data, *args, **kwargs)
        self.fields['member_name_field2'].choices = member_names_for_select_box()



class DelAdmin(forms.Form):
    member_name_field2 = forms.ChoiceField(
        choices=(), 
        label=u'ПІБ')
    def __init__(self, data=None, *args, **kwargs):
        super(DelAdmin, self).__init__(data, *args, **kwargs)
        self.fields['member_name_field2'].choices = admin_names_for_select_box()


class UploadImageForm(forms.Form):
    title = forms.CharField(max_length=50, label=u'Назва зображення', required=False)
    image = forms.ImageField(label=u'Вибрати зображення')


class UploadImageFromNetForm(forms.Form):
    title = forms.CharField(max_length=50, label=u'Назва зображення', required=False)
    image_link = forms.URLField(label=u'Посилання на зображення')


class DelImageForm(forms.Form):
    pass


class AddVideoForm(forms.Form):
    title = forms.CharField(max_length=50, label=u'Назва відео', required=False)
    video_link = forms.URLField(label=u'Посилання на відео')


class DelVideoForm(forms.Form):
    video_name_field = forms.ChoiceField(
        choices=(), 
        label=u'Назва відео')
    def __init__(self, data=None, *args, **kwargs):
        super(DelVideoForm, self).__init__(data, *args, **kwargs)
        self.fields['video_name_field'].choices = video_names_for_select_box()



class AddTutorialsForm(forms.Form):
    forms_name = (('5', '5',), ('6', '6',), ('7', '7',), ('8', '8',),
                 ('9', '9',), ('10', '10',), ('11', '11',))   
    form = forms.ChoiceField(choices=forms_name, label=u'Клас')
    tutorial_name = forms.CharField(label=u'Назва видання')
    author = forms.CharField(label=u'Автор')
    reproduction_house = forms.CharField(label=u'Видавництво')
    year = forms.IntegerField(label=u'Рік видання')
    filePDF = forms.FileField(label=u'Вибрати файл')


class DelTutorialsForm(forms.Form):
    forms_name = (('5', '5',), ('6', '6',), ('7', '7',), ('8', '8',),
                 ('9', '9',), ('10', '10',), ('11', '11',))
    form = forms.ChoiceField(choices=forms_name, label=u'Клас')
    tutorial_name = forms.CharField(label=u'Назва видання')
    author = forms.CharField(label=u'Автор')
    reproduction_house = forms.CharField(label=u'Видавництво')
    year = forms.CharField(label=u'Рік видання')


class AddPresentationForm(forms.Form):
    name_prezentation = forms.CharField(label=u'Назва презентації')
    description_pr = forms.CharField(label=u'Короктий опис')
    filePresent = forms.FileField(label=u'Вибрати файл')


class DelPresentationForm(forms.Form):
    prezentations = forms.ChoiceField(
        choices=(), 
        label=u'Назва презентації')
    def __init__(self, data=None, *args, **kwargs):
        super(DelPresentationForm, self).__init__(data, *args, **kwargs)
        self.fields['prezentations'].choices = get_all_presentations_names()


class AddUsefulLinksForm(forms.Form):
    name_link = forms.CharField(label=u'Назва')
    description_l = forms.CharField(label=u'Короктий опис')
    link = forms.CharField(label=u'Посилання')



class DelUsefulLinksForm(forms.Form):
    link_for_del = forms.ChoiceField(
        choices=(), 
        label=u'Назва посилання')
    def __init__(self, data=None, *args, **kwargs):
        super(DelUsefulLinksForm, self).__init__(data, *args, **kwargs)
        self.fields['link_for_del'].choices = get_all_useful_links_names()


class AddNewsForm(forms.Form):
    title = forms.CharField(label=u'Заголовок')
    content_field = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}), label=u'Текст')
    side_picture_field = forms.ImageField(label=u'Вибрати зображення')

class SelectNewsImagesFolderForm(forms.Form):
    news_code = forms.ChoiceField(
        widget=forms.Select(attrs={'onChange': "loadXMLDoc1('/change_news_photo/','ajaxDiv', document.forms.selectform)"}),
        choices=(), 
        label=u'Вибрати публікацію')
    def __init__(self, data=None, *args, **kwargs):
        super(SelectNewsImagesFolderForm, self).__init__(data, *args, **kwargs)
        self.fields['news_code'].choices = get_all_news_codes()

class DelNewsForm(forms.Form):
    code = forms.ChoiceField(
        choices=(), 
        label=u'Вибрати публікацію')
    def __init__(self, data=None, *args, **kwargs):
        super(DelNewsForm, self).__init__(data, *args, **kwargs)
        self.fields['code'].choices = get_all_news_codes()