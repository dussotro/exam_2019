default: install

install:
	modprobe bcm4825-v4l

run:
  python servo_server.py &
  ./v4l2grad -o image_output.jpg

man:
  man TUTO.md
