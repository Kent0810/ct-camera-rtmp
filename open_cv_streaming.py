import subprocess as sp
import cv2

# def start_ffplay(rtmp_url):
#     return sp.Popen(['ffplay', '-listen', '1', '-i', rtmp_url])

# This is the XML location + file containing the pre-trained classifier for detecting frontal faces in images
face_cascade = cv2.CascadeClassifier('./pretrainned-model/haarcascade_frontalface_default.xml')


def start_ffmpeg(rtmp_url, width, height, fps):
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
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH ,1280);
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT ,720);
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # Get video information
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(width, height, fps)

    # ffplay_process = start_ffplay(rtmp_url)
    ffmpeg_process = start_ffmpeg(rtmp_url, width, height, fps)

    # Read web camera
    while cap.isOpened():
        _, frame = cap.read()
      
        # Detect faces
        frame = face_detection(frame)

        # Write to pipe
        ffmpeg_process.stdin.write(frame.tobytes())

    ffmpeg_process.stdin.close()  # Close stdin pipe
    ffmpeg_process.wait()

    ffplay_process.kill()  # Forcefully close FFplay sub-process

if __name__ == '__main__':
        
    main()
