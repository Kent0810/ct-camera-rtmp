import subprocess as sp
import cv2

# def start_ffplay(rtmp_url):
#     return sp.Popen(['ffplay', '-listen', '1', '-i', rtmp_url])

def start_ffmpeg(rtmp_url, width, height, fps):
    command = [
        'ffmpeg',
        '-y',
        '-re',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', "{}x{}".format(width, height),
        '-r', str(fps),
        '-i', '-',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'ultrafast',
        '-bufsize', '64M',
        '-f', 'flv',
        rtmp_url
    ]
    return sp.Popen(command, stdin=sp.PIPE)

def face_detection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return cv2.flip(frame, 1)

def main():
    rtmp_url = "rtmp://localhost:1935/live/test"  # TODO Dynamic URL, Stream keys...
    cap = cv2.VideoCapture(0)

    # Get video information
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # ffplay_process = start_ffplay(rtmp_url)
    ffmpeg_process = start_ffmpeg(rtmp_url, width, height, fps)

    # Read web camera
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of input file")
            break


         # Detect faces
        frame = face_detection(frame)

        # Write to pipe
        ffmpeg_process.stdin.write(frame.tobytes())

    ffmpeg_process.stdin.close()  # Close stdin pipe
    ffmpeg_process.wait()

    ffplay_process.kill()  # Forcefully close FFplay sub-process

if __name__ == '__main__':
    main()