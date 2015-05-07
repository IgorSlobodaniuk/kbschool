from django.db import models



'''
class forms(models.Model):
	form = models.CharField(max_length=5)

	def __unicode__(self):
		return self.form

class days(models.Model):
	day = models.CharField(max_length=10)

	def __unicode__(self):
		return self.day

class subjects(models.Model):
	subject = models.CharField(max_length=30)

	def __unicode__(self):
		return self.subject

class allID(models.Model):
	formID = models.ForeignKey(forms)
	dayID = models.ForeignKey(days)
	subjectID = models.ForeignKey(subjects)

	def __unicode__(self):
		return u'%s %s' %(self.formID, self.dayID, self.subjectID)


class sipleShedule(models.Model):
	form = models.CharField(max_length=5)
	day = models.CharField(max_length=10)
	lesson_number = models.IntegerField(max_length=1)
	subject = models.CharField(max_length=30)

	def __unicode__(self):
		return u'%s %s' %(self.form, self.day, self.subject)
'''



class someImage(models.Model):
    image = models.ImageField(upload_to='/media')