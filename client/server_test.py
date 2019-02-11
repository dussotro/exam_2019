# coding: utf-8
import sys
import socket
import time
import signal
import cv2

def close_all(signal, frame):
        socket_servo.close()
        socket_camera.close()
        socket_image.close()
        print("\nSIG : {} : Interruption programme...".format(signal))
        sys.exit(0)

try:
        socket_image.close()
        socket_servo.close()
        socket_camera.close()
except:
        pass    

#Gestion des signaux
signal.signal(signal.SIGINT, close_all)  #Ctrl + C
signal.signal(signal.SIGTSTP, close_all) #Ctrl + Z
signal.signal(signal.SIGTERM, close_all) #kill python

socket_servo  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_camera = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_image  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#creation socket
socket_servo.bind(('192.168.43.171', 15554))
socket_camera.bind(('192.168.43.171', 15555))
socket_image.bind(('192.168.43.171', 15556))

socket_servo.listen(5)
socket_camera.listen(5)
socket_image.listen(5)

servo , address_servo  = socket_servo.accept()
camera, address_camera = socket_camera.accept()
image , address_image  = socket_image.accept()
#test image
image_cv = cv2.imread("img.jpg")
img_bytes = image_cv.tobytes()


t0 = time.time()
while time.time()-t0<300:
        #print("{} connected".format(address_servo))
        #print("{} connected".format(address_camera))

        ans_servo  = servo.recv(255)
        ans_camera = camera.recv(255)

        if ans_camera == '1':
                #print(len(img_bytes)) #921600
                print("sending images...")
                image.send( img_bytes )
                print("sent : ", len(img_bytes))

        #if servo != "":
        #        print("Servo : ", ans_servo)
        #if camera != "":
	#        print("Camera : ", ans_camera)

print("Close")
socket_image.close()
socket_servo.close()
socket_camera.close()