import RPi._GPIO as GPIO
import time
import socket
import sys
import signal

#Initialisation du Server
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "172.20.21.164"
port = 15554

buffer_size = 256

#Initialisation du Servo-Moteur
GPIO.cleanup()
servoPIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO PIN for PWM with 50Hz
p.start(0) # Initialization

# Captation des Signaux
def close(signal, frame):
    #close socket
    serverSocket.close()
    #close and clean gpio
    p.stop()
    GPIO.cleanup()
    print 'SIG:'+ str(signal) + 'Program Interupted'
    sys.exit()

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

signal.signal(signal.SIGINT, close)
signal.signal(signal.SIGTERM, close)
signal.signal(signal.SIGQUIT, close)
signal.signal(signal.SIGTSTP, close)

#######---MAIN---#######
if __name__=='__main__':

    try:
        serverSocket.bind((host, port))
<<<<<<< HEAD
        print 'Connected Waiting for request:'
        serverSocket.listen(5)
        clientSocket, address = serverSocket.accept()   #Accepte connection
=======
        serverSocket.listen(5)
        clientSocket, address = serverSocket.accept()
        print 'Connected Waiting for request:'
>>>>>>> dd6850e9e176fc8ddd0fff2fde6a22a7caf417e6
    except socket.error as msg:
        print 'Bind fail : ' + str(msg[0]) + 'MESSAGE= '+ msg[1]
        close('sys exit', None)


    while True:
<<<<<<< HEAD
    	angle = clientSocket.recv(buffer_size)          #Recoit buffer
        angle = angle.decode()
        if angle == '':
            pass
        else:
            angle = (int(angle)/180.0)*5.0 + 5.0
            try:
                p.ChangeDutyCycle(float(angle))
                time.sleep(0.5)
            except:
                print 'Change Duty cycle FAIL'
                close('sys exit', None)
=======
    	  angle = clientSocket.recv(buffer_size)          #Recoit buffer
        angle = angle.decode()                          #Convertion string
        angle = int(angle)/10 + 5                       #Converion angle

        try:
            p.ChangeDutyCycle(angle)
            time.sleep(0.5)
        except:
            print 'Change Duty cycle FAIL'
            sys.exit()
>>>>>>> dd6850e9e176fc8ddd0fff2fde6a22a7caf417e6
