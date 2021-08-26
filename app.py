from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://csqkejzxapdayn:987be0c9d4ccb5db2b250d0651334b6f0225f6ef741bdefa1e24dd80012ee578@ec2-34-194-14-176.compute-1.amazonaws.com:5432/d7imc1vhfg9qbq'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description


class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')


post_schema = PostSchema()
posts_schema = PostSchema(many=True)


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome To RestBlog ! RestBlog is a blogging platform REST API . Made With ❤️ & Flask ."})


@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    result = posts_schema.dump(posts)
    return jsonify(result)


@app.route('/posts', methods=['POST'])
def add_post():
    title = request.json['title']
    description = request.json['description']
    post = Post(title=title, description=description)
    db.session.add(post)
    db.session.commit()
    return post_schema.jsonify(post)


@app.route('/post/<id>', methods=['GET'])
def get_post(id):
    post = Post.query.get(id)
    return post_schema.jsonify(post)


@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get(id)
    title = request.json['title']
    description = request.json['description']
    post.title = title
    post.description = description
    db.session.commit()
    return post_schema.jsonify(post)


@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return post_schema.jsonify(post)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
