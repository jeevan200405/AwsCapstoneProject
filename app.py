from flask import Flask, render_template, request, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import boto3
import os
from botocore.exceptions import ClientError
from werkzeug.middleware.proxy_fix import ProxyFix
# remove comment when get dynamodb working
# import key_config as keys
# import boto3

app = Flask(__name__)

# AWS SECURITY SETTINGS
#AWS Load BAlancer

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config['PREFERRED_URL_SCHEME'] = 'https'

# Must be set in AWS environment variables

app.secret_key = os.environ.get("FLASK_SECRET_KEY","dev-secret")

# AWS SERVICES CONFIGURATION

SESSION_COOKIE_SECURE = True if os.environ.get("ENV") == "prod" else False

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=SESSION_COOKIE_SECURE,
    PERMANENT_SESSION_LIFETIME=3600
)

# DATABASE CONNECTION
# remove 8 comment when get dynamodb working
# DynamoDB connection
# dynamodb = boto3.resource('dynamodb',
#     region_name='ap-south-1',
#     aws_access_key_id=keys.ACCESS_KEY_ID,
#     aws_secret_access_key=keys.ACCESS_SECRET_KEY,
#     aws_session_token=keys.AWS_SESSION_TOKEN,
# )


# table = dynamodb.Table('users')


AWS_REGION = os.environ.get('AWS_REGION',"us-east-1")

# IAM Role Authentication
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
users_table = dynamodb.Table("cinemy_users")
admin_table = dynamodb.Table("cinemy_admins")
sns = boto3.client("sns", region_name=AWS_REGION)
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")


# LOGIN PROTECTION

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first ❗")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin"))
        return f(*args, **kwargs)
    return decorated

# ROUTES

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")
    
@app.route("/health")
def health():
    return "OK", 200

# SIGN UP

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("All fields required ❌")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)

        try:
            users_table.put_item(
                Item={
                    "email": email,
                    "name": name,
                    "password": hashed_password
                },
                ConditionExpression="attribute_not_exists(email)"
            )
            
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f"New user signup: {email}",
                Subject="New Registration"
            )

            session["user_id"] = email
            session["user_name"] = name
            session.permanent = True

            flash("Signup Successful 🎉")
            return redirect(url_for("home"))


        except ClientError as e:

            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                flash("Email already exists ❌")
            else:
                flash("AWS Error ❌")

            return redirect(url_for("signup"))

    return render_template("signup.html")

# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        try:
            response = users_table.get_item(Key={"email": email})
            user = response.get("Item")

            if user and check_password_hash(user["password"], password):

                session["user_id"] = user["email"]
                session["user_name"] = user["name"]
                session.permanent = True


                flash("Login Successful 🎉")
                return redirect(url_for("home"))

            else:
                flash("Invalid credentials ❌")
                return redirect(url_for("login"))

        except ClientError:
            flash("AWS Error ❌")
            return redirect(url_for("login"))

    return render_template("login.html")

# ADMIN LOGIN PAGE

@app.route("/admin", methods=["GET", "POST"])
def admin():

    # Already logged in admin
    if "admin" in session:
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        try:
            response = admin_table.get_item(Key={"username": username})

            if "Item" not in response:
                flash("Admin not found ❌")
                return redirect(url_for("admin"))

            admin = response["Item"]

            if check_password_hash(admin["password"], password):

                session["admin"] = username
                session.permanent = True

                flash("Admin Login Successful ✅")
                return redirect(url_for("admin_dashboard"))

            else:
                flash("Wrong password ❌")

        except ClientError:
            flash("AWS Error ❌")

    return render_template("admin.html")


# ADMIN DASHBOARD

@app.route("/admin-dashboard")
@admin_required
def admin_dashboard():
    return render_template("admin-dashboard.html")


@app.route("/admin/add-movie", methods=["POST"])
@admin_required
def add_movie():

    data = request.json

    movies_table = dynamodb.Table("movies")

    movies_table.put_item(Item=data)

    return {"message": "Movie Added Successfully"}


@app.route("/admin/get-movies")
@admin_required
def get_movies():

    movies_table = dynamodb.Table("movies")

    response = movies_table.scan()

    return response["Items"]


@app.route("/admin/delete-movie", methods=["POST"])
@admin_required
def delete_movie():

    name = request.json["name"]

    movies_table = dynamodb.Table("movies")

    movies_table.delete_item(Key={"name": name})

    return {"message": "Movie Deleted Successfully"}


@app.route("/admin/get-users")
@admin_required
def get_users():

    response = users_table.scan()

    return response["Items"]


# LOGOUT

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully 👋")
    return redirect(url_for("home"))

# AWS SERVER START

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

