from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Need this code to meet new version requirements
app.app_context().push()

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for model for Pets."""

    def setUp(self):
        """Clean up any existing pets."""
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    # Unittest for the methods
    def test_full_name(self):
        testUser = User(name_first="TestUser", name_last="One")
        self.assertEquals(testUser.full_name(), "TestUser One")