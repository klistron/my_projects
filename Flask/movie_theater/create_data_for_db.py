import random
from datetime import date, time

from re import S
from webapp import create_app

from webapp.db import db
from webapp.main.models import Hall, Showtime, Seats

app = create_app()


def create_halls():
    standard = Hall(hall_name="Standard")
    vip = Hall(hall_name="VIP")

    db.session.add(standard)
    db.session.add(vip)
    db.session.commit()


def create_seats():
    hall = db.session.query(Hall).filter_by(hall_name="Standard").first()
    count_seats = 7
    coefficient = 0.7
    for row in range(1, 8):
        print(row)
        seats = []
        for seat in range(count_seats):
            seats.append(False)
        print(seats)
        hall_seats = Seats(
            hall_id=hall.id, row=row, seats=seats, coefficient_price=coefficient
        )
        db.session.add(hall_seats)
        db.session.commit()
        count_seats += 2
        coefficient += 0.1

    vip_hall = db.session.query(Hall).filter_by(hall_name="VIP").first()
    vip_seats = Seats(hall_id=vip_hall.id, row=1, seats=[False], coefficient_price=1.0)
    db.session.add(vip_seats)
    db.session.commit()


def create_showtimes():
    times = [
        "10:00:00",
        "12:00:00",
        "14:00:00",
        "16:00:00",
        "18:00:00",
        "20:00:00",
        "22:00:00",
    ]
    hall = db.session.query(Hall).filter_by(hall_name="Standard").first()
    free_seats = db.session.query(Seats).filter_by(hall_id=hall.id).all()
    all_seats = []
    for seats in free_seats:
        all_seats.append(seats.seats)
    print(all_seats)

    for time in times:
        showtime = Showtime(
            movie_id=random.randint(7, 16),
            hall_id=1,
            date=date.today(),
            time=time,
            seats=all_seats,
            price=500.00,
        )
        db.session.add(showtime)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        # create_halls()
        # create_seats()
        create_showtimes()
