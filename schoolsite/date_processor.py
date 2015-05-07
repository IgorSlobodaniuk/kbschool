from datetime import date


def get_season():
	doy = date.today().timetuple().tm_yday
	spring = range(60, 152)
	summer = range(152, 244)
	autumn = range(244, 335)
	if doy in spring:
		season = 'spring'
	elif doy in summer:
		season = 'summer'
	elif doy in autumn:
		season = 'autumn'
	else:
		season = 'winter'
	return season


def get_curent_day():
	curent_date = str(date.today())
	holidays = {'2014-08-23': (('flag_day', 'png'),), 
				'2014-08-24': (('independence_day', 'png'),), 
				'2014-09-01': (('1ver', 'png'),), 
				'2014-10-05': (('teachers_day', 'jpg'),), 
				'2014-10-31': (('helloween', 'png'),), 
				'2014-12-06': (('den_zproinyh_sil', 'jpg'),), 
				'2014-12-19': (('mikolay', 'png'),), 
				'2015-01-01': (('new_year', 'gif'),),  
				'2015-02-14': (('valentines_day', 'png'),),  
				'2015-03-08': (('woman_day', 'png'),), 
				'2015-03-09': (('tsh', 'jpg'),), 
				'2015-03-10': (('tsh', 'jpg'),), 
				}
	curent_holiday = holidays.get(curent_date)
	if curent_holiday:
		return curent_holiday 
	else:
		curent_holiday = (('general', 'png'),)
		return curent_holiday  
	