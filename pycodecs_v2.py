import cv2, time
from datetime import datetime

first_frame = None
status_list = [None,None]
times = []
burst = [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10" ]

# For third party Camera USB
#video = cv2.VideoCapture(1 + cv2.CAP_DSHOW())
video = cv2.VideoCapture(1)

while True:
  
    check, frame = video.read()

    hour = time.strftime('%H')
    hour = int(hour)

    status = 0
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
      first_frame = gray
      continue

    delta_frame = cv2.absdiff(first_frame,gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # wait
    time.sleep(0.4)

    for contour in cnts:
      if cv2.contourArea(contour) < 20000:
          continue
      status = 1

      (x, y, w, h)=cv2.boundingRect(contour)
      cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)

    status_list.append(status)

    status_list=status_list[-2:]


    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())

        # check
        if hour < 5:
          time.sleep(10)
          continue
            
      #  if hour > 7 & hour < 17:
      #    time.sleep(10)
      #    continue
            
        if hour > 19:
          time.sleep(10)
          continue
          
        # burst
        for x in burst:
          
          #print(x)
          #time.sleep(1)
          # call again while after stabilizing the image
          check2, frame2 = video.read()
          # save image
          cv2.imwrite("./images/" + time.strftime("%Y%m%d-%H%M%S") + "-" + x +".jpg", frame2)
          


    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())


    cv2.imshow("Gray Frame",gray)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("Color Frame",frame)
    
    
    key=cv2.waitKey(1)

    if key == ord('q'):
      if status == 1:
          times.append(datetime.now())
      break

print(status_list)
print(times)

video.release()
cv2.destroyAllWindows