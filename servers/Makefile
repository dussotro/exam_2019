default: install

install:
	modprobe bcm4825-v4l
	sudo apt install libjpeg-dev libv4l-dev autoconf automake libtool

run:
  python servo_server.py &
  ./v4l2grad 172.20.21.164

man:
  man README_EXAM.md
