from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type =str, default="C:/Users/DELL/Downloads/videoplayback.mp4")
ap.add_argument("-t","--tracker",type=str,default="kcf",
	help="OpenCV object tracker type")
args=vars(ap.parse_args())

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
 
if __name__ == '__main__' :
 
    # Set up tracker.
    # Instead of MIL, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]
if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()

	tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

initBB=None	

if not args.get("video",False):
	print("[INFO] starting video stream...")
	vs=VideoStream(src=1).start()
	time.sleep(1.0)

else:
	vs=cv2.VideoCapture(args["video"])

fps=None


while True:
	# grab the current frame, then handle if we are using a
	# VideoStream or VideoCapture object
	frame = vs.read()
	frame = frame[1] if args.get("video", False) else frame
 
	# check to see if we have reached the end of the stream
	if frame is None:
		break
 
	# resize the frame (so we can process it faster) and grab the
	# frame dimensions
	frame = imutils.resize(frame, width=500)
	(H, W) = frame.shape[:2]

if initBB is not None:
		# grab the new bounding box coordinates of the object
		(success, box) = tracker.update(frame)
 
		# check to see if the tracking was a success
		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h),
				(0, 255, 0), 2)
 
		# update the FPS counter
		fps.update()
		fps.stop()
 
		# initialize the set of information we'll be displaying on
		# the frame
		info = [
			("Tracker", args["tracker"]),
			("Success", "Yes" if success else "No"),
			("FPS", "{:.2f}".format(fps.fps())),
		]
 
		# loop over the info tuples and draw them on our frame
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
 
	# if the 's' key is selected, we are going to "select" a bounding
	# box to track
		if key == ord("s"):
		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
			initBB = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)
 
		# start OpenCV object tracker using the supplied bounding box
		# coordinates, then start the FPS throughput estimator as well
		tracker.init(frame, initBB)
		fps = FPS().start()
 		cv2.imshow("Tracking", frame);
		
        
# if we are using a webcam, release the pointer
if not args.get("video", False):
	vs.stop()
 
# otherwise, release the file pointer
else:
	vs.release()
 
# close all windows
cv2.destroyAllWindows()