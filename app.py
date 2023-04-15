"""

        CREATED BY @VIKAS
"""
from flask import Flask, request, render_template, redirect, session, Response
from flask_cors import CORS, cross_origin
from utils import detect, save_image, detector_util
from database import db
import os
import requests
import constants
import warnings
warnings.filterwarnings("ignore")

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)
PEOPLE_FOLDER = os.path.join('image')


@app.route('/')
@cross_origin()
def login():
    if 'user_email' in session:
        print('with session')
        return render_template('home.html')
    else:
        print('without session')
        return render_template('index.html')


@app.route('/register')
@cross_origin()
def register():
    return render_template('register.html')


@app.route('/admin')
@cross_origin()
def admin():
    return render_template('admin.html')


@app.route('/home')
@cross_origin()
def home():
    if 'user_email' in session:
        print('with session')
        return render_template('home.html')
    else:
        print('without session')
        return render_template('index.html')


@app.route('/profile')
@cross_origin()
def profile():
    if 'user_email' in session:
        u_email = session['user_email']
        fname = db.user_info_basic(u_email)
        count = db.user_complaint_basic(u_email)
        user_recent=db.view_recent(u_email)
        return render_template('profile.html', email=u_email, fname=fname, count=count,lat=user_recent[1],lon=user_recent[2],no_pothole=user_recent[3])
    else:
        return redirect('/')

@app.route('/about')
@cross_origin()
def about():
    if 'user_email' in session:
        return render_template('about.html')
    else:
        return redirect('/')


@app.route('/adm_dash')
@cross_origin()
def admin_dashboard():
    headings = {"Email", "latitude", "longitude", "No of potholes detetcted"}
    data = db.admshow()
    return render_template('admdash.html', headings=headings, data=data)


@app.route('/login_validate', methods=['POST'])
@cross_origin()
def login_vaidate():
    email = request.form.get('email')
    password = request.form.get('password')
    # methods.get_email(email)
    user_validate = db.login_validatlilon(email, password)
    print(user_validate)
    if user_validate == 0:

        return render_template("/index.html")
    else:
        session['user_email'] = user_validate[0][1]

        return redirect("/home")


@app.route('/users_register', methods=['POST'])
@cross_origin()
def reg_user():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    user_is_registerd = db.uniq_email(email)
    if user_is_registerd == 0:
        db.register_user(name, email, password)
        return render_template('/user_register.html')
    else:
        print("user is registerd already")
        return redirect('/register')


@app.route('/upload', methods=['GET', 'POST'])
@cross_origin()
def upload():
    if 'user_email' in session:
        return render_template('upload.html')
    else:
        return render_template('index.html')


# original code
@app.route('/upload_image', methods=['GET', 'POST'])
@cross_origin()
def upload_file():
    if 'user_email' in session:
        if request.method == 'POST':
            res = requests.get('https://ipinfo.io/')
            data = res.json()
            location = data['loc'].split(',')
            latitude = location[0]
            longitude = location[1]
            print("Latitude : ", latitude)
            print("Longitude : ", longitude)
            f = request.files['file']
            print(type(f))
            img_path_upload, img_name = save_image.get_location_of_uploaded()
            f.save(img_path_upload)
            img_path = img_path_upload
            user_session_email = session['user_email']
            print(user_session_email)
            return Response(detect.detect_pothole(img_path, latitude, longitude, session['user_email'], img_name),
                            mimetype="multipart/x-mixed-replace; boundary=frame")
    else:
        print('without session')
        return render_template('index.html')


@app.route('/view_previous', methods=['GET', 'POST'])
@cross_origin()
def view_previous():
    if request.method == 'POST':
        if 'user_email' in session:
            print('with session')
            headings = {"Email", "longitude", "latitude", "Count"}
            data = db.view_previous(session['user_email'])
            return render_template('view_previous.html', headings=headings, data=data, user_email=session['user_email'])
        else:
            print('without session')
            return redirect('/')


@app.route('/logout')
@cross_origin()
def logout():
    if 'user_email' in session:
        session.pop('user_email')
        return redirect('/')
    else:
        return redirect('/')


if __name__ == "__main__":
    print('server started')
    detection_graph1, sess1 = detector_util.load_inference_graph()
    constants.sess = sess1
    constants.detection_graph = detection_graph1
    print('model loaded')
    app.run(host='localhost', debug=True)
