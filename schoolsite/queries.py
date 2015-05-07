# -*- coding: utf-8 -*-
from django.db import connection, transaction
import time
from datetime import date
import os

def get_shedule(form, day):
    cursor = connection.cursor()
    sql = """SELECT  `lesson_number`, `subject` 
             FROM `schoolsite_sipleshedule` 
             WHERE `form`= '%s' AND `day`= '%s' 
             ORDER BY `lesson_number`

          """ %(form, day)

    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def add_subject(form, day, lesson_number, subject):
    cursor = connection.cursor()
    sql = """ INSERT INTO `schoolsite_sipleshedule`(`form`, `day`, `lesson_number`, `subject`) 
              VALUES ('%s', '%s', '%s', '%s')
          """  %(form, day, lesson_number, subject)
    cursor.execute(sql)
    transaction.commit_unless_managed()
    

def del_subject(form, day, lesson_number):
    cursor = connection.cursor()
    sql1 = """ SELECT `form`, `day`, `lesson_number`
               FROM `schoolsite_sipleshedule` 
               WHERE `form` = '%s'
               AND `day` = '%s'
               AND `lesson_number` = '%s'
               
          """  %(form, day, lesson_number)
    
    sql2 = """ DELETE FROM `schoolsite_sipleshedule` 
               WHERE `form` = '%s'
               AND `day` = '%s'
               AND `lesson_number` = '%s'
               
          """  %(form, day, lesson_number)
    cursor.execute(sql1)
    res = cursor.fetchone()
    if res != None:
        cursor.execute(sql2)
        transaction.commit_unless_managed()
    return res

    
   
def del_all():
    cursor = connection.cursor()
    sql1 = "SELECT * FROM `schoolsite_sipleshedule`"
    sql2 = "DELETE FROM `schoolsite_sipleshedule`"
    cursor.execute(sql1)
    res = cursor.fetchall()
    if res:
        cursor.execute(sql2)
        transaction.commit_unless_managed()
        return True
    else:
        return False


def build_select_box():
    cursor = connection.cursor()
    sql = "SELECT `schoolform`, `schoolform` FROM `forms`"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res



def add_forms(form_name):
    cursor = connection.cursor()
    sql1 = "SELECT `schoolform` FROM `forms` WHERE `schoolform` = '%s' " %form_name
    sql2 = "INSERT INTO `forms`(`schoolform`) VALUES ('%s')" %form_name
    cursor.execute(sql1)
    res = cursor.fetchone()
    if not res:
        cursor.execute(sql2)
        transaction.commit_unless_managed()
        return True
    else:
        return False


def del_forms(form_name):
    cursor = connection.cursor()
    sql1 = "SELECT * FROM `forms` WHERE `schoolform` = '%s'" %form_name
    sql2 = "DELETE FROM `forms` WHERE `schoolform` = '%s'" %form_name
    res = cursor.execute(sql1)
    if res:
        cursor.fetchone()
        cursor.execute(sql2)
        transaction.commit_unless_managed()
        return True
    else:
        return False


    

def del_forms_all():
    cursor = connection.cursor()
    sql1 = "SELECT * FROM `forms`"
    sql2 = "DELETE FROM `forms`"
    cursor.execute(sql1)
    res = cursor.fetchall()
    if res:
        cursor.execute(sql2)
        transaction.commit_unless_managed()
        return True



def select_forms_for_sch():
    res = build_select_box()
    myRes = []
    for a, b in res:
        myRes.append(a)
    return myRes


    
def get_members(kafedra):
    cursor = connection.cursor()
    sql = "SELECT * FROM `members` WHERE `kafedra` = '%s' ORDER BY `level`" % kafedra
    cursor.execute(sql)
    res = cursor.fetchall()
    return res
    



def add_member(member_name, photo_link, kafedra, info, level):
    cursor = connection.cursor()
    sql1 = "DELETE FROM `members` WHERE `member_name` = '%s'" % member_name
    sql2 =  """INSERT INTO `members`(`member_name`, `photo_link`, `member_info`, `level`, `kafedra`)
               VALUES ('%s', '%s', '%s', '%s', '%s')
            """ % (member_name, photo_link,  info, level, kafedra)
    cursor.execute(sql1)
    cursor.execute(sql2)
    transaction.commit_unless_managed()
    return True



def member_names_for_select_box():
    cursor = connection.cursor()
    sql = "SELECT `member_name`, `member_name` FROM `members`"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def del_member(member_name):
    cursor = connection.cursor()
    sql = "DELETE FROM `members` WHERE `member_name` = '%s'" % member_name
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return True





def get_all_admins():
    cursor = connection.cursor()
    sql = "SELECT * FROM `admins` ORDER BY `level`"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res
    



def add_admin(member_name, photo_link, info, level):
    cursor = connection.cursor()
    sql1 = "DELETE FROM `admins` WHERE `member_name` = '%s'" % member_name
    sql2 =  """INSERT INTO `admins`(`member_name`, `photo_link`, `member_info`, `level`)
               VALUES ('%s', '%s', '%s', '%s')
            """ % (member_name, photo_link, info, level)
    cursor.execute(sql1)
    cursor.execute(sql2)
    transaction.commit_unless_managed()
    return True



def admin_names_for_select_box():
    cursor = connection.cursor()
    sql = "SELECT `member_name`, `member_name` FROM `admins`"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def del_admin(member_name):
    cursor = connection.cursor()
    sql = "DELETE FROM `admins` WHERE `member_name` = '%s'" % member_name
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return True



def add_new_guest():
    cursor = connection.cursor()
    sql = "INSERT INTO `attendance`(`count_times`) VALUES ('1')"
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return True


def get_guests_count():
    cursor = connection.cursor()
    sql = "SELECT SUM(`count_times`) FROM `attendance`"
    cursor.execute(sql)
    res1 = cursor.fetchone()
    res2 = ''
    res2 += str(int(res1[0]))
    if 10 < int(res2[-2:]) < 20:
        res = res2 + u' разів'
    elif res2[-1:] == '1':
        res = res2 + u' раз'
    elif 1 < int(res2[-1:]) < 5:
        res = res2 + u' рази'
    else:
        res = res2 + u' разів'
    return res


def get_all_videos():
    cursor = connection.cursor()
    sql = "SELECT * FROM `videos`"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res



def video_names_for_select_box():
    cursor = connection.cursor()
    sql = "SELECT `videoname`, `videoname` FROM `videos`"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res



def add_video_to_database(video_name, video_link):
    cursor = connection.cursor()
    sql = """INSERT INTO `videos`(`videoname`, `videolink`) 
             VALUES ('%s', '%s')""" % (video_name, video_link)
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return True



def del_video_from_database(video_name):
    cursor = connection.cursor()
    sql = "DELETE FROM `videos` WHERE `videoname` = '%s' " % video_name
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return True


def get_all_tutorials():
    cursor = connection.cursor()
    sql = """SELECT `name`, `form`, `author`, `reproduction_hous`, `year`, `url` 
             FROM `tutorials` """ 
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def add_tutorials_data(tutorial_name, form, author, reproduction_house, year, fileURL):
    cursor = connection.cursor()
    sql = """ INSERT INTO `tutorials`(`name`, `form`, `author`, `reproduction_hous`, `year`, `url`) 
              VALUES ('%s','%s','%s','%s','%s','%s')
          """ % (tutorial_name, form, author, reproduction_house, year, fileURL)
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return True


def del_tutorials_data(tutorial_name, form, author, reproduction_house, year):
    cursor = connection.cursor()
    sql = """ DELETE FROM `tutorials` 
              WHERE `name` ='%s' 
              AND  `form` ='%s' 
              AND `author` ='%s' 
              AND `reproduction_hous` ='%s' 
              AND `year` = '%s'
          """ % (tutorial_name, form, author, reproduction_house, year)
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return True


def get_all_presentation():
    cursor = connection.cursor()
    sql = "SELECT * FROM `presentation`"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

   
def get_all_presentations_names():
    cursor = connection.cursor()
    sql = "SELECT `name`, `name` FROM `presentation`"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res
 

def add_presentation_data(name_prezentation, description_pr, fileURL):
    cursor = connection.cursor()
    sql = """ INSERT INTO `presentation`(`name`, `description`, `link`) 
              VALUES ('%s','%s','%s')
          """ % (name_prezentation, description_pr, fileURL)
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return True


def del_presentation_data(name_prezentation):
    cursor = connection.cursor()
    sql = "DELETE FROM `presentation` WHERE `name` ='%s'"% name_prezentation
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return True


def get_all_useful_links():
    cursor = connection.cursor()
    sql = "SELECT * FROM `useful_links`"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def get_all_useful_links_names():
    cursor = connection.cursor()
    sql = "SELECT `name`, `name` FROM `useful_links`"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def add_links(name_link, description_l, link):
    cursor = connection.cursor()
    sql = """ INSERT INTO `useful_links`(`name`, `description`, `link`)
              VALUES ('%s','%s','%s')
          """ % (name_link, description_l, link)
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return True


def del_links(link_name):
    cursor = connection.cursor()
    sql = "DELETE FROM `useful_links` WHERE `name` ='%s'"% link_name
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return True


def get_all_news_data():
    cursor = connection.cursor()
    sql = "SELECT * FROM `news` ORDER BY `date_added` DESC"
    cursor.execute(sql)
    res = cursor.fetchall()
    res = [list(i) for i in res]
    for el in res:
        el[3] = el[3][:500]+'...'
        el[3] = el[3].split('<br>')
    return res

def get_news_title_and_date():
    cursor = connection.cursor()
    sql = "SELECT  `title`, `code`, `date_added` FROM `news` ORDER BY `date_added` DESC LIMIT 5 "
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def add_news_it(title, side_picture, content):
    cursor = connection.cursor()
    code = str(int(time.time()))
    path_to_files = 'edusite/media/images/for_news/'
    os.makedirs(path_to_files + code)
    photos_directory = path_to_files + code
    date_added = date.today()
    sql = """ INSERT INTO `news`(`code`, `title`, `side_picture`, `content`, `photos_directory`, `date_added`) 
              VALUES ('%s', '%s', '%s', '%s', '%s', '%s')
          """ % (code, title, side_picture, content, photos_directory, date_added)
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return True


def del_news_it(code):
    cursor = connection.cursor()
    sql = "DELETE FROM `news` WHERE `code` = '%s'" % code
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return True

def get_news_item_data(code):
    cursor = connection.cursor()
    sql = """SELECT `title`, `side_picture`, `content`, `date_added`, `photos_directory` 
             FROM `news` WHERE `code` = '%s'""" % code
    cursor.execute(sql)
    res = cursor.fetchall()
    res = [list(i) for i in res]
    for el in res:
        el[2] = el[2].split('<br>')
    return res


def get_all_news_codes():
    cursor = connection.cursor()
    sql = "SELECT `code`, `code` FROM `news` ORDER BY `date_added`"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res
