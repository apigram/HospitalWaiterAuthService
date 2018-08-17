from app import app, token_auth, db
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import bcrypt


class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)

    def __repr__(self):
        return '<Patient {}>'.format(self.first_name + ' ' + self.last_name)

    def jsonify(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(3000))
    email = db.Column(db.String(100))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    patient = db.relationship('Patient')

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config.get('SECRET_KEY'), expires_in=expiration)
        return s.dumps({'id': self.id, 'patient_id': self.patient_id})

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config.get('SECRET_KEY'))
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    @staticmethod
    @token_auth.verify_token
    def verify_token(token):
        # first try to authenticate by token
        user = User.verify_auth_token(token)
        if not user:
            return False
        return True
