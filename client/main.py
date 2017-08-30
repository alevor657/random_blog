from flask import Flask, render_template, redirect, url_for, abort
from requests import get
app = Flask(__name__)

with open('api_url.txt', 'r', encoding = 'utf-8') as file:
    api_url = file.read() 
@app.route('/')
def hello():
    return redirect(url_for('home'))

@app.route('/post/<int:id>')
def show_post(id):
    r = get(api_url + 'posts/get/' + str(id))
    try:
        post = r.json()
    except:
        abort(404)
    return render_template('post.html', post = post)

@app.route('/home')
def home():
    posts = get(api_url + 'posts/get')
    categories = get(api_url + 'categories/get')
    return render_template('home.html', posts = posts.json(), categories = categories.json())

@app.route('/categories')
def categories():
    return redirect(url_for('soon'))

@app.route('/about')
def about():
    return redirect(url_for('soon'))

@app.route('/soon')
def soon():
    return render_template('soon.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
