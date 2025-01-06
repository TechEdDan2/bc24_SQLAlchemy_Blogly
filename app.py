"""Blogly application."""

from flask import Flask, request, render_template, redirect, session, flash
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['SECRET_KEY'] = "passwordistaco123"
debug = DebugToolbarExtension(app)

# Call the function in models.py
# This creates an application context. This context pushes the current application object onto a stack and makes it accessible within the with block. This is crucial because many Flask extensions and features rely on having the application object available in the current context.
with app.app_context():
    connect_db(app)
    db.create_all()

# --------------------- #
#   Routes for Users    #
# --------------------- #

# GET REQUESTS
@app.route('/')
def home():
    """ For this project the main list of users will be the homepage, so this will redirect site traffic """
    return redirect("/users")

@app.route('/users')
def list_users():
    """ Shows A list of Users """
    users = User.get_all_users()
    return render_template('list.html', users = users)

# POST REQUESTS
@app.route('/users/add', methods=["POST"])
def create_user():
    """ 
    Create a user by pulling data from the  
        new user form and instantiate it using
        the user model
    """
    name_first = request.form["name_first"]
    name_last = request.form["name_last"]
    user_image = request.form["user_image"]

    new_user = User(
        name_first = name_first, 
        name_last = name_last, 
        user_image = user_image or None)

    # Stage the Data
    db.session.add(new_user)

    # Commit to the DB
    db.session.commit()

    return redirect(f"/users/{new_user.id}")


@app.route('/users/add')
def show_add_user_form():
    """ Show the Add User Form """
    return render_template('newUser.html')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    """ Show Details about a single user """
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user = user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('editUser.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.name_first = request.form['first']
    user.name_last = request.form['last']
    user.user_image = request.form['user_image']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# --------------------- #
#   Routes for Posts    #
# --------------------- #

@app.route('/users/<int:user_id>/posts/new')
def get_post_form(user_id):
    """  Show form to add a post for that user. """
    user = User.query.get_or_404(user_id)
    return render_template('addPost.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """ Handle add form; add post and redirect to the user detail page. """
    user = User.query.get_or_404(user_id)
    new_post = Post(title = request.form['title'],
                    content = request.form['content'],
                    user_id = user.id)
    
    # Stage the Data
    db.session.add(new_post)

    # Commit to the DB
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def get_single_post(post_id):
    """ Show a post. Show buttons to edit and delete the post. """

    post = Post.query.get_or_404(post_id)
    return render_template('detailsPost.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def get_edit_post(post_id):
    """ Show form to edit a post, and to cancel (back to user page). """

    post = Post.query.get_or_404(post_id)
    return render_template('editPost.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def submit_edit(post_id):
    """ Handle editing of a post. Update popup. Redirect back to the post view. """ 

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    flash(f"Post named '{post.title}' updated")  

    return redirect(f"/posts/{post_id}")  

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete a single post based on id trigger popup notification """

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash(f"Post named '{post.title}' deleted")  

    return redirect(f"/users/{post.user_id}")




