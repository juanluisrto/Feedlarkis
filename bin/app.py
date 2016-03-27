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

session = web.session.Session(app, store, initializer={'login': 0, 'privilege': 0})

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
			render = web.template.render('templates/user/', base="layout") # TODO make layout
		elif privilege == 1:
			render = web.template.render('templates/admin/', base="layout")
		else:
			render = web.template.render('templates/reader/', base="layout")
	else:
		render = web.template.render('templates/reader/', base="layout")
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
			if u_passwd == storage['password'] and storage['authorized']:
				session.login = 1
				session.privilege = storage['privilege']
				render = create_render(session.privilege)
				return render.login(failed=False, state='login_ok')
			elif u_passwd == storage['password'] and not storage['authorized']:
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
	form.Password('Password_again',description="Repat Password"),
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

			sequence_id = db.insert('USERS_DATA', USER="$name0", PASSWORD="$pass0",\
				EMAIL="$email0", PRIVILEGE=0, APPROVALCODE="$approval0",AUTHORIZED=0 )

			send_email('feedlarkis@gmail.com', '1234feedme', recipient=email0, subject='%s has signed up to feedlarkis',\
				body='''Dear Admin,
				A new user is trying to get access to feedlarkis with the following credentials:

				Username:  %s
				Email:  %s

				Follow this link to give him approval:

				%s

				''' % (user0, email0, BASE_URL+'/approval/'+approval0))

			return "Grrreat success! Username: %s, Password: %s\nNow please wait for approval" % (form0['Username'].value, form0['Password'].value)
			#TODO Add the new user info to the database


###### Booking system ######

days = ['10th November','11th November','12th November']


def allowed_bookings():
	pass


class Bookings:

	def GET(self):
		if logged():
			render = create_render(session.privilege)
			return '%s' % render.bookview(days=days)
		else:
			render = create_render(session.privilege)
			return '%s' % render.login(message='You cannot book without being logged in!!!')

	def POST(self):
		#form0 = booking_form()
		#render = create_render(session.privilege)
		form_info = web.input()
		return str( form_info )


class Approve:

	def GET(self, approval_id):
		q = db.update('users_database', where='approvalcode = $approval_id', authorized=1, vars=locals())
		return name



class Manage_Mealtimes:
	pass

if __name__ == "__main__":
	app.run()