import cv2
#import imutils
#import time
import numpy as np
'''
import pafy

#url of the video to do face 
url = 'https://www.youtube.com/watch?v=iH1ZJVqJO3Y'
vPafy = pafy.new(url)
play = vPafy.getbest(preftype="mp4")
'''

cap = cv2.VideoCapture(0)

cap.set(3, 480) #set width of the frame
cap.set(4, 640) #set height of the frame

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(14, 17)', '(18, 19)','(20, 23)', '(25, 28)','(30,35)','(38, 43)', '(48, 53)', '(60, 100)']
gender_list = ['Male', 'Female']

#prototxt file means it contains layers of CNN
#caffemodel means it contains trained model

def initialize_caffe_models():
	#load .prototxt and caffemodel for both gender and Age
	age_net = cv2.dnn.readNetFromCaffe('deploy_age.prototxt', 'age_net.caffemodel') 

	gender_net = cv2.dnn.readNetFromCaffe('deploy_gender.prototxt', 'gender_net.caffemodel')

	return(age_net, gender_net)

def read_from_camera(age_net, gender_net):
	font = cv2.FONT_HERSHEY_SIMPLEX

	while True:

       #cap.read() returns a bool (True/False). If frame is read correctly, it will be True.
       #So you can check end of the video by checking this return value.
       #Sometimes, cap may not have initialized the capture. In that case, this code shows error. 
       #You can check whether it is initialized or not by the method cap.isOpened(). If it is True, OK. Otherwise open it using cap.open().
		ret, image = cap.read()
       
       #load pre built model for facial recognition
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
 
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		faces = face_cascade.detectMultiScale(gray, 1.1, 5)

		if(len(faces)>0):
			print("Found {} faces".format(str(len(faces))))

		for (x, y, w, h )in faces:
			cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 2)

			# Get Face 
			face_img = image[y:y+h, h:h+w].copy()
			blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

			#[blobFromImage] creates 4-dimensional blob from image. Optionally resizes and crops image from center,
             #subtract mean values, scales values by scalefactor , swap Blue and Red channels


			#Predict Gender
			gender_net.setInput(blob)
			gender_preds = gender_net.forward()
			gender = gender_list[gender_preds[0].argmax()]
			print("Gender : " + gender)

			#Predict Age
			age_net.setInput(blob)
			age_preds = age_net.forward()
			age = age_list[age_preds[0].argmax()]
			print("Age Range: " + age)

			overlay_text = "%s %s" % (gender, age)
			cv2.putText(image, overlay_text, (x, y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)


		cv2.imshow('frame', image)
       #0xFF is a hexadecimal constant which is 11111111 in binary.
       #By using bitwise AND (&) with this constant, it leaves only the last 8 bits of the original (in this case, whatever cv2.waitKey(0) is).
		if cv2.waitKey(1) & 0xFF == ord('q'): 
			break

if __name__ == "__main__":
	age_net, gender_net = initialize_caffe_models()

	read_from_camera(age_net, gender_net)