import cv2
import os
import time
from datetime import datetime, timedelta
from collections import deque
from threading import Thread
import numpy as np

class StreamCctv:
    def __init__(self, data, socketio=None, deque_size = 1):
        # identity
        self.id = data["id"]
        self.name = data["name"]
        self.camera_stream_link = data["link_rtsp"]
        self.data = data

        # camera
        self.deque = deque(maxlen=deque_size)
        self.online = False
        self.video_frame = None
        self.capture = None
        self.exit = False
        self.count = 1

        self.load_network_stream()
        
        # Start background frame grabbing
        self.get_frame_thread = Thread(target=self.get_frame, args=(), name=f"get_frame ::: {str(self.id)}")
        self.get_frame_thread.daemon = True
        self.get_frame_thread.start()

        # self.set_frame_thread = Thread(target=self.set_frame_loop, args=(), name=f"set_frame ::: {str(self.id)}")
        # self.set_frame_thread.daemon = True
        # self.set_frame_thread.start()


        print('Started camera: {}'.format(self.camera_stream_link))

    def load_network_stream(self):
        """Verifies stream link and open new stream if valid"""
        
        def load_network_stream_thread():
            if self.verify_network_stream(self.camera_stream_link):
                self.capture = cv2.VideoCapture(self.camera_stream_link)
                self.online = True
                print('loaded:', self.camera_stream_link)
        self.load_stream_thread = Thread(target=load_network_stream_thread, args=(), name="load_network_stream_thread ::: "+str(self.id))
        self.load_stream_thread.daemon = True
        self.load_stream_thread.start()
        self.load_stream_thread.join()
        print('thread loaded', self.camera_stream_link)
        self.count = 1
    
    def verify_network_stream(self, link):
        """Attempts to receive a frame from given link"""
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"]="rtsp_transport;tcp|analyzeduration;2000|"

        cap = cv2.VideoCapture(link, cv2.CAP_FFMPEG)
        if not cap.isOpened():
            return False
        cap.release()
        print("verify", self.camera_stream_link)
        return True
    
    def get_frame(self):
        """Reads frame, resizes, and converts image to pixmap"""
        fpsLimit = 1
        prev = 0
        while True:
            try:
                # self.get_memory_usage()
                if self.exit:
                    break
                if self.capture is None or not self.capture.isOpened():
                    self.load_network_stream()
                if self.capture.isOpened() and self.online:
                    # Read next frame from stream and insert into deque
                    time_elapsed = time.time() - prev
                    status, frame = self.capture.read()
                    if status:
                        if float(self.capture.get(cv2.CAP_PROP_FRAME_COUNT)) < 0:
                            if time_elapsed > 1/fpsLimit:
                                prev = time.time()
                                self.deque.append(frame)
                                self.set_frame()
                        else:
                            self.deque.append(frame)
                            self.set_frame()
                            self.count += int(self.capture.get(cv2.CAP_PROP_FPS))
                            # self.count += 1
                            self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.count)

                    else:
                        self.capture.release()
                        self.online = False
                        print('status offline', self.camera_stream_link)
                else:
                    # Attempt to reconnect
                    print('attempting to reconnect', self.camera_stream_link)
                    self.load_network_stream()
                    self.spin(2)
                self.spin(.001)
            except AttributeError:
                pass

    def spin(self, seconds):
        time.sleep(seconds)

    def set_frame(self):
        if not self.online:
            self.spin(1)
            # return

        if self.deque and self.online:
            # Grab latest frame
            try:
                frame = self.deque[-1]
                frame = cv2.resize(frame,(1280,720),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)

                # Add timestamp to cameras
                cv2.rectangle(frame, (1080-190,0), (1080,50), color=(0,0,0), thickness=-1)
                cv2.putText(frame, datetime.now().strftime('%H:%M:%S'), (1080-185,37), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), lineType=cv2.LINE_AA)

                self.video_frame = frame
            except Exception as e:
                print(e)

    def set_frame_loop(self):
        while True:
            self.set_frame()

    def get_video_frame(self):
        return self.video_frame
    
    def generate_frame(self):
        while True:
            try:
                frame = self.get_video_frame()
                (flag, encodedImage) = cv2.imencode(".jpg", frame)
            except:
                frame = np.zeros((720, 1280, 3), np.uint8)
                frame = cv2.putText(frame, "Camera Offline", (1050//2, 720//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                (flag, encodedImage) = cv2.imencode(".jpg", frame)
            finally:
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                            bytearray(encodedImage) + b'\r\n')
                
    def exit_object(self):      
        print("start process thread get frame")
        try:
            self.exit = True
            time.sleep(5)
            self.get_frame_thread.join()
        except:
            print("error terminate thread")
    
    def reload(self):
        if self.capture is None or not self.capture.isOpened():
            self.capture.release()
            self.load_network_stream()

        time.sleep(2)

        try:
            self.exit = True
            time.sleep(5)
            self.get_frame_thread.join()
            self.exit = False
        except:
            print("error terminate thread")
        self.get_frame_thread = Thread(target=self.get_frame, args=(), name=f"get_frame ::: {str(self.id)}")
        self.get_frame_thread.daemon = True
        self.get_frame_thread.start()
    
