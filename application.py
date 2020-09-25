import cv2
import os
import numpy as np
from flask import Flask, render_template, request

img=np.array([])
logo=np.array([])
app=Flask(__name__)

def blend_logo():
    global img, logo
    shape_original_image = img.shape
    print(img.shape, logo.shape)
    crop_original = img[-int(0.09*shape_original_image[1])  : - int(0.02*shape_original_image[1]),-int(0.09*shape_original_image[1])  : - int(0.02*shape_original_image[1])]
    print(crop_original.shape)
    resized_logo = cv2.resize(logo, (crop_original.shape[1], crop_original.shape[0]))
    print(resized_logo.shape)
    blended= cv2.addWeighted(crop_original,0.2,resized_logo,0.8,0)

    img[-int(0.09*shape_original_image[1])  : - int(0.02*shape_original_image[1]),-int(0.09*shape_original_image[1])  : - int(0.02*shape_original_image[1])] = blended
    return img

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/upload_original", methods=['POST'])
def upload_original():

    original= request.files['original_image']
    path = os.path.join('static/img', original.filename)
    try:
        os.remove(path)
    except:
        pass
    original.save(path)

    global img

    img=cv2.imread(path)
    return path


@app.route("/upload_logo", methods=['POST'])
def upload_logo():
    logo_image = request.files['logo_image']
    path = os.path.join('static/img', logo_image.filename)
    try:
        os.remove(path)
    except:
        pass

    logo_image.save(path)

    global logo

    logo = cv2.imread(path)
    return path

@app.route("/generate", methods=['GET'])
def generate():
    path = os.path.join('static/img', "generated_"+str(np.random.randint(low=0, high=1e6))+".png")
    try:
        os.remove(path)
    except:
        pass

    blended = blend_logo()
    cv2.imwrite(path,blended)

    return path
