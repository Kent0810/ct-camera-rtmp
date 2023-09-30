import subprocess as sp
import cv2

from threading import Thread
from WebcamVideoStream import WebcamVideoStream

# This is the XML location + file containing the pre-trained classifier for detecting frontal faces in images
face_cascade = cv2.CascadeClassifier('./pretrainned-model/haarcascade_frontalface_default.xml')

def start_ffmpeg(rtmp_url):
    command = [
      'ffmpeg',
      '-s', '1280x720',
      '-y',
      '-f', 'rawvideo',
      '-pix_fmt', 'bgr24',
      '-r', '30',
      '-i', '-',
      '-vf', 'format=yuv420p',
      '-c:v', 'h264_v4l2m2m',
      '-b:v', '1M',
      '-f', 'flv',
      '-bufsize', '256M',
       rtmp_url
    ]
    return sp.Popen(command, stdin=sp.PIPE)

def face_detection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return cv2.flip(frame, 1)

def main():
    rtmp_url = "rtmp://103.165.142.44:7957/camera/kent-test"  # TODO Dynamic URL, Stream keys...
    vs = WebcamVideoStream().start()
    vs.print()
    
    ffmpeg_process = start_ffmpeg(rtmp_url)

    # Read web camera
    while vs.isOpened():
        frame = vs.read()
      
        # Detect faces
        # frame = face_detection(frame)

        # Write to pipe
        ffmpeg_process.stdin.write(frame.tobytes())

    ffmpeg_process.stdin.close()  # Close stdin pipe
    ffmpeg_process.wait()

    ffplay_process.kill()  # Forcefully close FFplay sub-process

if __name__ == '__main__':
        
    main()
