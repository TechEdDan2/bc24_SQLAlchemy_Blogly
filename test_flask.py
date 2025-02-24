from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Need this...yes? 
app.app_context().push()

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """ Tests the views for Users """
    def setUp(self):
        """ Add a sample user to the db """
        User.query.delete()

        test_user = User(name_first="TestUser", name_last="One")

        db.session.add(test_user)
        db.session.commit()

        self.user_id = test_user.id
    
    def tearDown(self):
        """Clean up any transactions."""
        db.session.rollback()

    def test_list_of_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser", html)
    
    def test_show_user(self):
        """ Test the user detail page """
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 id="user_full_name">TestUser One</h1>', html)

    def test_add_user(self):
        """ Test the user add page"""
        with app.test_client() as client:
            testUser = {"name_first": "TestUser2", "name_last": "Two", "user_img": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"}
            resp = client.post("/", data=testUser, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestPet2</h1>", html)
