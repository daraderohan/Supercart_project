from test import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(30), nullable=False)
    cart_items=db.relationship('Cart_items',backref='user',lazy=True)
    def __repr__(self):
        return f"User('{self.username}','{self.password}')"


class Cart_items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True, nullable=False)
    price = db.Column(db.String(10), nullable=False)
    threshold_price=db.Column(db.Integer,nullable=False,default=0)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Cart_items('{self.name}','{self.price}')"
