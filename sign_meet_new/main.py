# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from camera import VideoCamera
from camera1 import VideoCamera1
import mysql.connector
import hashlib
import datetime
import calendar
import random
from random import randint
from urllib.request import urlopen
import webbrowser
#from plotly import graph_objects as go
import cv2
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shutil
import imagehash
from werkzeug.utils import secure_filename
from PIL import Image
import argparse
import urllib.request
import urllib.parse

import pyttsx3

from skimage import transform
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS


import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
import PIL.Image
from PIL import Image
   
# necessary imports 
import seaborn as sns
#import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

plt.style.use('fivethirtyeight')
#%matplotlib inline
pd.set_option('display.max_columns', 26)
##
from PIL import Image, ImageOps
import scipy.ndimage as ndi

from skimage import transform
import seaborn as sns
#from keras.preprocessing.image import ImageDataGenerator , load_img , img_to_array
#from keras.models import Sequential
#from keras.layers import Conv2D, Flatten, MaxPool2D, Dense
##
import glob
#from keras.models import Sequential, load_model
import numpy as np
import pandas as pd
import seaborn as sns
#import keras as k
#from keras.layers import Dense
#from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt
#from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
#from tensorflow.keras.optimizers import Adam
##
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="sign_meet_new"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    ff1=open("static/log.txt","w")
    ff1.write("2")
    ff1.close()
    
    return render_template('index.html',msg=msg)


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM sign_user WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname

            ff=open("static/msg.txt","w")
            ff.write("")
            ff.close()

            f2=open("static/user2.txt","w")
            f2.write(uname)
            f2.close()
            
            cursor.execute('SELECT count(*) FROM sign_user WHERE status=1')
            dd = cursor.fetchone()[0]
            if dd==0:
                cursor.execute("update sign_user set status=1 where uname=%s",(uname,))
                mydb.commit()

                ff=open("static/deaf.txt","w")
                ff.write(uname)
                ff.close()
            
            return redirect(url_for('test_cam'))
        else:
            msg = 'Incorrect username/password! or access not provided' 
   
    return render_template('login_user.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password! or access not provided' 
   
    return render_template('login.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor = mydb.cursor()
    #if request.method=='GET':
    #    msg = request.args.get('msg')
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor.execute('SELECT count(*) FROM sign_user WHERE uname = %s', (uname,))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM sign_user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                    
            sql = "INSERT INTO sign_user(id,name,mobile,email,uname,pass) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (maxid,name,mobile,email,uname,pass1)
            mycursor.execute(sql,val)
            mydb.commit()
            return redirect(url_for('login_user'))
        else:
            msg="fail"

    
        
    return render_template('register.html',msg=msg)

def lg_translate(lg,output):
    result=""
    recognized_text=output
    recognizer = sr.Recognizer()
    translator = Translator()
    try:
        available_languages = {
            'ta': 'Tamil',
            'hi': 'Hindi',
            'ml': 'Malayalam',
            'kn': 'Kannada',
            'te': 'Telugu',
            'mr': 'Marathi',
            'ur': 'Urdu',
            'bn': 'Bengali',
            'gu': 'Gujarati',
            'fr': 'French'
        }

        print("Available languages:")
        for code, language in available_languages.items():
            print(f"{code}: {language}")

        #selected_languages = input("Enter the language codes (comma-separated) you want to translate to: ").split(',')
        selected_languages=lg.split(',')
       
        for lang_code in selected_languages:
            lang_code = lang_code.strip()
            if lang_code in available_languages:
                translated = translator.translate(recognized_text, dest=lang_code)
                print(f"Translation in {available_languages[lang_code]} ({lang_code}): {translated.text}")

                result=translated.text
               

            else:
                print(f"Language code {lang_code} not available.")

        
    except Exception as e:
        print("An error occurred during translation:", e)

    return result
    ###

####
def translate_text(text, source_language, target_language):
    api_key = 'AIzaSyDW9tvaQUsywmaILt73Go8Fy5mU6ILOixU'  # Replace with your API key
    url = f'https://translation.googleapis.com/language/translate/v2?key={api_key}'
    payload = {
        'q': text,
        'source': source_language,
        'target': target_language,
        'format': 'text'
    }
    response = requests.post(url, json=payload)
    translation_data = response.json()
    translated_text = translation_data
    #translation_data['data']['translations'][0]['translatedText']
    return translated_text

def speak(audio):
    engine = pyttsx3.init()
    engine.say(audio)
    engine.runAndWait()

def text_to_speech(text, language='en'):
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False)

    # Save the audio file
    tts.save("static/output.mp3")

    # Play the audio
    #os.system("start output.mp3")  # For Windows, use "start", for macOS use "afplay", for Linux use "mpg321"




@app.route('/admin', methods=['GET', 'POST'])
def admin():
    
    dimg=[]
    '''path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        #resize
        img = cv2.imread('static/data/'+fname)
        rez = cv2.resize(img, (300, 300))
        cv2.imwrite("static/dataset/"+fname, rez)'''
        
        
    return render_template('admin.html',dimg=dimg)

@app.route('/train_gesture', methods=['GET', 'POST'])
def train_gesture():
    msg=""
    mycursor = mydb.cursor()

    
    
    if request.method=='POST':
        gname=request.form['gname']
        
        
        
        mycursor.execute("SELECT count(*) FROM ga_gesture where gesture=%s",(gname,))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM ga_gesture")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            ff=open("static/label.txt","w")
            ff.write(gname)
            ff.close()
            gf="f"+str(maxid)

            
            gfile="f"+str(maxid)+".csv"
            ff=open("static/label1.txt","w")
            ff.write(gfile)
            ff.close()
                    
            sql = "INSERT INTO ga_gesture(id,gesture,fname) VALUES (%s, %s, %s)"
            val = (maxid,gname,gfile)
            mycursor.execute(sql,val)
            mydb.commit()
        else:
            mycursor.execute("SELECT * FROM ga_gesture where gesture=%s",(gname,))
            gd = mycursor.fetchone()
            gid=gd[0]
            ff=open("static/label.txt","w")
            ff.write(gname)
            ff.close()
            gf="f"+str(gid)

            
            gfile="f"+str(gid)+".csv"
            ff=open("static/label1.txt","w")
            ff.write(gfile)
            ff.close() 
            
            
        msg="ok"
    
        
    return render_template('train_gesture.html',msg=msg)

@app.route('/capture', methods=['GET', 'POST'])
def capture():
    msg=""
    gdata=[]
    act=request.args.get("act")
    st=request.args.get("st")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM ga_gesture")
    gdata = mycursor.fetchall()

    if st=="del":
        did=request.args.get("did")
        mycursor.execute("SELECT * FROM ga_gesture where id=%s",(did,))
        gd = mycursor.fetchone()
        gfile=gd[2]
        os.remove("static/hand_gesture_data/"+gfile)
        mycursor.execute("delete from ga_gesture where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('capture',act='1'))
        
        
    return render_template('capture.html',msg=msg,act=act,gdata=gdata)

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ga_gesture")
    data = mycursor.fetchall()

    dt=[]
    dt2=[]
    for dc in data:
        dt.append(dc[1])
        d1=dc[2].split(".")
        dt2.append(d1[0])
        
    cname="|".join(dt)
    cname2="|".join(dt2)
    ff=open("static/class1.txt","w")
    ff.write(cname)
    ff.close()

    ff=open("static/class2.txt","w")
    ff.write(cname2)
    ff.close()
    
    #build model
    DATA_DIR = "static/hand_gesture_data"

    # Load data
    data = []
    labels = []
    gesture_map = {}  # Label mapping

    for idx, file in enumerate(os.listdir(DATA_DIR)):
        gesture_name = file.split(".")[0]
        gesture_map[idx] = gesture_name  # Store label mapping

        file_path = os.path.join(DATA_DIR, file)
        df = pd.read_csv(file_path, header=None)
        data.extend(df.values)
        labels.extend([idx] * len(df))

    # Convert to numpy array
    X = np.array(data)
    y = np.array(labels)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model and gesture mapping
    joblib.dump(model, "gesture_model.pkl")
    joblib.dump(gesture_map, "gesture_map.pkl")

    print(f"Model trained with accuracy: {model.score(X_test, y_test) * 100:.2f}%")

    return render_template('classify.html',msg=msg,data=data)


@app.route('/avatar_upload', methods=['GET', 'POST'])
def avatar_upload():
    msg=""
    dimg=[]
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        
        message=request.form['message']
        file = request.files['file']

        mycursor.execute("SELECT max(id)+1 FROM sign_image")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        fn="F"+str(maxid)+".gif"
        file.save(os.path.join("static/upload", fn))
        
        sql = "INSERT INTO sign_image(id,message,image_file) VALUES (%s, %s, %s)"
        val = (maxid,message,fn)
        mycursor.execute(sql,val)
        mydb.commit()
        msg="success"
        #return redirect(url_for('login_user'))

    
    '''path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        #resize
        img = cv2.imread('static/data/'+fname)
        rez = cv2.resize(img, (300, 300))
        cv2.imwrite("static/dataset/"+fname, rez)'''
        
        
    return render_template('avatar_upload.html',msg=msg)

@app.route('/view_image', methods=['GET', 'POST'])
def view_image():
    msg=""
    act=request.args.get("act")
    dimg=[]
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM sign_image")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")

        mycursor.execute("SELECT * FROM sign_image where id=%s",(did,))
        d1 = mycursor.fetchone()
        fn=d1[2]
        if os.path.exists("static/upload/"+fn):
            os.remove("static/upload/"+fn)
        mycursor.execute("delete from sign_image where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_image'))

        
    return render_template('view_image.html',msg=msg,data=data,act=act)

@app.route('/test_cam', methods=['GET', 'POST'])
def test_cam():
    msg=""
    fn=""
    uname=""
    
    if 'username' in session:
        uname = session['username']
    print(uname)
    cursor = mydb.cursor()
    user=""
    cursor.execute('SELECT * FROM sign_user WHERE status=1')
    dd = cursor.fetchall()
    for dd1 in dd:
        user=dd1[4]

    f2=open("static/user.txt","w")
    f2.write(user)
    f2.close()

    ff=open("static/msg.txt","w")
    ff.write("")
    ff.close()

    ff=open("static/act.txt","w")
    ff.write("")
    ff.close()
            

    act=request.args.get("act")
    f2=open("lang.txt","r")
    lg=f2.read()
    f2.close()

    if request.method=='POST':
        lg=request.form['language']
        f2=open("lang.txt","w")
        f2.write(lg)
        f2.close()

    
        
    return render_template('test_cam.html',msg=msg,lg=lg,user=user,uname=uname)

@app.route('/test_voice', methods=['GET', 'POST'])
def test_voice():
    msg=""
    st=""
    vtext=""
    act=""
    dimg=[]
    uname=""
    
    if 'username' in session:
        uname = session['username']
    
    mycursor = mydb.cursor()
    
    img=""

    if request.method=='POST':        
        mess=request.form['message']
        print("hh")
        print(mess)
        if mess=="":
            s=1
        else:
            mm="%"+mess+"%"
            
            mycursor.execute("SELECT * FROM sign_image where message like %s",(mm,))
            dat = mycursor.fetchall()

            for dat1 in dat:
                img=dat1[2]
                

            if img=="":
                s=1
            else:
                ff=open("static/det.txt","w")
                ff.write(mess)
                ff.close()
                ff=open("static/img.txt","w")
                ff.write(img)
                ff.close()
                ff=open("static/act.txt","w")
                ff.write("1")
                ff.close()
        
                return redirect(url_for('test_voice',act='1'))

    ff=open("static/act.txt","r")
    act=ff.read()
    ff.close()
        
    if act=="1":
        ff=open("static/det.txt","r")
        vtext=ff.read()
        ff.close()

        ff=open("static/img.txt","r")
        img=ff.read()
        ff.close()

        #ff=open("static/act.txt","w")
        #ff.write("")
        #ff.close()
        
    return render_template('test_voice.html',msg=msg,act=act,img=img,st=st,vtext=vtext)

@app.route('/test_voice1', methods=['GET', 'POST'])
def test_voice1():
    msg=""
    st=""
    vtext=""
    act=""
    dimg=[]
    uname=""
    
    if 'username' in session:
        uname = session['username']
    
    img=""
    ff=open("static/act.txt","r")
    act=ff.read()
    ff.close()
        
    if act=="1":
        ff=open("static/det.txt","r")
        vtext=ff.read()
        ff.close()

        ff=open("static/img.txt","r")
        img=ff.read()
        ff.close()

        #ff=open("static/act.txt","w")
        #ff.write("")
        #ff.close()
        
    return render_template('test_voice1.html',msg=msg,act=act,img=img,st=st,vtext=vtext)

@app.route('/test_voice2', methods=['GET', 'POST'])
def test_voice2():
    msg=""
    st=""
    vtext=""
    act=""
    dimg=[]
    img=""
    uname=""
    
    if 'username' in session:
        uname = session['username']
    
    ff=open("static/act.txt","r")
    act=ff.read()
    ff.close()

    ff=open("static/user.txt","r")
    user=ff.read()
    ff.close()
        
    if act=="1":
        ff=open("static/det.txt","r")
        vtext=ff.read()
        ff.close()

        ff=open("static/img.txt","r")
        img=ff.read()
        ff.close()

        if user==uname:
            ff=open("static/count.txt","w")
            ff.write("1")
            ff.close()
        else:
            ff=open("static/count2.txt","w")
            ff.write("1")
            ff.close()

    ff=open("static/count.txt","r")
    cc=ff.read()
    ff.close()

    ff=open("static/count2.txt","r")
    cc2=ff.read()
    ff.close()

    cn=int(cc)
    cn2=int(cc2)
    cnn=cn+cn2
    if cnn>=2:
        ff=open("static/act.txt","w")
        ff.write("")
        ff.close()

        ff=open("static/count.txt","w")
        ff.write("0")
        ff.close()

        ff=open("static/count2.txt","w")
        ff.write("0")
        ff.close()
        
    return render_template('test_voice2.html',msg=msg,act=act,img=img,st=st,vtext=vtext)

@app.route('/process', methods=['GET', 'POST'])
def process():
    dimg=[]
    path_main = 'static/dataset'
    
    for fname in os.listdir(path_main):
        dimg.append(fname)
        print(fname)

    return render_template('process.html',dimg=dimg)

@app.route('/process1', methods=['GET', 'POST'])
def process1():
    dimg=[]
    path_main = 'static/dataset'
    
    for fname in os.listdir(path_main):
        dimg.append(fname)
        print(fname)

    return render_template('process1.html',dimg=dimg)


#TCN  - Temporal Convolutional Network - Sign Language Recognition
def is_power_of_two(num: int):
    return num != 0 and ((num & (num - 1)) == 0)


def adjust_dilations(dilations: list):
    if all([is_power_of_two(i) for i in dilations]):
        return dilations
    else:
        new_dilations = [2 ** i for i in dilations]
        return new_dilations


    

    def __init__(self,
                 dilation_rate: int,
                 nb_filters: int,
                 kernel_size: int,
                 padding: str,
                 activation: str = 'relu',
                 dropout_rate: float = 0,
                 kernel_initializer: str = 'he_normal',
                 use_batch_norm: bool = False,
                 use_layer_norm: bool = False,
                 use_weight_norm: bool = False,
                 **kwargs):

        self.dilation_rate = dilation_rate
        self.nb_filters = nb_filters
        self.kernel_size = kernel_size
        self.padding = padding
        self.activation = activation
        self.dropout_rate = dropout_rate
        self.use_batch_norm = use_batch_norm
        self.use_layer_norm = use_layer_norm
        self.use_weight_norm = use_weight_norm
        self.kernel_initializer = kernel_initializer
        self.layers = []
        self.shape_match_conv = None
        self.res_output_shape = None
        self.final_activation = None

        super(ResidualBlock, self).__init__(**kwargs)

    def tcn_full_summary(model: Model, expand_residual_blocks=True):
        #import tensorflow as tf
        # 2.6.0-rc1, 2.5.0...
        versions = [int(v) for v in tf.__version__.split('-')[0].split('.')]
        if versions[0] <= 2 and versions[1] < 5:
            layers = model._layers.copy()  # store existing layers
            model._layers.clear()  # clear layers

            for i in range(len(layers)):
                if isinstance(layers[i], TCN):
                    for layer in layers[i]._layers:
                        if not isinstance(layer, ResidualBlock):
                            if not hasattr(layer, '__iter__'):
                                model._layers.append(layer)
                        else:
                            if expand_residual_blocks:
                                for lyr in layer._layers:
                                    if not hasattr(lyr, '__iter__'):
                                        model._layers.append(lyr)
                            else:
                                model._layers.append(layer)
                else:
                    model._layers.append(layers[i])

            model.summary()  # print summary

            # restore original layers
            model._layers.clear()
            [model._layers.append(lyr) for lyr in layers]

            

        def _build_layer(self, layer):
           
            self.layers.append(layer)
            self.layers[-1].build(self.res_output_shape)
            self.res_output_shape = self.layers[-1].compute_output_shape(self.res_output_shape)

        def build(self, input_shape):

            with K.name_scope(self.name):  # name scope used to make sure weights get unique names
                self.layers = []
                self.res_output_shape = input_shape

                for k in range(2):  # dilated conv block.
                    name = 'conv1D_{}'.format(k)
                    with K.name_scope(name):  # name scope used to make sure weights get unique names
                        conv = Conv1D(
                            filters=self.nb_filters,
                            kernel_size=self.kernel_size,
                            dilation_rate=self.dilation_rate,
                            padding=self.padding,
                            name=name,
                            kernel_initializer=self.kernel_initializer
                        )
                        if self.use_weight_norm:
                            from tensorflow_addons.layers import WeightNormalization
                            # wrap it. WeightNormalization API is different than BatchNormalization or LayerNormalization.
                            with K.name_scope('norm_{}'.format(k)):
                                conv = WeightNormalization(conv)
                        self._build_layer(conv)

                    with K.name_scope('norm_{}'.format(k)):
                        if self.use_batch_norm:
                            self._build_layer(BatchNormalization())
                        elif self.use_layer_norm:
                            self._build_layer(LayerNormalization())
                        elif self.use_weight_norm:
                            pass  # done above.

                    with K.name_scope('act_and_dropout_{}'.format(k)):
                        self._build_layer(Activation(self.activation, name='Act_Conv1D_{}'.format(k)))
                        self._build_layer(SpatialDropout1D(rate=self.dropout_rate, name='SDropout_{}'.format(k)))

                if self.nb_filters != input_shape[-1]:
                    # 1x1 conv to match the shapes (channel dimension).
                    name = 'matching_conv1D'
                    with K.name_scope(name):
                        # make and build this layer separately because it directly uses input_shape.
                        # 1x1 conv.
                        self.shape_match_conv = Conv1D(
                            filters=self.nb_filters,
                            kernel_size=1,
                            padding='same',
                            name=name,
                            kernel_initializer=self.kernel_initializer
                        )
                else:
                    name = 'matching_identity'
                    self.shape_match_conv = Lambda(lambda x: x, name=name)

                with K.name_scope(name):
                    self.shape_match_conv.build(input_shape)
                    self.res_output_shape = self.shape_match_conv.compute_output_shape(input_shape)

                self._build_layer(Activation(self.activation, name='Act_Conv_Blocks'))
                self.final_activation = Activation(self.activation, name='Act_Res_Block')
                self.final_activation.build(self.res_output_shape)  # probably isn't necessary

                # this is done to force Keras to add the layers in the list to self._layers
                for layer in self.layers:
                    self.__setattr__(layer.name, layer)
                self.__setattr__(self.shape_match_conv.name, self.shape_match_conv)
                self.__setattr__(self.final_activation.name, self.final_activation)

                super(ResidualBlock, self).build(input_shape)  # done to make sure self.built is set True

        def call(self, inputs, training=None, **kwargs):
            """
            Returns: A tuple where the first element is the residual model tensor, and the second
                     is the skip connection tensor.
            """
            
            x1 = inputs
            for layer in self.layers:
                training_flag = 'training' in dict(inspect.signature(layer.call).parameters)
                x1 = layer(x1, training=training) if training_flag else layer(x1)
            x2 = self.shape_match_conv(inputs)
            x1_x2 = self.final_activation(layers.add([x2, x1], name='Add_Res'))
            return [x1_x2, x1]

        def compute_output_shape(self, input_shape):
            return [self.res_output_shape, self.res_output_shape]
####
def CNN():
    #Lets start by loading the Cifar10 data
    (X, y), (X_test, y_test) = cifar10.load_data()

    #Keep in mind the images are in RGB
    #So we can normalise the data by diving by 255
    #The data is in integers therefore we need to convert them to float first
    X, X_test = X.astype('float32')/255.0, X_test.astype('float32')/255.0

    #Then we convert the y values into one-hot vectors
    #The cifar10 has only 10 classes, thats is why we specify a one-hot
    #vector of width/class 10
    y, y_test = u.to_categorical(y, 10), u.to_categorical(y_test, 10)

    #Now we can go ahead and create our Convolution model
    model = Sequential()
    #We want to output 32 features maps. The kernel size is going to be
    #3x3 and we specify our input shape to be 32x32 with 3 channels
    #Padding=same means we want the same dimensional output as input
    #activation specifies the activation function
    model.add(Conv2D(32, (3, 3), input_shape=(32, 32, 3), padding='same',
                     activation='relu'))
    #20% of the nodes are set to 0
    model.add(Dropout(0.2))
    #now we add another convolution layer, again with a 3x3 kernel
    #This time our padding=valid this means that the output dimension can
    #take any form
    model.add(Conv2D(32, (3, 3), activation='relu', padding='valid'))
    #maxpool with a kernet of 2x2
    model.add(MaxPooling2D(pool_size=(2, 2)))
    #In a convolution NN, we neet to flatten our data before we can
    #input it into the ouput/dense layer
    model.add(Flatten())
    #Dense layer with 512 hidden units
    model.add(Dense(512, activation='relu'))
    #this time we set 30% of the nodes to 0 to minimize overfitting
    model.add(Dropout(0.3))
    #Finally the output dense layer with 10 hidden units corresponding to
    #our 10 classe
    model.add(Dense(10, activation='softmax'))
    #Few simple configurations
    model.compile(loss='categorical_crossentropy',
                  optimizer=SGD(momentum=0.5, decay=0.0004), metrics=['accuracy'])
    #Run the algorithm!
    model.fit(X, y, validation_data=(X_test, y_test), epochs=25,
              batch_size=512)
    #Save the weights to use for later
    model.save_weights("cifar10.hdf5")
    #Finally print the accuracy of our model!
    print("Accuracy: &2.f%%" %(model.evaluate(X_test, y_test)[1]*100))



#######
@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""

    
        
    return render_template('userhome.html',msg=msg)

@app.route('/test', methods=['GET', 'POST'])
def test():
    msg=""
    ss=""
    fn=""
    fn1=""
    tclass=0

    ff=open("static/trained/class1.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')

    ff=open("static/msg.txt","w")
    ff.write("")
    ff.close()
    
    if request.method=='POST':
        lg=request.form['language']
        #file = request.files['file']

        af=open("lang.txt","w")
        af.write(lg)
        af.close()
        return redirect(url_for('test_cam'))

        
        '''if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = file.filename
            filename = secure_filename(fname)
            f1=open('static/test/file.txt','w')
            f1.write(filename)
            f1.close()
            file.save(os.path.join("static/test", filename))

        cutoff=1
        path_main = 'static/dataset'
        for fname1 in os.listdir(path_main):
            hash0 = imagehash.average_hash(Image.open("static/dataset/"+fname1)) 
            hash1 = imagehash.average_hash(Image.open("static/test/"+filename))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                ss="ok"
                fn=fname1
                print("ff="+fn)
                break
            else:
                ss="no"

        if ss=="ok":
            print("yes")
            tclass=0
            dimg=[]

            ##    
            ff2=open("static/trained/tdata.txt","r")
            rd=ff2.read()
            ff2.close()

            num=[]
            r1=rd.split(',')
            s=len(r1)
            ss=s-1
            i=0
            while i<ss:
                num.append(int(r1[i]))
                i+=1

            #print(num)
            dat=toString(num)
            dd2=[]
            ex=dat.split(',')
            print(fn)
            ##
            ##
            n=0
            fpos=""
            path_main = 'static/dataset'
            for val in ex:
                dt=[]
                fa1=fn.split('.')
                fa=fa1[0].split('-')
                fpos=fa[1]
                fv=int(fa[1])-1
                n+=1
                if cname[fv]==val:
                    tclass=n
                    
                    break
                
            
            print(tclass)
            tt=tclass-1
            cla=cname[tt]
            dta=cla+"|"+fn+"|"+fpos
            f3=open("static/test/res.txt","w")
            f3.write(dta)
            f3.close()

            
                    
            return redirect(url_for('test_pro',act="1"))
        else:
            msg="Invalid!"'''
    
        
    return render_template('test.html',msg=msg)


    
@app.route('/test_pro', methods=['GET', 'POST'])
def test_pro():
    msg=""
    fn=""
    act=request.args.get("act")
    f2=open("static/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split('|')
    fn=gs[1]
    
    ts=gs[0]
    fname=fn

    
    ##bin
    '''image = cv2.imread('static/dataset/'+fn)
    original = image.copy()
    kmeans = kmeans_color_quantization(image, clusters=4)

    # Convert to grayscale, Gaussian blur, adaptive threshold
    gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

    # Draw largest enclosing circle onto a mask
    mask = np.zeros(original.shape[:2], dtype=np.uint8)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
        cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
        break
    
    # Bitwise-and for result
    result = cv2.bitwise_and(original, original, mask=mask)
    result[mask==0] = (0,0,0)

    
    ###cv2.imshow('thresh', thresh)
    ###cv2.imshow('result', result)
    ###cv2.imshow('mask', mask)
    ###cv2.imshow('kmeans', kmeans)
    ###cv2.imshow('image', image)
    ###cv2.waitKey()

    #cv2.imwrite("static/upload/bin_"+fname, thresh)'''
    

    ###fg
    '''img = cv2.imread('static/dataset/'+fn)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    segment = cv2.subtract(sure_bg,sure_fg)
    img = Image.fromarray(img)
    segment = Image.fromarray(segment)
    path3="static/trained/test/fg_"+fname
    #segment.save(path3)'+'''
    
        
    return render_template('test_pro.html',msg=msg,fn=fn,ts=ts,act=act)

@app.route('/test_pro2', methods=['GET', 'POST'])
def test_pro2():
    msg=""
    fn=""
    act=request.args.get("act")
    f2=open("static/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split('|')
    fn=gs[1]
    ts=gs[0]
    pos=gs[2]

    n=int(pos)-1

    af2=open("lang.txt","r")
    lgg=af2.read()
    af2.close()
    
    lfile="a"+pos+"_"+lgg+".jpg"

    
    af=open("static/trained/lang1.txt","r")
    la=af.read()
    af.close()

    la1=la.split(",")
    la2=la1[n].split("-")
    
    c=0
    if lgg=="h":
        c=1
    elif lgg=="t":
        c=2
    elif lgg=="m":
        c=3
    else:
        c=0

    word=la2[c]
    
    
    return render_template('test_pro2.html',msg=msg,fn=fn,ts=ts,act=act,lfile=lfile,word=word)


@app.route('/test2',methods=['POST','GET'])
def test2():
    msg=""
    name=request.args.get("name")
    return render_template('test2.html', msg=msg,name=name)

@app.route('/autocapture',methods=['POST','GET'])
def autocapture():
    msg=""
    uname=""
    ff1=open("static/log.txt","r")
    log=ff1.read()
    ff1.close()

    if 'username' in session:
        uname = session['username']

    ff1=open("static/user.txt","r")
    user=ff1.read()
    ff1.close()
    
    if uname==user:
        print("hello")

        # Load model and gesture map
        model = joblib.load("gesture_model.pkl")
        gesture_map = joblib.load("gesture_map.pkl")

        # Get expected number of features
        expected_features = model.n_features_in_

        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils
        hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

        imgname=user+".jpg"
        frame = cv2.imread('static/photo/'+imgname)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract features
                landmark_list = []
                for lm in hand_landmarks.landmark:
                    landmark_list.extend([lm.x, lm.y, lm.z])
                
                # Predict only if feature size matches
                if len(landmark_list) == expected_features:
                    prediction = model.predict([landmark_list])[0]
                    gesture_name = gesture_map.get(prediction, "Unknown")

                    gn=""
                    ff=open("static/class2.txt","r")
                    cn=ff.read()
                    ff.close()
                    cna=cn.split("|")

                    ff=open("static/class1.txt","r")
                    hn=ff.read()
                    ff.close()
                    hna=hn.split("|")
                    u=0
                    for cna1 in cna:
                        if cna1==gesture_name:
                            gn=hna[u]
                            break
                        u+=1
                    if gn=="":
                        s=1
                    else:
                        ff=open("static/detect.txt","w")
                        ff.write(gn)
                        ff.close()
                        print(gn)

                        #cv2.putText(frame, f"{gn}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                else:
                    ff=open("static/detect.txt","w")
                    ff.write("")
                    ff.close()

        '''mpHands = mp.solutions.hands
        hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        mpDraw = mp.solutions.drawing_utils

        # Load the gesture recognizer model
        model = load_model('mp_hand_gesture')

        # Load class names
        f = open('gesture.names', 'r')
        classNames = f.read().split('\n')
        f.close()

        imgname=user+".jpg"
        frame = cv2.imread('static/photo/'+imgname)
        x, y, c = frame.shape

        # Flip the frame vertically
        #frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = hands.process(framergb)

        # print(result)
        
        className = ''
        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    # print(id, lm)
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)

                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                # Predict gesture
                prediction = model.predict([landmarks])
                # print(prediction)
                classID = np.argmax(prediction)
                className = classNames[classID]
                ff=open("static/msg.txt","w")
                ff.write(className)
                ff.close()
                text_to_speech(className)
                print("class="+className)
        else:
            ff=open("static/msg.txt","w")
            ff.write("")
            ff.close()'''

    return render_template('autocapture.html',msg=msg,user=user,uname=uname)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    msg=""
    uname=""
    
    if 'username' in session:
        uname = session['username']

    ff1=open("static/user.txt","r")
    user=ff1.read()
    ff1.close()
    print("yes")
    if request.method=='POST':
        if uname==user:
            print("capture")
            file = request.files['webcam']
            try:
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file:
                    fn=user+".jpg"
                    fn1 = secure_filename(fn)
                    file.save(os.path.join("static/photo", fn1))
                    #return redirect(url_for('detect'))
                    ff1=open("static/log.txt","w")
                    ff1.write("1")
                    ff1.close()
            except:
                print("dd")
    return render_template('upload.html',msg=msg)


@app.route('/test_pro3', methods=['GET', 'POST'])
def test_pro3():
    msg=""
    fn=""
    st=""
    lfile=""
    word=""
    val=""
    
    act=request.args.get("act")
    f2=open("lang.txt","r")
    lgg=f2.read()
    f2.close()

    f3=open("static/detect.txt","r")
    ms=f3.read()
    f3.close()

    ff=open("static/class1.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split('|')

    if ms=="":
        st=""
    else:
        st="1"
        n=0
        for cc in cname:
            n+=1
            if cc==ms:              
                
                break
        print("value=")
        print(str(n))
        m=n-1
        pos=n
        ##
        
        #lfile="a"+str(pos)+"_"+lgg+".jpg"

        c=0
        if lgg=="" or lgg=="en":
            c=1
            val=ms
            word=ms
            #text_to_speech(word)
        else:
            val=lg_translate(lgg,ms)
            word=val
            #text_to_speech(word,lgg)

        ff=open("static/detect.txt","w")
        ff.write("")
        ff.close()
        

    return render_template('test_pro3.html',msg=msg,st=st,lgg=lgg,fn=fn,act=act,lfile=lfile,word=word,val=val)

#######################
def gen1(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video_feed1')
def video_feed1():
    return Response(gen1(VideoCamera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
############
def gen(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


##########################
@app.route('/logout')
def logout():

    uname=""
    
    if 'username' in session:
        uname = session['username']

    cursor = mydb.cursor()
    cursor.execute("update sign_user set status=0 where uname=%s",(uname,))
    mydb.commit()
                
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


