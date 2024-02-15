from .stream_cctv import StreamCctv
import cv2
import numpy as np
import os
import mysql.connector
import telepot
from scipy.spatial import distance as dist
from datetime import datetime, timedelta
import threading
from application.helper import AREAPRODUKSI_CONFIG, AREAPRODUKSI_WEIGHTS, AREAPRODUKSI_DATASET
from matplotlib.path import Path
import time
# from application import socketio

class AnalyticsThreeClass(StreamCctv):
    def __init__(self, data, MIN_CONF = 0.2, NMS_THRESH = 0.001, socketio=None):
        super().__init__(data)
        # init bot
        self.bot = telepot.Bot(os.environ.get("ID_BOT_TELEGRAM"))
        self.chat_id = os.environ.get('ID_GROUP_CHAT')
        self.NUM_RETRIES_BOT = 3
        self.RETRY_DELAY_BOT = 5
        self.telegram_on = False
        # init cv to set weights and config also cuda
        self.MIN_CONF = MIN_CONF
        self.NMS_THRESH = NMS_THRESH
        self.net = cv2.dnn.readNetFromDarknet(AREAPRODUKSI_CONFIG, AREAPRODUKSI_WEIGHTS)
        try:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
            print("[INFO set to cuda]")
        except:
            print("[INFO set to CPU] Failed to using GPU")
        try:
            self.ln = [self.net.getLayerNames()[i - 1]
                    for i in self.net.getUnconnectedOutLayers()]
        except:
            self.ln = [self.net.getLayerNames()[i[0] - 1]
                    for i in self.net.getUnconnectedOutLayers()]
        self.labels = open(AREAPRODUKSI_DATASET).read().strip().split("\n")
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

        # init perimeter
        self.polygon = []
        self.outside_secure_area = False
        self.object_perimeter = ["HD"]

        self.id_parrent_deviations_person = 0
        self.id_parrent_deviations_lv = 0
        self.time_deviasi_person = datetime.now() - timedelta(seconds=10)
        self.time_deviasi_lv = datetime.now() - timedelta(seconds=10)
        self.count_object_person = -1
        self.count_object_lv = -1

        self.distance_hd = 4

        self.time = datetime.now()

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

    def detect(self, frame, net, ln, Idx):
        # grab the dimensions of the frame and  initialize the list of
        # results
        (H, W) = frame.shape[:2]
        results = []

        # construct a blob from the input frame and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes
        # and associated probabilities
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (480, 480),
            swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)

        # initialize our lists of detected bounding boxes, centroids, and
        # confidences, respectively
        boxes = []
        centroids = []
        confidences = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter detections by (1) ensuring that the object
                # detected was a object and (2) that the minimum
                # confidence is met
                if classID == Idx and confidence > self.MIN_CONF:
                    # scale the bounding box coordinates back relative to
                    # the size of the image, keeping in mind that YOLO
                    # actually returns the center (x, y)-coordinates of
                    # the bounding box followed by the boxes' width and
                    # height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top
                    # and and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates,
                    # centroids, and confidences
                    boxes.append([x, y, int(width), int(height)])
                    centroids.append((centerX, centerY))
                    confidences.append(float(confidence))

        # apply non-maxima suppression to suppress weak, overlapping
        # bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.MIN_CONF, self.NMS_THRESH)

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # update our results list to consist of the object
                # prediction probability, bounding box coordinates,
                # and the centroid
                r = (confidences[i], (x, y, x + w, y + h), centroids[i])
                results.append(r)

        # return the list of results
        return results
    
    def is_point_inside_polygon(self, bbox, polygon_points):
        rectangle = [(bbox[0], bbox[1]), (bbox[2], bbox[1]), (bbox[2], bbox[3]), (bbox[0], bbox[3])]
        path = Path(polygon_points)
        return all(path.contains_points(rectangle))
    
    def analitik(self,frame):
        frame_nonanalitik = frame.copy()
        results_person = self.detect(frame, self.net, self.ln,
                                            Idx=self.labels.index("person"))

        results_hd = self.detect(frame, self.net, self.ln,
                                    Idx=self.labels.index("HD"))

        results_lv = self.detect(frame, self.net, self.ln,
                                    Idx=self.labels.index("LV"))

        if "Person" in self.object_perimeter:
            cv2.polylines(frame, [np.array(self.polygon, dtype=np.int32)], True, (1, 216, 255), thickness=2)
        if "HD" in self.object_perimeter:
            cv2.polylines(frame, [np.array(self.polygon, dtype=np.int32)], True, (153, 51, 255), thickness=2)
        if "LV" in self.object_perimeter:
            cv2.polylines(frame, [np.array(self.polygon, dtype=np.int32)], True, (255, 51, 153), thickness=2)

        # person analitik -----------------------------------------------------------------------
        count_person_no_risk = 0
        for (i, (prob, bbox, centroid)) in enumerate(results_person):
            # extract the bounding box and centroid coordinates, then initialize the color of the annotation
            (startX, startY, endX, endY) = bbox
            color = (0, 0, 255)

            if len(self.polygon) > 2 and "Person" in self.object_perimeter:
                if self.is_point_inside_polygon(bbox, self.polygon) != self.outside_secure_area:
                    count_person_no_risk += 1
                    color = (0, 255, 0) #green
                else:
                    color = (0, 0, 255)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        # HD analitik ----------------------------------------------------------------------------
        # initialize the set of indexes that violate the minimum social distance
        violate_hd = set()

        # ensure there are *at least* two people detections (required in
        # order to compute our pairwise distance maps)
        avg_panjang_bbox_hd = None
        if len(results_hd) >= 2:
            # extract all centroids from the results and compute the Euclidean distances between all pairs of the centroids
            centroids = np.array([r[2] for r in results_hd])
            # print("centroids", centroids)
            coordinates = np.array([r[1] for r in results_hd])
            # print("coordinates", coordinates)
    
            D = dist.cdist(centroids, centroids, metric="euclidean")
            list_panjang_bbox_hd = []

            for (i, (prob, bbox, centroid)) in enumerate(results_hd):
                (startX, startY, endX, endY) = bbox
                panjang_bbox_hd = np.abs(endX-startX)
                # print("Panjang HD : ", panjang_bbox_hd)
                # text_panjang_bbox_hd = " {} ".format(panjang_bbox_hd)
                # cv2.putText(frame, text_panjang_bbox_hd, (endX, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                list_panjang_bbox_hd.append(panjang_bbox_hd)
            avg_panjang_bbox_hd = sum(list_panjang_bbox_hd)/len(list_panjang_bbox_hd)

            # loop over the upper triangular of the distance matrix
            for i in range(0, D.shape[0]):
                for j in range(i + 1, D.shape[1]):

                    panjang_bbox_hd1 = np.abs(coordinates[i][2]-coordinates[i][0])
                    # print("panjang hd pertama : {}".format(panjang_bbox_hd1))
                    panjang_bbox_hd2 = np.abs(coordinates[j][2]-coordinates[j][0])
                    # print("panjang hd kedua : {}".format(panjang_bbox_hd2))

                    if panjang_bbox_hd1 > panjang_bbox_hd2:
                        max_panjang_hd = panjang_bbox_hd1
                    else:
                        max_panjang_hd = panjang_bbox_hd2

                    panjang_distance_hd = self.distance_hd*max_panjang_hd
                    # print("panjang 3x hd : ", panjang_distance_hd)


                    # check to see if the distance between any two centroid pairs is less than the configured number of pixels
                    if D[i, j] < panjang_distance_hd:
                        # cv2.line(frame, (centroids[i][0], centroids[i][1]), (centroids[j][0], centroids[j][1]), (0,0,255), 2)
                        # print("jarak violate hd terdeteksi {} pixel : ".format(round(panjang_distance_hd, 2)))

                        # text_jarak_violate_hd = " {} ".format(round(panjang_distance_hd, 2))
                        # cv2.putText(frame, text_jarak_violate_hd, (centroids[i][0], centroids[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 225, 0), 2)

                        # update our violation set with the indexes of the centroid pairs
                        violate_hd.add(i)
                        violate_hd.add(j)

        count_hd_no_risk = 0
        for (i, (prob, bbox, centroid)) in enumerate(results_hd):
            # extract the bounding box and centroid coordinates, then initialize the color of the annotation
            (startX, startY, endX, endY) = bbox
            color = (0, 255, 0)
            
            if len(self.polygon) > 2 and  "HD" in self.object_perimeter:
                if self.is_point_inside_polygon(bbox, self.polygon) != self.outside_secure_area:
                    count_hd_no_risk += 1
                    color = (0, 255, 0)  
                else:
                    color = (0, 0, 255)
            if i in violate_hd:
                color = (0, 0, 255)

            # draw (1) a bounding box around the object and (2) the centroid coordinates of the object,
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        # LV analitik --------------------------------------------------------------------------------
        # initialize the set of indexes that violate the minimum social distance
        violate_lv = set()
        # ensure there are *at least* two people detections (required in order to compute our pairwise distance maps)
        if len(results_lv) >= 2:
            # extract all centroids from the results and compute the Euclidean distances between all pairs of the centroids
            centroids = np.array([r[2] for r in results_lv])
            D = dist.cdist(centroids, centroids, metric="euclidean")

            # loop over the upper triangular of the distance matrix
            for i in range(0, D.shape[0]):
                for j in range(i + 1, D.shape[1]):
                    # check to see if the distance between any two
                    # centroid pairs is less than the configured number
                    # of pixels
                    if D[i, j] < 100:
                        # update our violation set with the indexes of the centroid pairs
                        violate_lv.add(i)
                        violate_lv.add(j)

        # loop over the results
        count_lv_no_risk = 0
        for (i, (prob, bbox, centroid)) in enumerate(results_lv):
            # extract the bounding box and centroid coordinates, then initialize the color of the annotation
            (startX, startY, endX, endY) = bbox
            color = (0, 0, 255)

            Cx , Cy = centroid
            if len(self.polygon) > 2 and "LV" in self.object_perimeter:
                if self.is_point_inside_polygon(bbox, self.polygon) != self.outside_secure_area:
                    count_lv_no_risk += 1
                    color = (0, 255, 0)  
                else:
                    color = (0, 0, 255)

            # draw (1) a bounding box around the object and (2) the centroid coordinates of the object,
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

    # text analitik -------------------------------------------------------------------------------------
        # draw the total number of social distancing violations on the output frame
        text_person = "Jumlah Manusia Terdeteksi : {}".format(len(results_person) - count_person_no_risk)
        cv2.putText(frame, text_person, (int(os.environ.get("TEXT_VERTIKAL")), int(os.environ.get("TEXT_HORIZONTAL"))),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

        text_hd = "HD Tidak Menjaga Jarak : {}".format(len(violate_hd))
        cv2.putText(frame, text_hd, (int(os.environ.get("TEXT_VERTIKAL")), int(os.environ.get("TEXT_HORIZONTAL"))+35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

        text_lv = "Jumlah LV Terdeteksi : {}".format(len(results_lv) - count_lv_no_risk)
        cv2.putText(frame, text_lv, (int(os.environ.get("TEXT_VERTIKAL")), int(os.environ.get("TEXT_HORIZONTAL"))+70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        
        if "HD" in self.object_perimeter and len(self.polygon) > 2:
            text_jumlah_hd = "Jumlah HD Terdeteksi di area tidak aman: {}".format(len(results_hd)-count_hd_no_risk)
            cv2.putText(frame, text_jumlah_hd, (int(os.environ.get("TEXT_VERTIKAL")), int(os.environ.get("TEXT_HORIZONTAL"))+105),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
            
        # self.socketio.emit('testing', [{"testing": "123"}])

        if os.environ.get("SAVE_STREAMING_TO_DATABASE") == "True":
            sql_image = ("INSERT INTO realtime_images (cctv_id, image, avg_panjang_bbox_hd, created_at, updated_at, path)\
                    VALUES (%s, %s, %s, %s, %s, %s)")
            sql_deviation = ("INSERT INTO realtime_deviations (parent_id, realtime_images_id, type_object, type_validation, violate_count, created_at)\
                    VALUES (%s, %s, %s, %s, %s, %s)")
            if(len(results_person) - count_person_no_risk > 0) or (len(violate_hd) > 0) or (len(results_lv) - count_lv_no_risk > 0) or ((len(results_hd) - count_hd_no_risk > 0) and len(self.polygon) > 2):
                # Name of image deviation
                address_img = './application/assets/output_folder/analytics_image'
                address_img_nobbox = './application/assets/output_folder/non_analytics_image'
                type_deviation = []
                if len(violate_hd) > 0:
                    type_deviation.append('hd')
                if len(results_lv) - count_lv_no_risk > 0:
                    type_deviation.append('lv')
                if len(results_person) - count_person_no_risk > 0:
                    type_deviation.append('person')
                if (len(results_hd) - count_hd_no_risk > 0) and len(self.polygon) > 2:
                    type_deviation.append('perimeter')
                type_deviation = "_".join(type_deviation)
                namafile_with_no_extension = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{str(self.data['name'])}_{str(self.data['location'])}_{type_deviation}".replace(" ","").lower()
                namafile = f"{namafile_with_no_extension}.jpg"
                # namafile = str(datetime.now())+"_"+self.data["location"]+".jpg"
                sub_folder = f'{datetime.now().strftime("%Y-%m-%d")}/{type_deviation}'
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
                dt_notif = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
                list_of_notification = []

                if dt - self.time > timedelta(seconds=1):
                    print(f'[{dt}] [CCTV {self.data["name"]} - {self.data["location"]}] : Deviasi terdeteksi (Person : {len(results_person)} ) (HD: {len(violate_hd)} ) (LV: {len(results_lv)} )')
                    if(os.environ.get("SAVE_IMAGES_STREAMING") == "True"):
                        cv2.imwrite(address_img+namafile, frame)
                        #----------write frame tanpa bounding box-----------------------
                        cv2.imwrite(address_img_nobbox+namafile, frame_nonanalitik)
                    value_image = (self.id, namafile, avg_panjang_bbox_hd, dt, dt, path)
                    Image = self.execute_query(sql_image,value_image)
                    idImage = Image.lastrowid

                    if(len(results_person) > 0 and os.environ.get("SAVE_PERSON_TO_DATABASE") == "True"):
                        if dt - self.time_deviasi_person <= timedelta(seconds=2) and (self.count_object_person == len(results_person)):
                            self.time_deviasi_person = dt
                            self.count_object_person = len(results_person)
                            val = (self.id_parrent_deviations_person, idImage, "Person", "not_yet", len(results_person), dt)
                            id_deviation = self.execute_query(sql_deviation, val)
                            id_deviation = id_deviation.lastrowid
                            list_of_notification.append(self.send_notif(idImage, id_deviation,self.id_parrent_deviations_person, self.id, str(
                                self.data["name"]), str(
                                self.data["location"]), 'Person', 'not_yet', namafile, dt_notif,path))
                        else:
                            self.time_deviasi_person = dt
                            self.count_object_person = len(results_person)
                            val = (None,idImage, "Person", "not_yet", len(results_person), dt)

                            id_parrent_deviations = self.execute_query(sql_deviation, val)
                            self.id_parrent_deviations_person = id_parrent_deviations.lastrowid
                            list_of_notification.append(self.send_notif(idImage, self.id_parrent_deviations_person,None, self.id, str(
                                self.data["name"]), str(
                                self.data["location"]), 'Person', 'not_yet', namafile, dt_notif,path))
                            if (os.environ.get("TELEGRAM_PERSON") == "True" and self.telegram_on):
                                try:
                                    with open(address_img+namafile, 'rb') as photo:
                                        self.bot.sendPhoto(self.chat_id, photo=photo, caption=self.formatMessageTelebot(self.data["location"], self.data["name"], "PERSON", len(results_person), dt_notif))
                                except Exception as e:
                                    print(f"Error: {e}")

                    if(len(violate_hd) > 0 and os.environ.get("SAVE_HD_TO_DATABASE") == "true"):
                        val = (None,idImage, "HD", "not_yet", len(violate_hd), dt)
                        id_parrent_deviations = self.execute_query(sql_deviation, val)
                        self.id_parrent_deviations_hd = id_parrent_deviations.lastrowid
                        list_of_notification.append(self.send_notif(idImage, self.id_parrent_deviations_hd, None, self.id, str(
                            self.data["name"]), str(
                            self.data["location"]), 'HD', 'not_yet', namafile, dt_notif,path))
                        if (os.environ.get("TELEGRAM_HD") == "True" and self.telegram_on):
                            try:
                                with open(address_img+namafile, 'rb') as photo:
                                    self.bot.sendPhoto(self.chat_id, photo=photo, caption=self.formatMessageTelebot(self.data["location"], self.data["name"], "HD", len(violate_hd), dt_notif))
                            except Exception as e:
                                print(f"Error: {e}")
                    
                    if(len(results_lv) > 0 and os.environ.get("SAVE_LV_TO_DATABASE") == "True"):
                        if (dt - self.time_deviasi_lv <= timedelta(seconds=2)) and (self.count_object_lv == len(results_lv)):
                            self.count_object_lv = len(results_lv)
                            self.time_deviasi_lv = dt
                            val = (self.id_parrent_deviations_lv,idImage, "LV", "not_yet", len(results_lv), dt)
                            id_deviation = self.execute_query(sql_deviation, val)
                            id_deviation = id_deviation.lastrowid
                            list_of_notification.append(self.send_notif(idImage,id_deviation, self.id_parrent_deviations_lv, self.id, str(
                                self.data["name"]), str(
                                self.data["location"]), 'LV', 'not_yet', namafile, dt_notif,path))
                        else:
                            self.time_deviasi_lv = dt
                            self.count_object_lv = len(results_lv)
                            val = (None,idImage, "LV",'not_yet', len(results_lv), dt)

                            id_parrent_deviations = self.execute_query(sql_deviation, val)
                            self.id_parrent_deviations_lv = id_parrent_deviations.lastrowid
                            list_of_notification.append(self.send_notif(idImage, self.id_parrent_deviations_lv,None, self.id, str(
                                self.data["name"]), str(
                                self.data["location"]), 'LV', 'not_yet', namafile, dt_notif,path))
                            if (os.environ.get("TELEGRAM_LV") == "True" and self.telegram_on):
                                try:
                                    with open(address_img+namafile, 'rb') as photo:
                                        self.bot.sendPhoto(self.chat_id, photo=photo, caption=self.formatMessageTelebot(self.data["location"], self.data["name"], "LV", len(results_lv), dt_notif))
                                except Exception as e:
                                    print(f"Error: {e}")
                    try:
                        self.connection.commit()
                    except:
                        print("Error commit")

                    if(len(list_of_notification) > 0):
                        # print(list_of_notification)
                        self.socketio.emit('message_from_server', list_of_notification)

                    self.time = dt
        return frame
    
    def send_notif(self,id, deviation_id,parent_id, cctv_id, name, location, deviasi, ctype, image, time, path):
        result = {
            'cctv_id': cctv_id,
            'realtime_images_id': id,
            'id': deviation_id,
            'parent_id': parent_id,
            'image': image,
            'name': name,
            'location': location,
            'type_object': deviasi,
            'type_validation': ctype,
            'created_at': time,
            'updated_at': time,
            'path': path
        }
        return result
    
    def formatMessageTelebot(self, cctvname, site, typedeviation, count, timestamp):
        msg =   f"""Mining Eyes Analytics Notification!!!!
CCTV name          : {cctvname}
Site Location        : {site}
Type Deviation    : {typedeviation}
Count Deviation  : {count}
Timestamp           : {timestamp}
"""
        return msg