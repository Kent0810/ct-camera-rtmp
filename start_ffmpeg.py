import subprocess as sp

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
