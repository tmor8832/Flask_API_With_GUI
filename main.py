from flask import Flask, render_template, request, url_for, flash, redirect
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 123456
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

from flask_cors import CORS

CORS(app)

messages = [{'title': 'Hello One',
             'content': 'This is a message'},
            {'title': 'Hello Two',
             'content': 'This is also a message'}]


@app.route('/')
def index():
    entries = VideoModel.query.all()
    return render_template('index.html', messages=messages, entries=entries)


@app.route('/test/', methods=('GET', 'POST'))
def test():
    if request.method == 'POST':
        title = request.form['title']
        views = request.form['views']
        ID = request.form['ID']
        likes = request.form['likes']
        if not title:
            flash('Title is required!')
        elif not ID:
            flash('ID is required!')
        elif not views:
            flash('views is required!')
        elif not likes:
            flash('likes is required!')
        else:
            result = VideoModel.query.filter_by(id=ID).first()
            if result:
                abort(409, message="Video id taken...")
            video = VideoModel(
                id=ID, name=title, views=views, likes=likes)
            db.session.add(video)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('test.html')


@app.route('/edit/<int:video_id>', methods=('GET', 'POST'))
def edit(video_id):
    if request.method == 'GET':
        entry = VideoModel.query.filter_by(id=video_id).first()
        return render_template('edit.html', video_id=video_id, entry=entry)

    if request.method == 'POST':
        title = str(request.form['title'])
        views = int(request.form['views'])
        ID = int(video_id)
        likes = int(request.form['likes'])
        if not title:
            flash('Title is required!')
        elif not ID:
            flash('ID is required!')
        elif not views:
            flash('views is required!')
        elif not likes:
            flash('likes is required!')
        #elif type(title) != str & type(views) != int & type(likes) != int:
            #flash('Format correctly')
        else:
            result = VideoModel.query.filter_by(id=ID).first()
            result.name = str(title)
            result.views = int(views)
            result.likes = int(likes)
            db.session.commit()
            return redirect(url_for('index'))

    return redirect('index.html')


@app.route('/delete/<int:video_id>', methods=('GET', 'POST'))
def delete(video_id):
    if request.method == 'GET':
        entry = VideoModel.query.filter_by(id=video_id).first()
        return render_template('delete.html', video_id=video_id, entry=entry)

    elif request.method == 'POST':
        VideoModel.query.filter_by(id=video_id).delete()
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('test.html')


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"


video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument(
    "views", type=int, help="Views of the video", required=True)
video_put_args.add_argument(
    "likes", type=int, help="Likes on the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument(
    "name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with that id")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id taken...")

        video = VideoModel(
            id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()

        return result

    def delete(self, video_id):
        VideoModel.query.filter_by(id=video_id).delete()
        db.session.commit()
        return ''


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
