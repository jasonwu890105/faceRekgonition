from picamera import PiCamera #Pi Camera Library

from PIL import Image #Pillow library to convert photo to memory buffer
import requests    #To make api call
from time import time, sleep
import io, json
import sys, base64

photo_taken_time = int(time())
stream = io.BytesIO() # Set up a stream object for the photo taken

### Taking photos
with PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview(fullscreen=False, window=(100, 20, 640, 480))
    sleep(3)
    camera.capture(stream, format='jpeg') #Buffered image stream wihch will be sent to API GW on-the-fly

stream.seek(0) #Before this sys call, the stream is at the end of its position, which means if we don't call the stream to go back to its first position(0 posibtion), the data will actually will none/null(0)

name = input('Please Enter this person name (eg, jason_wu, please include underscore in between first and last.): ')

# Jason's API : url_index_faces = 'https://ohxiwbxnwf.execute-api.ap-southeast-2.amazonaws.com/dev' # This is the api call to facerekgonition lambda function
url_index_faces = 'https://ul9xu8s6f0.execute-api.ap-northeast-1.amazonaws.com/dev'
try:
    
    res = requests.post(url = url_index_faces,
                        data = stream,
                        params={'photoname':name},
                        headers = {'Content-Type': 'application/octet-stream'}) # Make sure the API has settings to accept binary data
    
    print('{} has been added into collection, visitor can now access your home'.format(name))

except Exception as e:
    
    print(str(e))


