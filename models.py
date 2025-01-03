"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

# Connect the app to the db
db = SQLAlchemy()

# function to connect
def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_USER_IMG = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"

# ----------- #
#   Models    #
# ----------- #

class User(db.Model):
    """User Schema Table"""

    __tablename__ = "users"

    # Attributes
    id = db.Column(db.Integer, 
                   primary_key = True,
                   autoincrement = True)
    
    name_first = db.Column(db.String(50),
                     nullable = False)
    
    name_last = db.Column(db.String(50),
                     nullable = False)
    
    user_image = db.Column(db.Text,
                        nullable = False,
                        default = DEFAULT_USER_IMG)

    # Custom printout which overrides the original 
    def __repr__(self):
        """ 
        Returns a string representation of the User object. This method 
            provides a concise and informative representation of the User 
            object, useful for debugging and logging purposes.
        
        Returns:
            str: A string representation of the User object in the format:
                <User id=<id> first name = <name_first> Last Name = <name_last> Image URL = <user_image>> 
        """
        u = self
        return f"<User id={u.id} First Name = {u.name_first} Last Name = {u.name_last} Image URL = {u.user_image}>"

    @classmethod
    def get_all_users(cls):
        """ Retrieves a list of all active users """
        return cls.query.all()
    

    # Instance Methods
    def full_name(self):
        """ Returns the user's full name """
        return f"{self.name_first} {self.name_last}"