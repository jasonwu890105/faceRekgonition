from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import json
import time, base64

from picamera import PiCamera #Pi Camera Library

from PIL import Image #Pillow library to convert photo to memory buffer
import requests    #To make api call
from time import time, sleep
import io, json

photo_taken_time = int(time())
stream = io.BytesIO() # Set up a stream object for the photo taken

### Taking photos
with PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview(fullscreen=False, window=(100, 20, 640, 480))
    sleep(3)
    camera.capture(stream, format='jpeg') #Buffered image stream wihch will be sent to API GW on-the-fly

stream.seek(0)
#a = stream.read()
#pic = str(base64.b64encode(a))
#a = stream.getvalue()
a = base64.b64encode(stream.getvalue()).decode()
def customCallback(client, userdata, message):
    print(message.payload)
    print('from topic: ')
    print(message.topic)
    
host = 'a3g2q7v45ktx5e-ats.iot.ap-southeast-2.amazonaws.com'
port = 8883
rootCAPath = '/home/pi/Desktop/certs/AmazonRootCA1.pem'
privateKeyPath = '/home/pi/Desktop/certs/7691ad2e74-private.pem.key'
certificatePath = '/home/pi/Desktop/certs/7691ad2e74-certificate.pem.crt'
clientId = 'test'
myAWSIotMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIotMQTTClient.configureEndpoint(host, port)
myAWSIotMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

myAWSIotMQTTClient.connect()
myAWSIotMQTTClient.publish('test', a, 1)