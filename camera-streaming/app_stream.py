from flask import Flask, render_template, Response
import cv2
import time

app = Flask(__name__)

# list of camera accesses
cameras = ["rtmp://140.116.187.114:1935/live3", "rtmp://140.116.187.114:1935/live/test1", "rtmp://140.116.187.114:1935/live2/test2"]


def find_camera(list_id):
    return cameras[int(list_id)]


def gen_frames(camera_id):
    cam = find_camera(camera_id) # cam = cameras[int(id)]
    cap = cv2.VideoCapture(cam)  # capture the video from the live feed

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        #time.sleep(0.06)


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html", camera_list=len(cameras), camera=cameras)


@app.route('/video_feed/<string:list_id>/', methods=["GET"])
def video_feed(list_id):
    return Response(gen_frames(list_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)