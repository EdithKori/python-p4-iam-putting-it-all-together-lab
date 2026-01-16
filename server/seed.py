from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    # Relationships
    recipes = relationship("Recipe", backref="user", lazy=True)
    serialize_only = ('id', 'username', 'image_url', 'bio', 'recipes')



    # Serialization rules (hide password hash)
    serialize_rules = ('-recipes.user', '-_password_hash',)

    # Password property
    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes are not viewable.")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')

    def authenticate(self, password):
        """Check if provided password matches stored hash."""
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    # Validations
    @validates("username")
    def validate_username(self, key, username):
        if not username or username.strip() == "":
            raise ValueError("Username must be present.")
        return username





    

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # Serialization rules
    serialize_rules = ('-user.recipes',)
    serialize_only = ('id', 'title', 'instructions', 'minutes_to_complete', 'user')


    # Validations
    @validates("title")
    def validate_title(self, key, title):
        if not title or title.strip() == "":
            raise ValueError("Title must be present.")
        return title

    @validates("instructions")
    def validate_instructions(self, key, instructions):
        if not instructions or instructions.strip() == "":
            raise ValueError("Instructions must be present.")
        if len(instructions.strip()) < 50:
            raise ValueError("Instructions must be at least 50 characters long.")
        return instructions




    
    