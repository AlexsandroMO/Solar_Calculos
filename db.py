#from tinymongo import TinyMongoClient
from tinydb import TinyDB, Query

db = TinyDB('DB_JSON/db.json')

#===============================
#Cadastro Usuários
#===============================

def registerDB(firstname, lastname, email1, password1):
  return db.insert({'FIRST_NAME':firstname,'LAST_NAME':lastname,'EMAIL':email1,'PASSWORD':password1})

#print(db.all())

Ft = Query()

def query_email_confere(email, password):
  new_db = db.search(Ft.EMAIL == email and Ft.PASSWORD == password)
  
  return new_db
