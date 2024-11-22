from sqlalchemy.orm import relationship

from webapp.db import db



class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    age_rating = db.Column(db.String(10), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    counry = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    showtimes = relationship("Showtime", back_populates="movie")

    def __repr__(self):
        return f"<Movie {self.title}>"


class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey("hall.id"), nullable  =False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    seats = db.Column(db.JSON, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    hall = relationship("Hall", back_populates="showtimes")
    movie = relationship("Movie", back_populates="showtimes")
    orders = db.relationship('Order', back_populates='showtime')

    def __repr__(self):
        return f"<Showtime: {self.date}> {self.time} - {self.movie}"

class Hall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hall_name = db.Column(db.String(100), nullable=False)

    seats = relationship("Seats", back_populates="hall")
    showtimes = relationship("Showtime", back_populates="hall")

    def __repr__(self):
        return f"<Hall: {self.hall_name}>"


class Seats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hall_id = db.Column(db.Integer, db.ForeignKey("hall.id"), nullable=False)
    row = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.JSON, nullable=False)
    coefficient_price = db.Column(db.REAL, nullable=False)

    hall = relationship("Hall", back_populates="seats")

    def __repr__(self):
        return f"<Seats: {self.hall_id}>"
    
class OrderStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(100), nullable=False)

    orders = relationship("Order", back_populates="status")

    def __repr__(self):
        return f"<OrderStatus: {self.name}>"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey("showtime.id"), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("order_status.id"), nullable=False)
    payment_type = db.Column(db.String(100), nullable=False, default="Online")
    seats = db.Column(db.JSON)
    datetime = db.Column(db.DateTime, default=db.func.now())

    user = relationship("User", back_populates="orders")
    tickets = relationship("Ticket", back_populates="order")
    showtime = relationship("Showtime", back_populates="orders")
    status = relationship("OrderStatus", back_populates="orders")

    def __repr__(self):
        return f"<Order: {self.user_id}>"


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    row = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    order = relationship("Order", back_populates="tickets")

    def __repr__(self):
        return f"<Ticket: {self.order_id}>"
