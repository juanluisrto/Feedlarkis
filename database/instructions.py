import sqlite3
import datetime

conn = sqlite3.connect('larkstadens.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE USERS_DATA(
  USER TEXT PRIMARY KEY NOT NULL,
  NAME TEXT,
  SURNAME TEXT,
  PASSWORD TEXT NOT NULL,
  EMAIL TEXT NOT NULL,
  PRIVILEGE INTEGER NOT NULL DEFAULT 0,
  AUTHORIZED INTEGER NOT NULL DEFAULT 0,
  APPROVALCODE TEXT);
''')

# Insert a row of data
c.execute('''INSERT INTO USERS_DATA (USER, NAME, SURNAME, PASSWORD, EMAIL, PRIVILEGE, AUTHORIZED, APPROVALCODE)
	VALUES ('gioelelm', 'Gioele', 'La Manno', 'adminpass','gioelelamanno@gmail.com',1,1);''')

# Create table
c.execute('''CREATE TABLE BOOKINGS(
  ID INTEGER PRIMARY KEY NOT NULL,
  USER TEXT,
  SUBMISSION_TIME TEXT NOT NULL,
  BOOKING_TIME TEXT NOT NULL,
  MEAL TEXT NOT NULL,
  MESSAGE TEXT)
''')

# Insert a row of data
c.execute("INSERT INTO BOOKINGS VALUES ()")

# Create table
c.execute('''CREATE TABLE MEALTIMES(
  DAY TEXT PRIMARY KEY NOT NULL,
  BREAKFAST TEXT NOT NULL,
  LUNCH TEXT NOT NULL,
  DINNER TEXT NOT NULL,
  MESSAGE TEXT)
''')

def default_meals(timeobj):
	pass

#Prefill with the next 5 years
for i in range(1800):
	now = datetime.datetime.today()
	day = now + datetime.timedelta(i)
	c.execute("INSERT INTO MEALTIMES (DAY,BREAKFAST,LUNCH,DINNER) VALUES (%s,%s,%s,%s)" % default_meals(day) )

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
