# Blogly: A Flask User Blogging Application

Blogly is a simple Flask application that allows users to create, view, edit, and delete user accounts 

## Table of Contents
- [Overview](#overview)
  - [Features](#features)
  - [Screenshot](#screenshot)
- [Getting Started](#getting-started)
  - [Built with](#built-with)
  - [What I learned](#what-i-learned)
  - [Continued development](#continued-development)
  - [Useful resources](#useful-resources)
- [Author](#author)
- [Acknowledgments](#acknowledgments)

## Overview

### Features:

- User accounts with profile information (name and image)
- List of all users
- User detail page
- Create new user
- Edit user information
- Delete user

## Getting Started:

1. **Prerequisites:**
   - Python 3
   - pip (package installer for Python)

2. **Installation:**

   - Clone this repository.
   - Navigate to the project directory in your terminal.
   - create a virtual environment python3 -m venv venv
   - Install required dependencies:

     ```
     pip install -r requirements.txt
     ```

3. **Configuration:**

   - Update the database URI in `app.config['SQLALCHEMY_DATABASE_URI']` to point to your desired PostgreSQL database.

4. **Database Setup:**

   - Create a PostgreSQL database.
   - Run the following command to create the database tables (assuming your database name is `blogly_db`):

     ```bash
     python app.py
     ```

     **Note:** This will only create the tables on the first run. Subsequent runs won't recreate them unless you explicitly drop the tables first.

5. **Running the Application:**

   - Start the development server:

     ```bash
     python app.py
     ```

   - This will run the Flask development server on `http://127.0.0.1:5000/` by default. You can access the application in your web browser.

**Usage:**

1. **Visit `http://127.0.0.1:5000/users`** to see a list of all users.
2. **Click on a user's name** to view their details.
3. **Click on the "Add User" button** to create a new user.
4. **Fill out the form** with the user's name and optional image URL.
5. **Click on the "Edit" button** on a user's detail page to edit their information.
6. **Click on the "Delete" button** on a user's detail page to delete the user (**Warning:** This action cannot be undone).

### Built with

- HTML
- CSS
- Jinja
- Bootstrap
- Python
- Flask
- SQLAlchemy

### Continued development
- This is a basic user management application and doesn't include features like user authentication, password management, or blog post creation in the first version of the app.
- In the next update I hope to add more features and functionalities.

### Useful resources
- [MDN](https://developer.mozilla.org/en-US/) - As always, I used the MDN resource when I had a quick question.
- [JinjaDocs] (https://jinja.palletsprojects.com/en/stable/templates/) - I used this to help with creating templates for my pages. 
- [Bootstrap] (https://getbootstrap.com/docs/5.3/getting-started/introduction/) - I used these docs for some of the styling
- [FlaskSQLAlchemy] (https://flask-sqlalchemy.readthedocs.io/en/stable/) - Help with using Flask-SQLAlchemy

## Author
- Github - [DNel2](https://github.com/TechEdDan2)
- Frontend Mentor - [@TechEdDan2](https://www.frontendmentor.io/profile/TechEdDan2)
- Twitter - [@TechEdDan](https://twitter.com/TechEdDan)

## Acknowledgments
The YouTubers and other educational resources I have been learning from include: Coder Coder (Jessica Chan), BringYourOwnLaptop (Daniel Walter Scott), Udemy and Bootcamp (Colt Steele)  
