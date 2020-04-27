from flask import Flask, render_template, request, send_from_directory
import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

NST = __import__('style_transfer').NST

application = Flask(__name__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
pictures = {}

@application.route("/",  methods=["GET", "POST"])
def index():
    return render_template("index.html")

@application.route("/upload_content",  methods=["POST"])
def upload_content():
    target = os.path.join(PROJECT_ROOT, 'images/')
    if not os.path.isdir(target):
        os.mkdir(target)
    for upload in request.files.getlist("file"):
        filename = upload.filename
        destination = '/'.join([target, filename])
        upload.save(destination)
        pictures['content'] = destination
    return render_template("upload_content.html", image_name=filename)

@application.route("/upload_style", methods=["POST"])
def upload_style():
    target = os.path.join(PROJECT_ROOT, 'images/')
    if not os.path.isdir(target):
        os.mkdir(target)
    if request.method == "POST":
        for upload in request.files.getlist("file"):
            filename = upload.filename
            destination = '/'.join([target, filename])
            pictures['style'] = destination
            upload.save(destination)
    return render_template("upload_style.html", image_name=filename)

@application.route('/upload/<filename>')
def send_images(filename):
    return send_from_directory("images", filename=filename)

@application.route("/content_style", methods=["GET", "POST"])
def show_content_style():
    target = os.path.join(PROJECT_ROOT, 'images/')
    pic = pictures
    style_image = mpimg.imread(pic['style'])
    content_image = mpimg.imread(pic['content'])
    np.random.seed(0)
    nst = NST(style_image, content_image)
    generated_image, cost = nst.generate_image(iterations=2, step=1, lr=0.002)
    mpimg.imsave(target + 'generated_image.jpg', generated_image)
    images = os.listdir('./images')
    print("Best cost:", cost)
    return render_template("content_style.html", images=images, pictures=pic, gen_im = generated_image)


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=True)
