"""Blogly application."""

from flask import Flask, request, render_template, redirect, session, flash
from models import db, connect_db, User, Post, Tag, PostTag
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
    tags = Tag.query.all()
    return render_template('addPost.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """ Handle add form; add post and redirect to the user detail page. """
    user = User.query.get_or_404(user_id)
    new_post = Post(title = request.form['title'],
                    content = request.form['content'],
                    user_id = user.id)
    
    # Stage the Data
    db.session.add(new_post)
    db.session.commit()

    # Handle tags
    tag_ids = request.form.getlist('tags')
    for tag_id in tag_ids:
        tag = Tag.query.get(tag_id)
        new_post.tags.append(tag)

    # Commit to the DB
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def get_single_post(post_id):
    """ Show a post. Show buttons to edit and delete the post. """

    post = Post.query.get_or_404(post_id)
    post_tags = post.tags
    return render_template('detailsPost.html', post=post, post_tags=post_tags)

@app.route('/posts/<int:post_id>/edit')
def get_edit_post(post_id):
    """ Show form to edit a post, and to cancel (back to user page). """

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('editPost.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """ Handle editing of a post. Update form. """

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = request.form.getlist('tags')
    post.tags = [Tag.query.get(tag_id) for tag_id in tag_ids]

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route('/posts/all')
def list_all_posts():
    """ Show all posts """

    posts = Post.query.all()
    return render_template('listAllPosts.html', posts=posts)

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


# --------------------- #
#   Routes for Tags     #
# --------------------- #

@app.route('/tags')
def list_tags():
    """ Show all tags """

    tags = Tag.query.all()
    return render_template('listAllTags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """ Show detail about a tag. Have links to edit form and to delete. """

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tagWithPosts.html', tag=tag)

@app.route('/tags/new')
def add_tag_form():
    """ Show a form to add a new tag. """

    return render_template('addTag.html')

@app.route('/tags/new', methods=["POST"])
def create_tag():
    """ Handle form submission for creating a new tag. """

    name = request.form['name']
    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """ Show form to edit a tag. """

    tag = Tag.query.get_or_404(tag_id)
    return render_template('editTag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def update_tag(tag_id):
    """ Handle form submission for updating an existing tag. """

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """ Delete a tag. Should be redirected to /tags """

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')