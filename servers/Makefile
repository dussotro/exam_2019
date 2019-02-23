default: install

install:
	modprobe bcm2835-v4l2

run:
  python servo_server.py 168.20.21.164 &
  ./v4l2grad -o image_output.jpg

man:
  man TUTO.md
