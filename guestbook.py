from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from logging import FileHandler, WARNING
# from flask.ext.uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor@localhost/guessbook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
# photos = UploadSet('photos', IMAGES)
# app.config['UPLOAD_PHOTOS_DES'] = 'static/img'
# configure_uploads(app, photos)

app.config.from_pyfile('myconfig.cfg')
app.logger.addHandler(file_handler)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    comment = db.Column(db.String(500), nullable=False)


@app.route('/')
def index():
    result = Comments.query.order_by(Comments.username).all()
    return render_template('index.html', result=result)


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/process', methods=['POST'])
def process():
    username = request.form['username']
    comment = request.form['comment']

    signature = Comments(username=username, comment=comment)
    db.session.add(signature)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    links = {'Google': 'https://www.google.com',
             'Facebook': 'https://www.facebook.com', 'Bing': 'https://www.bing.com'}
    keyLinks = links.keys()
    valLinks = links.values()
    title = []

    for key in keyLinks:
        title.append(key)

    return render_template('home.html', user='Admin', links=links, keyLinks=keyLinks, valLinks=title)


@app.route('/about/<something>')
def about(something):
    return '<h1>You are on the ' + something + ' page!</h1>'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
    return render_template('upload.html')


@app.route('/tesabort/<username>', methods=['GET', 'POST'])
def tesabort(username):
    if username[0].isdigit():
        abort(400)
    return '<h1>Good Username</h1>'


@app.route('/teserror', methods=['POST'])
def teserror():
    return 1/0


@app.errorhandler(400)
def error400(error):
    return '<h1>Custom Error 400 - Bad Request</h1>', 400


@app.errorhandler(404)
def error404(error):
    return '<h1>Custom Error 404 - Not Found!!</h1>', 404


@app.errorhandler(405)
def error405(error):
    return '<h1>Custom Error 405 - Method Not Allowed!!</h1>', 405


@app.errorhandler(500)
def error500(error):
    return '<h1>Custom Error 500 - Internal Server Error</h1>', 500


if __name__ == '__main__':
    app.run()
