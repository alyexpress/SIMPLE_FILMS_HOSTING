from flask import Flask, render_template, request, redirect, jsonify
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

@app.route('/search', methods=['GET'])
def to_search():
    query = request.args.get("query")
    return redirect(f"/search/{query}")

@app.route('/search/<query>')
def search(query):
    data = fp.search_kinovod(query)
    return render_template("search.html", query=query, data=data)

@app.route('/film/<link>')
def film(link):
    data, serial = fp.get_info_kinovod(f"https://kinovod.pro/film/{link}")
    if serial:
        return redirect(f"/serial/{link}")
    for field in "Жанр Страна Режиссер Актеры".split():
        if field not in data.keys():
            data[field] = ""
    return render_template("film.html", data=data)

@app.route('/serial/<link>')
def serial(link):
    data, _ = fp.get_info_kinovod(f"https://kinovod.pro/film/{link}")
    for field in "Жанр Страна Режиссер Актеры".split():
        if field not in data.keys():
            data[field] = ""
    return render_template("serial.html", data=data)

@app.route('/link/<link>')
def path(link):
    return fp.get_kinovod(f"https://kinovod.pro/film/{link}")

@app.route('/serial/<link>/api/s<int:s>e<int:e>')
def serial_api(link, s, e):
    url = f"https://kinovod.pro/serial/{link}"
    data = fp.get_kinovod_serials(url, s, e)
    titles = ["src", "seasons", "episodes"]
    return jsonify(dict(zip(titles, data)))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)