from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
import os

app = Flask(__name__)
CORS(app)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Admin(db.Model):
    __tablename__="admin"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(24), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

class AdminSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password")

admin_schema = AdminSchema()
admin_schemas = AdminSchema(many=True)

# @app.route("/sign-up", methods=["POST"])
# def admin_signup():
#     email = request.json["email"]
#     password = request.json["password"]
#     print( "after")
#     new_admin = Admin(email, password)
#     print(new_admin, "after")

#     db.session.add(new_admin)
#     db.session.commit()

#     return admin_schema.jsonify(new_admin)

@app.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    admin = Admin.query.filter_by(email=email).first()
    admin_password = admin.password

    if password == admin_password:
        return admin_schema.jsonify(admin)
    else:
        return jsonify("No User")
    
@app.route("/logged_in", methods=["POST"])
def admin_logged_in():
    email = request.json["email"]
    password = request.json["password"]
    print( "after")
    new_admin = Admin(email, password)
    print(new_admin, "after")

    db.session.add(new_admin)
    db.session.commit()

    return admin_schema.jsonify(new_admin)


class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(55))
    blog_status = db.Column(db.String(75))
    content = db.Column(db.String(155))
    featured_image = db.Column(db.String(50))
    category = db.Column(db.String(20))

    def __init__(self, title, blog_status, content, featured_image, category):
        self.title = title 
        self.blog_status = blog_status
        self.content = content
        self.featured_image = featured_image
        self.category = category

class BlogSchema(ma.Schema):
    class Meta:
        fields = ('title',  'blog_status', 'content', 'featured_image', 'category')

blog_schema = BlogSchema()
blogs_schema = BlogSchema(many = True)


@app.route("/", methods=["GET"])
def home():
    return "<h1>Hello from flask!</h1>"

@app.route("/blog", methods = ["POST"])
def add_blog():
    title = request.json["title"]
    blog_status = request.json["blog_status"]
    content = request.json["content"]
    featured_image = request.json["featured_image"]
    category = request.json["category"]

    new_blog_post = Blog(title, blog_status, content, featured_image, category)

    db.session.add(new_blog_post)
    db.session.commit()

    blog = Blog.query.get(new_blog_post.id)

    return blog_schema.jsonify(blog)

@app.route("/blog/<id>", methods=["GET"])
def get_blog_id(id):
    blog = Blog.query.get(id)
    result = blog_schema.dump(blog)

    return jsonify(result)

@app.route("/delete/blog/<id>", methods=["DELETE"])
def delete_blog(id):
    record = Blog.query.get(id)

    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "DELETED"})

@app.route("/blog/<id>", methods=["PUT"])
def update_blog(id):
    blog = Blog.query.get(id)
    new_title = request.json["title"]
    new_blog_status = request.json["blog_status"]
    new_content = request.json["content"]
    new_featured_image = request.json["featured_image"]
    new_category = request.json["category"]

    new_blog = Blog(new_title, new_blog_status, new_content, new_featured_image, new_category)

    db.session.commit()

    return blog_schema.jsonify(blog)

if __name__ == "__main__":
    app.run(debug=True)