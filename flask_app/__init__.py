from flask import Flask
app = Flask(__name__)
app.secret_key = 'nosecret_here'

DATABASE = 'todos_python_schema'
