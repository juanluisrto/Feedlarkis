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
c.execute('''INSERT INTO USERS_DATA (USER, NAME, SURNAME, PASSWORD, EMAIL, PRIVILEGE, AUTHORIZED)
	VALUES ('gioelelm', 'Gioele', 'La Manno', 'adminpass','gioelelamanno@gmail.com',1,1);''')

# Create table
c.execute('''CREATE TABLE BOOKINGS(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  USER TEXT,
  SUBMISSION_TIME TEXT NOT NULL,
  BOOKING_DAY TEXT NOT NULL,
  MEAL TEXT NOT NULL,
  TYPE TEXT NOT NULL DEFAULT "-",
  MESSAGE TEXT)
''')

# Insert a row of data
#c.execute("INSERT INTO BOOKINGS VALUES ()")

# Create table
c.execute('''CREATE TABLE MEALTIMES(
  DAY TEXT PRIMARY KEY NOT NULL,
  BREAKFAST_START TEXT NOT NULL,
  BREAKFAST_END TEXT NOT NULL,
  LUNCH TEXT NOT NULL,
  FIKA_START TEXT NOT NULL,
  FIKA_END TEXT NOT NULL,
  DINNER TEXT NOT NULL,
  MESSAGE TEXT DEFAULT "")
''')

def default_meals(dateobj):
    day = dateobj.strftime('%A - %d %B %Y')
    if dateobj.strftime('%A') in ['Saturday','Sunday']:
        breakfast_start = '7:45'
        breakfast_end = '10:15'
        lunch = '13:00'
        fika_start = '16:00'
        fika_end = '18:00'
        dinner = '19:30'
    else:
        breakfast_start = '6:45'
        breakfast_end = '9:30'
        lunch = '12:15'
        fika_start = '15:30'
        fika_end = '18:00'
        dinner = '19:30'
        
    return day, breakfast_start, breakfast_end, lunch, fika_start, fika_end, dinner

#Prefill with the next 5 years
for i in range(1800):
	now = datetime.datetime.today()
	day = now + datetime.timedelta(i)
	c.execute("INSERT INTO MEALTIMES (DAY, BREAKFAST_START, BREAKFAST_END, LUNCH, FIKA_START, FIKA_END, DINNER) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % default_meals(day) )

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
