from sqlalchemy import create_engine, text

import os, random

# FOLLOW FROM THIS DOCUMENT
# https://docs.sqlalchemy.org/en/20/dialects/mysql.html

# we have to create a engine to import mysql database

# we hide our db username, pass string in Db_Connections as we do not want to show this on github
db_connection_string = os.environ['DB_Connections']

engine = create_engine(
  db_connection_string,
  connect_args={
    "ssl":{ # ssl is used for more secure connection
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  }
)

def Load_Jobs_From_DB():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    JOBS = []
  
    # print(type(result))
    # to convert DB rows as dict use ._asdict() v imp
    for row in result.all():
       JOBS.append(row._asdict())
      
    return JOBS


def load_users():
  with engine.connect() as conn:
    result = conn.execute(text("select * from users"))
    Users = []
  
    # print(type(result))
    # to convert DB rows as dict use ._asdict() v imp
    for user in result.all():
       Users.append(user._asdict())
      
    return Users
  

def check_valid_user(type, email, password):
  with engine.connect() as conn:
    result = conn.execute(text((""" select * from {} where email = "{}" and password = "{}" """).format(type,email,password)))
    users = []
    
      # print(type(result))
      # to convert DB rows as dict use ._asdict() v imp
    for row in result.all():
      users.append(row._asdict())
        
    return users
  
def register_new_user(type, name, email, password):
  with engine.connect() as conn:
    conn.execute(text((""" insert into {} (name, email, password) VALUES ('{}', '{}', '{}') """).format(type,name,email,password)))


def add_job_to_DB(title, location, salary, currency, responsibilities, requirements):
  with engine.connect() as conn:
    conn.execute(text((""" insert into jobs (`title`, `location`, `salary`, `currency`, `responsibilities`, `requirements`) VALUES ('{}', '{}', '{}','{}', '{}', '{}') """).format(title, location, salary, currency, responsibilities, requirements)))

def get_job():
  with engine.connect() as conn:
    result = conn.execute(text(""" select * from jobs """))
    job = []
    
      # print(type(result))
      # to convert DB rows as dict use ._asdict() v imp
    for row in result.all():
      job.append(row._asdict())
        
    return job