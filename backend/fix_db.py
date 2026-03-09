import sqlite3

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
try:
    cur.execute("CREATE TABLE IF NOT EXISTS django_site (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, domain varchar(100) NOT NULL UNIQUE, name varchar(50) NOT NULL)")
    cur.execute("INSERT OR IGNORE INTO django_site (id, domain, name) VALUES (1, '127.0.0.1:8000', '127.0.0.1:8000')")
    cur.execute("INSERT OR IGNORE INTO django_migrations (app, name, applied) VALUES ('sites', '0001_initial', '2023-01-01 00:00:00')")
    cur.execute("INSERT OR IGNORE INTO django_migrations (app, name, applied) VALUES ('sites', '0002_alter_domain_unique', '2023-01-01 00:00:00')")
    conn.commit()
    print("Database fixed successfully.")
except Exception as e:
    print("Error:", e)
finally:
    conn.close()
