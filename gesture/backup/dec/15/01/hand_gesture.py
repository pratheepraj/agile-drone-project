# IMPORTING LIBRARIES
import time
import numpy as np
import cv2
import math
from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

#class
class hand(object):

	upload_flag=1





		#LOADING HAND CASCADE
	hand_cascade = cv2.CascadeClassifier('hand_haar_cascade.xml')

# VIDEO CAPTURE
	cap = cv2.VideoCapture(0)
	while 1:
		ret, img = cap.read()
		blur = cv2.GaussianBlur(img,(27,27),0) # BLURRING IMAGE TO SMOOTHEN EDGES
		#BGR->grey
		gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
		#threshold the image
		retval2,thresh1 = cv2.threshold(gray,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
		#detecting hand in threshold image
		hand = hand_cascade.detectMultiScale(thresh1, 1.3, 5)
		#create mask
		mask = np.zeros(thresh1.shape, dtype = "uint8")
		#detecting roi
		for (x,y,w,h) in hand:
			cv2.rectangle(img,(x,y),(x+w,y+h), (122,122,0), 2)
			cv2.rectangle(mask, (x,y),(x+w,y+h),255,-1)
		img2 = cv2.bitwise_and(thresh1, mask)
		final = cv2.GaussianBlur(img2,(7,7),0)
		contours, hierarchy = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		cv2.drawContours(img, contours, 0, (255,255,0), 3)
		cv2.drawContours(final, contours, 0, (255,255,0), 3)

		if len(contours) > 0:
			cnt=contours[0]
			hull = cv2.convexHull(cnt, returnPoints=False)
			# finding convexity defects
			defects = cv2.convexityDefects(cnt, hull)
			count_defects = 0
			# applying Cosine Rule to find angle for all defects (between fingers)
			# with angle > 90 degrees and ignore defect
			if defects is not None:
				for i in range(defects.shape[0]):
					p,q,r,s = defects[i,0]
					finger1 = tuple(cnt[p][0])
					finger2 = tuple(cnt[q][0])
					dip = tuple(cnt[r][0])
					# find length of all sides of triangle
					a = math.sqrt((finger2[0] - finger1[0])**2 + (finger2[1] - finger1[1])**2)
					b = math.sqrt((dip[0] - finger1[0])**2 + (dip[1] - finger1[1])**2)
					c = math.sqrt((finger2[0] - dip[0])**2 + (finger2[1] - dip[1])**2)
					# apply cosine rule here
					angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57.29
					# ignore angles > 90 and highlight rest with red dots
					if angle <= 90:
						count_defects += 1
			# define actions required
			if count_defects == 1:
				#cv2.putText(img,"2", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, 4)
				cv2.putText(img, '2', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 20, cv2.LINE_AA)
			elif count_defects==0:
				#cv2.putText(img,"1", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, 4)
				cv2.putText(img, '1', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 20, cv2.LINE_AA)
			elif count_defects == 2:
				#cv2.putText(img, "3", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, 4)
				cv2.putText(img, '3', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 20, cv2.LINE_AA)
			elif count_defects == 3:
				#cv2.putText(img,"4", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, 4)
				#cv2.putText(img, '4 : Upload image', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 20, cv2.LINE_AA)
				if upload_flag == 1:
					cv2.putText(img, '4 : Upload image', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 20, cv2.LINE_AA)

					message = " Hi firends! Yay!!! this is my 3rd tweet using api and Hangesture. Hi firends! And Gesture raed is 4 fingers to upload tweet and image on twitter"
					image = open('saiful-100-100.jpg', 'rb')

					response = twitter.upload_media(media=image)
					media_id = [response['media_id']]

					twitter.update_status(status=message, media_ids=media_id)


					upload_flag = 0
				if upload_flag == 0:
					cv2.putText(img, '4', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 20, cv2.LINE_AA)
					cv2.putText(img, 'Image Uploaded', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 20, cv2.LINE_AA)




			elif count_defects == 4:
				#cv2.putText(img,"THIS IS 5", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, 4)
				cv2.putText(img, '5', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 20, cv2.LINE_AA)

		cv2.imshow('img',thresh1)
		cv2.imshow('img1',img)
		cv2.imshow('img2',img2)

		k = cv2.waitKey(30) & 0xff
		#if k == 27:
		#	break
	cap.release()
	cv2.destroyAllWindows()
