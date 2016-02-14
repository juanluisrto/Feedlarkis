import web
import hashlib
from web import form

urls = (
  '/login', 'Login',
  '/reset', 'Reset',
  '/signup', 'Signup'
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


class Login:

	def GET(self):
		if logged():
			render = create_render(session.privilege)
			return '%s' % render.login_double() # TODO Make the login_double template
		else:
			render = create_render(session.privilege)
			return '%s' % render.login()

	def POST(self):
		form_info = web.input()
		u_name, u_passwd = form_info.user, form_info.passwd

		try:
			storage = db.select('users_database', where='user=$u_name', vars=locals())[0]
			if u_passwd == storage['pass']:
					session.login = 1
					session.privilege = storage['privilege']
					render = create_render(session.privilege)
					return render.login_ok() # TODO Make the login_ok template
			else:
				session.login = 0
				session.privilege = -1
				render = create_render(session.privilege)
				return render.login_error(user_exists=True) # TODO Make the login_ok template
			
		except:
			session.login = 0
			session.privilege = -1
			render = create_render(session.privilege)
			return render.login_error(user_exists=False)
		

class Reset:

	def GET(self):
		session.login = 0
		session.kill()
		render = create_render(session.privilege)
		return 'Logged out' # TODO logout template


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
            return "Grrreat success! Username: %s, Password: %s" % (form0['Username'].value, form0['Password'].value)

if __name__ == "__main__":
	app.run()