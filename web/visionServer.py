from flask import Flask, render_template, Response, request, current_app, redirect, url_for
from vision import WorbotsVision
import time
import threading

app = Flask("VisionServer")
vision = WorbotsVision(0)

class VisionServer:
    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/video')
    def video():
        return Response(vision.mainFunc(), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/setCamera', methods=['GET', 'POST'])
    def setCamera():
        if request.method == 'POST':
            number = request.form['cameraID']
            vision.openNewCam(number)
            return redirect(url_for('index'))
        else:
            return '<p>POST only</p>'

    def runServer(self):
        app.run(debug=True, host='0.0.0.0', port=5800, threaded=True)
        time.sleep(2.0)
        t = threading.Thread(target=vision.openMain)
        t.daemon = True
        t.start()

        