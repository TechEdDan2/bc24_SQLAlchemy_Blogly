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

    def test_create_user(self):
        user = User(name_first="John", name_last="Doe")
        db.session.add(user)
        db.session.commit()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.name_first, "John")
        self.assertEqual(user.name_last, "Doe")
    
    def test_update_user(self):
        user = User(name_first="John", name_last="Doe")
        db.session.add(user)
        db.session.commit()

        user.name_first = "Jane"
        db.session.commit()

        updated_user = User.query.get(user.id)
        self.assertEqual(updated_user.name_first, "Jane")

    def test_delete_user(self):
        user = User(name_first="John", name_last="Doe")
        db.session.add(user)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        deleted_user = User.query.get(user.id)
        self.assertIsNone(deleted_user)