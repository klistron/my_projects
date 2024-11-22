"""
Скачивает информацию о фильмах и сохраняет в базу данных.
Также сохраняет изображения постеров, нужно предварительно создать папку "webapp/static/images"
"""

import os
import requests

from bs4 import BeautifulSoup
from webapp import create_app
from webapp.db import db
from webapp.main.models import Movie

app = create_app()


def get_html(url: str):
    try:
        response = requests.get(url, verify=False, timeout=10)
        response.raise_for_status()
        return response.text
    except (requests.RequestException, requests.HTTPError, ValueError) as e:
        print("Сетевая ошибка", e)
        return False


def download_image(url: str, image_path: str):
    try:
        response = requests.get(url, stream=True, verify=False, timeout=10)
        if response.status_code == 200:
            with open(image_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
        else:
            print(
                f"Не удалось загрузить изображение. Статус код: {response.status_code}"
            )
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def get_cinema_info(html, url_number, static_dir):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("h1", class_="film-info__title").text
    nav_items = soup.find(
        "ul", class_="nav cinema__film__tags cinema__film__tags--v2"
    ).find_all("li")
    age_rating = nav_items[0].find("span", class_="cinema__film__tags__item").text
    date = soup.find(
        "div", class_="col-lg-8 film-info__metadate__item__value"
    ).text.strip()
    film_info = soup.find("div", class_="film-info__params").text.split("|")
    film_info = [i.strip() for i in film_info]
    duration_text = film_info[2]
    duration = int(duration_text.split()[0]) * 60 + int(duration_text.split()[2])
    genre = film_info[1]
    counry = film_info[0]
    description = soup.find("div", class_="cinema__text").text.strip()
    image = soup.find("div", class_="film-single__poster").find("img")["data-src"]
    img_path = os.path.join(static_dir, "images", f"{url_number}.jpg")
    download_image(image, img_path)

    return {
        "title": title,
        "age_rating": age_rating,
        "year": int(date.split()[2]),
        "duration": duration,
        "genre": genre,
        "counry": counry,
        "description": description,
        "img_url": f"/static/images/{url_number}.jpg",
    }


def get_static():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)
    static_dir = os.path.join(current_dir, "webapp", "static")
    return static_dir


def save_to_db(data):
    movie = Movie(**data)
    db.session.add(movie)
    db.session.commit()


if __name__ == "__main__":
    static_dir = get_static()
    url_number = 339
    for _ in range(10):
        url = f"https://mori.film/movie/{url_number}"
        html = get_html(url)
        if html:
            with app.app_context():
                movie = get_cinema_info(html, url_number, static_dir)
                save_to_db(movie)

        url_number -= 1
