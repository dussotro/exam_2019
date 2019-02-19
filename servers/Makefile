default: install

install:
	modprobe bcm4825-v4l

run:
  python servo_server.py &
  ./v4l2grad 172.20.21.164

man:
  man TUTO.md
