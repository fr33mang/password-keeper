from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    storage = db.relationship('Password', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Password(db.Model):
    __tablename__ = 'password'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(225))
    login = db.Column(db.String(64))
    password = db.Column(db.String(64))
    url = db.Column(db.String(225))

    owner = db.Column(db.Integer, db.ForeignKey('users.id'),
                      nullable=False)

    def __repr__(self):
        return '<Password %r>' % self.title
