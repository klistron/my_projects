from datetime import date, datetime
from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.sql import func
from webapp.db import db
from webapp.libs.chek_card import validate_card_expiry, validate_card_number, validate_cvv
from .models import Movie, Showtime, Order, Seats

import json


blueprint = Blueprint("main", __name__)


@blueprint.route("/")
def index():
    random_movies = (
        Movie.query.options(joinedload(Movie.showtimes))
        .order_by(func.random())
        .limit(3)
        .all()
    )
    showtimes = Showtime.query.limit(6).all()
    return render_template("main/index.html", movies=random_movies, showtimes=showtimes)


@blueprint.route("/showtime/<int:showtime_id>")
def showtime_detail(showtime_id):
    showtime = Showtime.query.options(joinedload(Showtime.movie)).get_or_404(
        showtime_id
    )
    return render_template(
        "main/theatre-area.html", showtime=showtime, current_user=current_user
    )


@blueprint.route("/order/<int:order_id>")
def order(order_id):
    order = Order.query.get_or_404(order_id)
    showtime = Showtime.query.get(order.showtime_id)
    if order.seats[0]['row'] == 'VIP-hall':
        return render_template("main/order.html", order=order, price=round(float(order.showtime.price), 2))
    total_price = Decimal(0)
    for seat in order.seats:
        seats = Seats.query.filter_by(hall_id=showtime.hall_id, row=seat['row']).first()
        total_price += Decimal(seats.coefficient_price) * showtime.price
    order.total_price = total_price    
    db.session.commit()
    return render_template("main/order.html", order=order, price=round(float(total_price), 2))

@blueprint.route("/submit-seats", methods=["POST"])
def submit_seats():
    if not current_user.is_authenticated:
        flash('Для оформления заказа необходимо авторизоваться!', 'warning')
        return redirect(url_for("user.login"))
    selected_seats = request.form.get("selectedSeats")
    selected_seats_list = json.loads(selected_seats)
    if len(selected_seats_list) > 0:
        showtime_id = request.form.get("showtime_id")
        order = Order(user_id=current_user.id, showtime_id=showtime_id, status_id=2, seats=selected_seats_list, datetime=datetime.now())
        showtime = Showtime.query.get(showtime_id)
        
        for seat in selected_seats_list:
            showtime.seats[int(seat["row"]) - 1][int(seat["seat"]) - 1] = True
        flag_modified(showtime, "seats")
        db.session.add(order)
        db.session.add(showtime)
        db.session.commit()
        
        return redirect(url_for("main.order", order_id=order.id))
    else:
        flash('Для заказа билета выберите места!', 'warning')
        return redirect(url_for("main.index"))
    

@blueprint.route('/check-card', methods=['POST'])
def check_card():
    card_number = request.form.get('cardNumber')
    card_expiry = request.form.get('cardExpiry')
    card_cvv = request.form.get('cardCVV')
    order_id = request.form.get('order_id')
    order = Order.query.get(order_id)
        
    if not validate_card_number(card_number):
        flash('Неверный номер карты!', 'warning')
        return redirect(url_for("main.order", order_id=order.id)) 

    if not validate_card_expiry(card_expiry):
        flash('Неверный срок действия карты!', 'warning')
        return redirect(url_for("main.order", order_id=order.id)) 

    if not validate_cvv(card_cvv):
        flash('Неверный CVV', 'warning')
        return redirect(url_for("main.order", order_id=order.id))

    # Здесь должна быть логика проверки данных карты через платежный шлюз

    order = Order.query.get(order_id)
    order.status_id = 3
    db.session.commit()
    
    flash('Заказ оплачен!', 'success')
    return redirect(url_for("user.user_page"))

@blueprint.route("/book_vip")
def book_vip():
    movies = Movie.query.order_by(Movie.id.desc()).limit(5).all()
    return render_template("main/book_vip.html", movies=movies)

@blueprint.route("/submit_vip", methods=["POST"])
def submit_vip():
    if not current_user.is_authenticated:
        flash('Для оформления заказа необходимо авторизоваться!', 'warning')
        return redirect(url_for("user.login"))
    movie_id = request.form.get("movieSelect")
    datetime_show = request.form.get("datePicker").split("T")
    if not movie_id:
        flash('Для оформления заказа необходимо выбрать сеанс !', 'warning')
        return redirect(url_for("main.book_vip"))        
    if not datetime_show:
        flash('Для оформления заказа необходимо выбрать дату и время !', 'warning')
        return redirect(url_for("main.book_vip")) 
    date_show = datetime.strptime(datetime_show[0], '%Y-%m-%d')
    time_show = datetime.strptime(datetime_show[1], '%H:%M')
    date_now = datetime.now()
    if date_show < date_now:
        flash('Для оформления заказа необходимо выбрать дату позднее сегодняшнего дня !', 'warning')
        return redirect(url_for("main.book_vip"))
    showtime = Showtime(movie_id=movie_id, date=date_show, time=time_show, hall_id=2, seats=[[True]], price=10000)
    db.session.add(showtime)
    db.session.commit()
    order = Order(user_id=current_user.id, showtime_id=showtime.id, status_id=2, seats=[{"row": 'VIP-hall', "seat": showtime.movie.title}], datetime=datetime.now())
    db.session.add(order)
    db.session.commit()
    return redirect(url_for("main.order", order_id=order.id))
