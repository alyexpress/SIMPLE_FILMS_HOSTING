from flask import Flask, render_template
from film_parse import FilmParse

#DEL
from pprint import pprint
from time import sleep

app = Flask(__name__)
fp = FilmParse()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/film')
def film1():
    return render_template("index_copy.html")

@app.route('/search/<query>')
def search(query):
    data = fp.search_kinovod(query)
    return render_template("search.html", query=query, data=data)

@app.route('/film/<link>')
def film(link):
    data = fp.get_info_kinovod(f"https://kinovod.pro/film/{link}")
    return render_template("film.html", data=data)

@app.route('/link/<link>')
def path(link):
    return fp.get_kinovod(f"https://kinovod.pro/film/{link}")

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)