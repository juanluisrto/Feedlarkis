import web
import hashlib
from web import form
import smtplib
import string
import random
import datetime

BASE_URL = 'www.feedlarkis.org'

urls = (
  '/', 'Welcome',
  '/login', 'Login',
  '/reset', 'Reset',
  '/signup', 'Signup',
  '/book', 'Bookings',
  '/approval/(.*)', 'Approve'
  '/manage/mealtimes', 'Manage_Mealtimes'
)

web.config.debug = False

app = web.application(urls, locals())

db = web.database(dbn='sqlite', db='larkstadens.db')

store = web.session.DiskStore('sessions')

session = web.session.Session(app, store, initializer={'login': 0, 'privilege': 0, 'user':'XXXXX'})

def logged():
	if session.login==1:
		return True
	else:
		return False

def create_render(privilege):

	'''This is the privilege management system

	It creates a different render object depending the privilege
	instead of doing simply
	render = web.template.render('templates/', base="layout")
	'''
	if logged():
		if privilege == 0:
			render = web.template.render('templates/user/', base="layout", globals={ 'zip': zip, 'enumerate':enumerate }) # TODO make layout
		elif privilege == 1:
			render = web.template.render('templates/admin/', base="layout", globals={ 'zip': zip, 'enumerate':enumerate })
		else:
			render = web.template.render('templates/reader/', base="layout", globals={ 'zip': zip, 'enumerate':enumerate })
	else:
		render = web.template.render('templates/reader/', base="layout", globals={ 'zip': zip, 'enumerate':enumerate })
	return render


def send_email(user, pwd, recipient, subject, body):

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"

class Welcome:

	def GET(self):
		if logged():
			render = create_render(session.privilege)
			return '%s' % render.welcome_screen()
		else:
			render = create_render(session.privilege)
			return '%s' % render.welcome_screen()

class Login:

	def GET(self):
		if logged():
			render = create_render(session.privilege)
			return '%s' % render.login(failed = False, state='double')
		else:
			render = create_render(session.privilege)
			return '%s' % render.login(failed = False, state='first_try')

	def POST(self):
		form_info = web.input()
		u_name, u_passwd = form_info.user, form_info.passwd

		try:
			storage = db.select('USERS_DATA', where='USER=$u_name', vars=locals())[0]
			print storage['PASSWORD'],storage['AUTHORIZED']
			if u_passwd == storage['PASSWORD'] and storage['AUTHORIZED']:
				session.login = 1
				session.privilege = storage['PRIVILEGE']
				session.user = u_name
				render = create_render(session.privilege)
				return render.login(failed=False, state='login_ok')
			elif u_passwd == storage['PASSWORD'] and not storage['AUTHORIZED']:
				session.login = 0
				session.privilege = -1
				render = create_render(session.privilege)
				return render.login(failed=True, state='wait_approval') # TODO Make the login_waitforapproval template
			else:
				session.login = 0
				session.privilege = -1
				render = create_render(session.privilege)
				return render.login(failed=True, state='user_exists')
			
		except:
			session.login = 0
			session.privilege = -1
			render = create_render(session.privilege)
			return render.login(failed=True, state='user_not_found')
		

class Reset:

	def GET(self):
		session.login = 0
		session.kill()
		render = create_render(session.privilege)
		return render.logout()


###### Signup ######

signup_form = form.Form( 
	form.Textbox("Username"),
	form.Textbox("Email",form.Validator('This is not a valid email', lambda x:'@' in x)),
	form.Password('Password',form.Validator('Must be more at least 6 characters', lambda x:len(x)>5)),
	form.Password('Password_again',description="Repeat Password"),
	validators = [form.Validator("Passwords didn't match.", lambda i: i.Password == i.Password_again)]
	) 

class Signup:

	def GET(self): 
		form0 = signup_form()
		# make sure you create a copy of the form by calling it (line above)
		# Otherwise changes will appear globally
		render = create_render(session.privilege)
		return render.signup(form0)

	def POST(self): 
		form0 = signup_form() 
		render = create_render(session.privilege)
		if not form0.validates(): 
			return render.signup(form0)
		else:
			# form.d.foe and form['foe'].value are equivalent ways of
			# extracting the validated arguments from the form.
			dictinput = web.input()
			user0 = dictinput['Username']
			pass0 = dictinput['Password']
			email0 = dictinput['Email']
			approval0 = ''.join( [ random.choice( string.letters ) for _ in xrange(10) ] )

			sequence_id = db.insert('USERS_DATA', USER=name0, PASSWORD=pass0,\
				EMAIL=email0, PRIVILEGE=0, AUTHORIZED=0, APPROVALCODE=approval0 )

			send_email('feedlarkis@gmail.com', '1234feedme', recipient="gioelelamanno@gmail.com", subject='%s has signed up to feedlarkis',\
				body='''
				Dear Admin,
				A new user is trying to get access to feedlarkis with the following credentials:

				Username:  %s
				Email:  %s

				Follow this link to give him approval:

				%s

				''' % (user0, email0, BASE_URL+'/approval/'+approval0))

			return "Grrreat success! Username: %s, Password: %s\nNow please wait for approval" % (form0['Username'].value, form0['Password'].value)
			#TODO Add the new user info to the database


###### Booking system ######

def allowed_bookings():
    days = list( db.query('''SELECT DAY FROM MEALTIMES 
    WHERE DATE(DAY) < DATE('now','+7 days') AND DATE('now') < DATE(DAY)'''))

    breakfast = list( db.query('''SELECT DAY, BREAKFAST_START FROM MEALTIMES 
    WHERE DATE('now') < DATE(BREAKFAST_START, 'start of day','-1 days','+9 hours','+30 minutes') AND DATE(DAY) < DATE('now','+7 days')''') )

    normal_lunch = list( db.query('''SELECT DAY, LUNCH FROM MEALTIMES 
    WHERE DATE('now') < DATE(LUNCH, 'start of day','+9 hours','+30 minutes') AND DATE(DAY) < DATE('now','+7 days')''') )

    box_lunch = list( db.query('''SELECT DAY, LUNCH FROM MEALTIMES 
    WHERE DATE('now') < DATE(LUNCH, 'start of day','-1 days','+9 hours','+30 minutes') AND DATE(DAY) < DATE('now','+7 days')''') )

    dinner = list( db.query('''SELECT DAY, DINNER FROM MEALTIMES 
    WHERE DATE('now') < DATE(DINNER, 'start of day','+9 hours','+30 minutes') AND DATE(DAY) < DATE('now','+7 days')''') )

    list_outputs = []
    for day in map(lambda x: x['DAY'], days):
        Bre = []
        Lun = []
        Din = []
        if day in map(lambda x: x['DAY'], breakfast):
            Bre += ['-','X','T']
        if day in map(lambda x: x['DAY'], normal_lunch):
            Lun += ['-','X']
        if day in map(lambda x: x['DAY'], box_lunch):
            Lun += ['M','L']
        if day in map(lambda x: x['DAY'], dinner):
            Din += ['-','X', 'S']

        prettyname = datetime.datetime.strptime(day, '%Y-%m-%d').strftime('%A - %d %B %Y')
        list_outputs.append([day, prettyname, Bre, Lun, Din])

    return list_outputs


class Bookings:

	def GET(self):
		if logged():
			render = create_render(session.privilege)
			return '%s' % render.bookview(allowed_bookings=allowed_bookings())
		else:
			render = create_render(session.privilege)
			return '%s' % render.login(failed = False, state='booking_attempt')

	def POST(self):
		#form0 = booking_form()
		#render = create_render(session.privilege)
		form_info = web.input()

		messages_dict = {}
		for k,v in form_info.iteritems():
			parsed_k = k.split(' ')
			if len(parsed_k) == 3:
				messages_dict[ ' '.join(parsed_k[:-1]) ] = v

		for k,v in form_info.iteritems():
			parsed_k = k.split(' ')
			if len(parsed_k) == 2:
				if v != u'':
					sequence_id = db.insert('BOOKINGS', USER=session.user,
						SUBMISSION_TIME=datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),\
						BOOKING_DAY=parsed_k[0],
						MEAL=parsed_k[1],
						TYPE=v,
						MESSAGE=messages_dict[k] )
		return 'Done'


class Approve:

	def GET(self, approval_id):
		q = db.update('USERS_DATA', where='APPROVALCODE = $approval_id', AUTHORIZED=1, vars=locals())
		return '<div>Approved!s</div>'


class Manage_Mealtimes:
	pass

if __name__ == "__main__":
	app.run()