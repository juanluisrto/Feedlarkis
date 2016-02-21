import sqlite3
conn = sqlite3.connect('larkstadens.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE users_database
(
  user text,
  password text,
  email text,
  privilege integer NOT NULL DEFAULT 0)
''')

# Insert a row of data
c.execute("INSERT INTO users_database VALUES ('gioele','adminpass','gioelelamanno@gmail.com',1)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
