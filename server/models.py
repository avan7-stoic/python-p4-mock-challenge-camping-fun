from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    difficulty = db.Column(db.Integer(50), nullable=False)

    signups = db.relationship ('Signup', back_populates='activity', cascade='all, delete-orphan')
    camper = db.relationship ('Camper', secondary='signups', back_populates='activities')

    # Add relationship

    serialize_rules = ('-signups.activity', '-campers.activities')
    
    # Add serialization rules
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    signups = db.relationship('Signup', back_populates='camper', cascade='all, dlete-orphan')
    activities = db.relationship('Activity', seconadary='signups', back_populates='campers')

    # Add relationship
    
    # Add serialization rules
    serialize_rules = ('-signups.camper', '-activities.campers')
    
    # Add validation
    def validate_age(self, key, value):
        if value < 8 or value > 18:
            raise ValueError('Age must be between 8 and 18.')
        return value
    
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    # Add relationships
    
    # Add serialization rules
    
    # Add validation
    
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
