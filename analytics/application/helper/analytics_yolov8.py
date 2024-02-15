from .stream_cctv import StreamCctv
import cv2
import numpy as np
import os
import mysql.connector
import telepot
from scipy.spatial import distance as dist
from datetime import datetime, timedelta
import threading
from application.helper import YOLOV8_WEIGHTS, CUSTOM_TRACK
from numpy import random
from ultralytics import YOLO
import numpy as np
from collections import deque
import time


class AnalyticsCountingCrossing(StreamCctv):
    def __init__(self, data, socketio=None):
        super().__init__(data)
        self.model = YOLO(YOLOV8_WEIGHTS)
        self.line_warga = [(36, 428), (361, 335)] 
        self.data_deque = {}
        self.object_counter_s = {}
        self.object_counter_n = {}
        self.total_n = 0
        self.total_s = 0
        self.socketio = socketio

        #initialize database connection for class web streaming only
        self.connection = mysql.connector.connect(
            host=os.environ.get("DATABASE_HOST"),
            port=os.environ.get("DATABASE_PORT"),
            user=os.environ.get("DATABASE_USER"),
            passwd=os.environ.get("DATABASE_PASSWORD"),
            database=os.environ.get("DATABASE_NAME"),
            connect_timeout=60
        )

    def enumerate_thread(self):
        for thread in threading.enumerate():
            print(thread.name)

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            cursor.close()
            return cursor
        except mysql.connector.Error as err:
            print("Terjadi kesalahan [id_cctv: %s]:%s" % (self.id, err))
            return None
        
    def set_frame(self):
        if not self.online:
            self.data_deque = {}
            self.spin(1)
            return

        if self.deque and self.online:
            # Grab latest frame
            try:
                frame = self.deque[-1]
                frame = cv2.resize(frame,(1280,720),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)


                # # Add timestamp to cameras
                # cv2.rectangle(frame, (1280-190,0), (1280,50), color=(0,0,0), thickness=-1)
                # cv2.putText(frame, datetime.now().strftime('%H:%M:%S'), (1280-185,37), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), lineType=cv2.LINE_AA)
                # start_time = time.time()
                self.video_frame = self.analitik(frame)
                # end_time = time.time()  # Waktu selesai eksekusi
                # execution_time = end_time - start_time
                # with open(f'application/assets/output_{self.data["location"]}.txt', 'a') as file:
                #     file.write(f"Execution Time: {execution_time} seconds\n")
                # self.video_frame = frame
            except Exception as e:
                print(e)

    def detect(self):
        pass

    def is_point_inside_polygon(self, bbox, polygon_points):
        pass
    
    def ccw(self,A,B,C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    # def intersect(self,A,B,C,D):
    #     return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)
    def calculate_slope(self, x1, y1, x2, y2):
        # Hitung gradien dari garis yang didefinisikan oleh dua titik
        if x2 - x1 == 0:
            return None  # Gradien tak hingga
        return (y2 - y1) / (x2 - x1)

    def calculate_intercept(self, x, y, slope):
        # Hitung perpotongan garis dengan sumbu y
        if slope is None:
            return None  # Garis vertikal
        return y - slope * x

    def intersect(self, A, B, C, D):
        # Hitung gradien dan perpotongan garis dari line
        slope = self.calculate_slope(C[0], C[1], D[0], D[1])
        intercept = self.calculate_intercept(D[0], D[1] , slope)

        # Hitung nilai y yang diharapkan berdasarkan nilai x objek (x2 dan x3)
        y2_expected = slope * A[0] + intercept
        y3_expected = slope * B[0] + intercept

        # Periksa apakah objek melewati garis
        return (A[1] >= y2_expected and B[1] <= y3_expected) or (A[1] <= y2_expected and B[1] >= y3_expected)

    def get_direction(self, point1, point2):
        direction_str = ""

        # calculate y axis direction
        if point1[1] > point2[1]:
            direction_str += "in"
        elif point1[1] < point2[1]:
            direction_str += "out"
        else:
            direction_str += ""

        return direction_str
    
    def deviation_dict(self, track_id, name ,direction):
        return {"track_id": track_id, "type_object": name, "direction": direction}

    def analitik(self,frame):
        bus = 0
        motorcycle = 0
        car = 0
        truck = 0

        classes = [0,2,3,5,7] # person, car, motorcycle, bus, truck
        results = self.model.track(frame, tracker=CUSTOM_TRACK, save=False, classes=classes, persist=True, verbose=False)
        
        # Visualize the results on the frame
        res_plotted = results[0].plot(line_width=2, labels=False)
        cv2.line(res_plotted, self.line_warga[0], self.line_warga[1], (255, 84, 46), 4) # biru

        # Get the boxes and track IDs
        boxes = results[0].boxes.xyxy
        track_ids = results[0].boxes.id
        names = results[0].boxes.cls

        # remove tracked point from buffer if object is lost
        idx = []
        if track_ids != None:
            for i in track_ids:
                idx.append(int(i))
        for key in list(self.data_deque):
            if key not in idx:
                self.data_deque.pop(key)

        deviations = []
        # rules counting object
        if track_ids != None:
            # looping get id and counting
            for box, id, name in zip(boxes, track_ids, names):
                x1, y1, x2, y2 = box
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)
                id = int(id)
                obj_name = self.model.names[int(name)]
                cx, cy = int(x1+((x2-x1)/2)), int(y1+((y2-y1)/2))
                center = (cx, cy)

                if obj_name == 'car':
                    cv2.rectangle(res_plotted, (x1,y1), (x2,y2), (255,254,62), thickness=2) # cyan
                elif obj_name == 'motorcycle':
                    cv2.rectangle(res_plotted, (x1,y1), (x2,y2), (0,255,255), thickness=2) # yellow
                elif obj_name == 'bus':
                    cv2.rectangle(res_plotted, (x1,y1), (x2,y2), (255,0,249), thickness=2) # magenta
                elif obj_name == 'truck':
                    cv2.rectangle(res_plotted, (x1,y1), (x2,y2), (0,255,0), thickness=2) # green
                elif obj_name == 'person':
                    cv2.rectangle(res_plotted, (x1,y1), (x2,y2), (95,164,244), thickness=2) # Sandy Brown

                if id not in self.data_deque:  
                    self.data_deque[id] = deque(maxlen= 64)
                self.data_deque[id].appendleft(center)

                if len(self.data_deque[id]) >= 2:
                    direction = self.get_direction(self.data_deque[id][0], self.data_deque[id][1])
                    if self.intersect(self.data_deque[id][0], self.data_deque[id][1], self.line_warga[0], self.line_warga[1]):
                        cv2.line(res_plotted, self.line_warga[0], self.line_warga[1], (255, 255, 255), 4) # putih
                        if direction != "":
                            deviations.append(self.deviation_dict(id, obj_name, direction))

        mycursor = self.connection.cursor()
        # print(f"SELECT * FROM crossing_counting where created_at between where direction = 'out' and created_at between '{datetime.now().strftime('%Y-%m-%d')} 00:00:00' and '{datetime.now().strftime('%Y-%m-%d')} 23:59:59'")
        mycursor.execute(f"SELECT direction, COUNT(*) AS total_count FROM crossing_counting where (direction = 'in' OR direction = 'out') AND created_at between '{datetime.now().strftime('%Y-%m-%d')} 00:00:00' and '{datetime.now().strftime('%Y-%m-%d')} 23:59:59' GROUP BY direction")

        myresult = mycursor.fetchall()
        # print
        # test = test.fetch_all()
        total_out = 0
        total_in = 0
        if myresult:
            for result in myresult:
                if result[0] == 'in':
                    total_in = int(result[1])
                elif result[0] == 'out':
                    total_out = int(result[1])
        # print(myresult)
        cv2.line(res_plotted, (535,35), (765,35), (85,45,255), 35)
        cv2.putText(res_plotted, f'Kendaraan Keluar:', (525, 45), 0, 0.75, [255, 255, 255], thickness=2, lineType=cv2.LINE_AA)
        cv2.line(res_plotted, (535, 70), (700, 70), [85, 45, 255], 35)
        cv2.putText(res_plotted, f'Total : {total_out}', (525, 80), 0, 0.75, [255, 255, 255], thickness = 2, lineType = cv2.LINE_AA)

        cv2.line(res_plotted, (895,35), (1125,35), (85,45,255), 35)
        cv2.putText(res_plotted, f'Kendaraan Masuk:', (885, 45), 0, 0.75, [255, 255, 255], thickness=2, lineType=cv2.LINE_AA)    
        cv2.line(res_plotted, (895, 70), (1060, 70), [85,45,255], 35)
        cv2.putText(res_plotted, f'Total : {total_in}', (885, 80), 0, 0.75, [255, 255, 255], thickness=2, lineType=cv2.LINE_AA)
        list_of_notification = []
        if os.environ["SAVE_STREAMING_TO_DATABASE"] == "True":
            for deviation in deviations:
                sql_image = ("INSERT INTO realtime_images (cctv_id, image, avg_panjang_bbox_hd, created_at, updated_at, path)\
                        VALUES (%s, %s, %s, %s, %s, %s)")
                sql_counting = ("INSERT INTO crossing_counting (realtime_images_id, type_object, count, track_id, direction, created_at)\
                        VALUES (%s, %s, %s, %s, %s, %s)")
            
                address_img = './application/assets/output_folder/analytics_image'
                address_img_nobbox = './application/assets/output_folder/non_analytics_image'
                namafile_with_no_extension = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{str(self.data['name'])}_{str(self.data['location'])}_{deviation['type_object']}".replace(" ","").lower()
                namafile = f"{namafile_with_no_extension}.jpg"
                # namafile = str(datetime.now())+"_"+self.data["location"]+".jpg"
                sub_folder = f'crosing/{datetime.now().strftime("%Y-%m-%d")}/{deviation["type_object"]}'
                if not os.path.exists(f'{address_img}/{sub_folder}'):
                    os.makedirs(f'{address_img}/{sub_folder}')
                if not os.path.exists(f'{address_img_nobbox}/{sub_folder}'):
                    os.makedirs(f'{address_img_nobbox}/{sub_folder}')

                if os.path.exists(f'{address_img}/{sub_folder}'):
                    address_img = f'{address_img}/{sub_folder}/'
                if os.path.exists(f'{address_img_nobbox}/{sub_folder}'):
                    address_img_nobbox = f'{address_img_nobbox}/{sub_folder}/'
            
                path = ""
                if address_img.startswith('./application/'):
                    path = address_img.replace('./application/', '')

                dt = datetime.now()
                if(os.environ.get("SAVE_IMAGES_STREAMING") == "True"):
                    cv2.imwrite(address_img+namafile, res_plotted)
                    #----------write frame tanpa bounding box-----------------------
                    cv2.imwrite(address_img_nobbox+namafile, frame)
                value_image = (self.id, namafile, None, dt, dt, path)
                Image = self.execute_query(sql_image,value_image)
                idImage = Image.lastrowid

                val = (idImage, deviation['type_object'], 1, deviation['track_id'], deviation['direction'], dt)
                id_deviation = self.execute_query(sql_counting, val)
                list_of_notification.append(self.send_notif(idImage,id_deviation, self.id, str(
                                self.data["name"]), str(
                                self.data["location"]), deviation['type_object'], deviation['direction'], namafile, dt,path))

                try:
                    self.connection.commit()
                except:
                    print("Error commit")
            if(len(list_of_notification) > 0):
                # print(list_of_notification)
                self.socketio.emit('message_from_server', list_of_notification)
        return res_plotted
    
    def send_notif(self,id, deviation_id, cctv_id, name, location, object, direction, image, time, path):
        result = {
            'cctv_id': cctv_id,
            'realtime_images_id': id,
            'id': deviation_id,
            'image': image,
            'name': name,
            'location': location,
            'type_object': object,
            'direction': direction,
            'created_at': time,
            'updated_at': time,
            'path': path
        }
        return result