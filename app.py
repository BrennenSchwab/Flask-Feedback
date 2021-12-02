from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, RemoveForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ghdjdydychfcytvtfk"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

@app.route("/")
def root():
    """redirects root page to register """

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():
    """register and create a user when the form is submitted correctly"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)
        db.session.commit()
        session["username"] = user.username

        return redirect(f"/users/{user.username}")
    else:
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Show a form that when submitted will login a user. 
    This form should accept a username and a password."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")
    

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Invalid username or password"]
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """user logout"""

    session.pop("username")
    return redirect("/register")

@app.route("/users/<username>")
def registered_user(username):
    """registered user page"""

    if "username" not in session or username!=session['username']: 
        raise Unauthorized()

    user = User.query.get(username)
    form = RemoveForm()
    return render_template("user.html", user=user, form=form) 


@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user and direct to root '/'"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """add feedback form"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback_add.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """update feedback form hand handle updates"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("feedback_edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """delete the specific feedback"""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = RemoveForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
