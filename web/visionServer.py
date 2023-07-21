from flask import Flask, render_template

app = Flask("VisionServer")


class VisionServer:
    @app.route('/')
    def index():
        return render_template("index.html")

    def runServer(self):
        app.run(debug=True, host='0.0.0.0', port=80)
