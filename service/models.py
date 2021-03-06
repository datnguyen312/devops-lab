# Copyright 2016, 2019 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Models for Pet Demo Service

All of the models are stored in this module

Models
------
Pet - A Pet used in the Pet Store

Attributes:
-----------
name (string) - the name of the pet
category (string) - the category the pet belongs to (i.e., dog, cat)
available (boolean) - True for pets that are available for adoption

"""
import logging
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class Pet(db.Model):
    """
    Class that represents a Pet

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger('flask.app')
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    category = db.Column(db.String(63))
    available = db.Column(db.Boolean())

    def __repr__(self):
        return '<Pet %r>' % (self.name)

    def save(self):
        """
        Saves a Pet to the data store
        """
        Pet.logger.info('Saving %s', self.name)
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes a Pet from the data store """
        Pet.logger.info('Deleting %s', self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Pet into a dictionary """
        return {"id": self.id,
                "name": self.name,
                "category": self.category,
                "available": self.available}

    def deserialize(self, data):
        """
        Deserializes a Pet from a dictionary

        Args:
            data (dict): A dictionary containing the Pet data
        """
        try:
            self.name = data['name']
            self.category = data['category']
            self.available = data['available']
        except KeyError as error:
            raise DataValidationError('Invalid pet: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid pet: body of request contained' \
                                      'bad or no data')
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        cls.logger.info('Initializing database')
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Pets in the database """
        cls.logger.info('Processing all Pets')
        return cls.query.all()

    @classmethod
    def find(cls, pet_id):
        """ Finds a Pet by it's ID """
        cls.logger.info('Processing lookup for id %s ...', pet_id)
        return cls.query.get(pet_id)

    @classmethod
    def find_or_404(cls, pet_id):
        """ Find a Pet by it's id """
        cls.logger.info('Processing lookup or 404 for id %s ...', pet_id)
        return cls.query.get_or_404(pet_id)

    @classmethod
    def find_by_name(cls, name):
        """ Returns all Pets with the given name

        Args:
            name (string): the name of the Pets you want to match
        """
        cls.logger.info('Processing name query for %s ...', name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category):
        """ Returns all of the Pets in a category

        Args:
            category (string): the category of the Pets you want to match
        """
        cls.logger.info('Processing category query for %s ...', category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available=True):
        """ Query that finds Pets by their availability """
        """ Returns all Pets by their availability

        Args:
            available (boolean): True for pets that are available
        """
        cls.logger.info('Processing available query for %s ...', available)
        return cls.query.filter(cls.available == available)
