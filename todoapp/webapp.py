from flask import Flask, render_template, request, redirect, url_for
from todoapp import todo
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', todos=todo.get_all())

@app.route("/create", methods=['GET'])
def create():
    return render_template('create.html')

@app.route("/create", methods=['POST'])
def create_save():
    text = request.form['text']
    todo.put(text=text, state=todo.TODO_STATES['TODO'], due=None)
    return redirect(url_for('index'))

@app.route("/hello")
def hello():
    return "Hello World!"

if __name__=='__main__':
    app.run(debug=True)
