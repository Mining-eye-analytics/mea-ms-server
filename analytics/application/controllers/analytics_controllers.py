from flask import send_from_directory, abort, jsonify, Response
from application import app
import requests
import os
from application.helper.response import response
from application.model.models import TypeAnalytics
from application.helper import analytics, stream_cctv, analytics_yolov8
from application import socketio
from onvif import ONVIFCamera

list_class_cctv_webstreaming = []

def generate_stream_cctvs():
        try:
            url = f"{os.environ.get('API_CCTV')}/server"
            type_analytics = [getattr(TypeAnalytics, attr) for attr in dir(TypeAnalytics) if not callable(getattr(TypeAnalytics, attr)) and not attr.startswith("__")]

            response = requests.get(url, headers={"API-key" : os.environ.get('SECRET_KEY_CCTV')})
            if response.status_code == 200:
                data = response.json()["data"]
                for item in data:
                    if item['type_analytics'] == TypeAnalytics.StreamCctv:
                        globals()["camera_%s" %item["id"]] = stream_cctv.StreamCctv(item, socketio=socketio)
                    elif item['type_analytics'] == TypeAnalytics.AnalyticsThreeClass:
                        globals()["camera_%s" %item["id"]] = analytics.AnalyticsThreeClass(item, socketio=socketio)
                    elif item['type_analytics'] == TypeAnalytics.AnalyticsCountingCrossing:
                        globals()["camera_%s" %item["id"]] = analytics_yolov8.AnalyticsCountingCrossing(item, socketio=socketio)
                    else:
                        globals()["camera_%s" %item["id"]] = stream_cctv.StreamCctv(item, socketio=socketio)
                    list_class_cctv_webstreaming.append({"camera_%s" %item["id"]: globals()["camera_%s" %item["id"]]})
            else:
                print("Cant's load cctvs")
        except:
            print("Error to load cctvs")
generate_stream_cctvs()

def cam_object(id):
    with app.app_context():
        for data in list_class_cctv_webstreaming:
            for key in data:
                if key == f"camera_{id}":
                    cam = data[key]
                    return cam
    return None

def list_type_analytics():
    try:
        # Mengubah atribut kelas menjadi iterable (daftar)
        class_names = [getattr(TypeAnalytics, attr) for attr in dir(TypeAnalytics) if not callable(getattr(TypeAnalytics, attr)) and not attr.startswith("__")]
        data = {"list_analytics" : class_names}
        # # Menggunakan enumerate untuk mengindeks data
        # for index, class_name in enumerate(class_names):
        #     print(f"Index {index}: {class_name}")
        return response(data,message=f"Success get list type of analytics", code=200, status="success")
    except Exception as e:
        print(e)
        return response(None,message=f"Failed get list type of analytics", code=500, status="error")
    
def get_type_analytics(request, id):
    try:
        headers = {"Authorization": request.headers["Authorization"]}
        url = f"{os.environ.get('API_CCTV')}/{id}"
        response_data = requests.get(url, headers=headers).json()["data"]
        if response_data is None:
            return response(None,message=f"CCTV not found", code=400, status="error")
        
        if list_class_cctv_webstreaming:
            cam = cam_object(id)
            if cam:
                print(cam.__class__.__name__)
                data = {"type_analytics" : cam.__class__.__name__}
                return response(data,message=f"Success get type of analytics", code=200, status="success")
            else:
                data = {"type_analytics" : None}
                return response(None,message=f"Success get type of analytics", code=200, status="success")
        else:
            data = {"type_analytics" : None}
            return response(None,message=f"Success get type of analytics", code=200, status="success")
    except Exception as e:
        print(e)
        return response(None,message=f"Failed get type of analytics", code=500, status="error")

def set_type_analytics(request, id):
    input_data = request.get_json(force=True)

    try:
        headers = {"Authorization": request.headers["Authorization"]}
        type_analytics = input_data['type_analytics']
        url = f"{os.environ.get('API_CCTV')}/{id}"
        response_data = requests.get(url, headers=headers).json()["data"]
        if response_data is None:
            data = None
            return response(data,message=f"CCTV not found", code=400, status="error")
        
        if list_class_cctv_webstreaming:
            cam = cam_object(id)
            if cam:
                if type_analytics == "AnalyticsThreeClass":
                    cam.exit_object()
                    for item in list_class_cctv_webstreaming:
                        if f"camera_{id}" in item:
                            del item[f"camera_{id}"]
                    del cam
                    temp = list(filter(None, list_class_cctv_webstreaming))
                    list_class_cctv_webstreaming.clear()
                    list_class_cctv_webstreaming.extend(temp)
                    globals()[f"camera_{id}"] = analytics.AnalyticsThreeClass(response_data[0], socketio=socketio)
                    cam = globals()[f"camera_{id}"]
                    list_class_cctv_webstreaming.append({f"camera_{id}" : globals()[f"camera_{id}"]})
                    data = {"type_analytics" : "AnalyticsThreeClass"}
                    response_value = {"data": data, "message": f"Success set type of analytics", "code": 200, "status": "success"}
                    
                elif type_analytics == "AnalyticsCountingCrossing":
                    cam.exit_object()
                    for item in list_class_cctv_webstreaming:
                        if f"camera_{id}" in item:
                            del item[f"camera_{id}"]
                    del cam
                    temp = list(filter(None, list_class_cctv_webstreaming))
                    list_class_cctv_webstreaming.clear()
                    list_class_cctv_webstreaming.extend(temp)
                    globals()[f"camera_{id}"] = analytics_yolov8.AnalyticsCountingCrossing(response_data[0], socketio=socketio)
                    cam = globals()[f"camera_{id}"]
                    list_class_cctv_webstreaming.append({f"camera_{id}" : globals()[f"camera_{id}"]})
                    data = {"type_analytics" : "AnalyticsCountingCrossing"}
                    response_value = {"data": data, "message": f"Success set type of analytics", "code": 200, "status": "success"}

                    
                elif type_analytics == "StreamCctv":
                    cam.exit_object()
                    for item in list_class_cctv_webstreaming:
                        if f"camera_{id}" in item:
                            del item[f"camera_{id}"]
                    del cam
                    temp = list(filter(None, list_class_cctv_webstreaming))
                    list_class_cctv_webstreaming.clear()
                    list_class_cctv_webstreaming.extend(temp)
                    globals()[f"camera_{id}"] = stream_cctv.StreamCctv(response_data[0])
                    cam = globals()[f"camera_{id}"]
                    list_class_cctv_webstreaming.append({f"camera_{id}" : globals()[f"camera_{id}"]})
                    data = {"type_analytics" : "StreamCctv"}
                    response_value = {"data": data, "message": f"Success set type of analytics", "code": 200, "status": "success"}
                    
                else:
                    data = None
                    response_value = {"data": data, "message": f"Failed set type of analytics", "code": 400, "status": "error"}
                    
            else:
                if type_analytics == "AnalyticsThreeClass":
                    globals()[f"camera_{id}"] = analytics.AnalyticsThreeClass(response_data[0], socketio=socketio)
                    cam = globals()[f"camera_{id}"]
                    list_class_cctv_webstreaming.append({f"camera_{id}" : globals()[f"camera_{id}"]})
                    data = {"type_analytics" : "AnalyticsThreeClass"}
                    response_value = {"data": data, "message": f"Success set type of analytics", "code": 200, "status": "success"}
                    
                elif type_analytics == "AnalyticsCountingCrossing":
                    globals()[f"camera_{id}"] = analytics_yolov8.AnalyticsCountingCrossing(response_data[0], socketio=socketio)
                    cam = globals()[f"camera_{id}"]
                    list_class_cctv_webstreaming.append({f"camera_{id}" : globals()[f"camera_{id}"]})
                    data = {"type_analytics" : "AnalyticsCountingCrossing"}
                    response_value = {"data": data, "message": f"Success set type of analytics", "code": 200, "status": "success"}
                    
                elif type_analytics == "StreamCctv":
                    globals()[f"camera_{id}"] = stream_cctv.StreamCctv(response_data[0])
                    cam = globals()[f"camera_{id}"]
                    list_class_cctv_webstreaming.append({f"camera_{id}" : globals()[f"camera_{id}"]})
                    data = {"type_analytics" : "StreamCctv"}
                    response_value = {"data": data, "message": f"Success set type of analytics", "code": 200, "status": "success"}
                    
                else:
                    data = None
                    response_value = {"data": data, "message": f"Failed set type of analytics", "code": 400, "status": "error"}
                    
        else:
            if type_analytics == "AnalyticsThreeClass":
                globals()[f"camera_{id}"] = analytics.AnalyticsThreeClass(response_data[0], socketio=socketio)
                cam = globals()[f"camera_{id}"]
                list_class_cctv_webstreaming.append({f"camera_{id}" : globals()[f"camera_{id}"]})
                data = {"type_analytics" : "AnalyticsThreeClass"}
                response_value = {"data": data, "message": f"Success set type of analytics", "code": 200, "status": "success"}
                
            elif type_analytics == "AnalyticsCountingCrossing":
                globals()[f"camera_{id}"] = analytics_yolov8.AnalyticsCountingCrossing(response_data[0], socketio=socketio)
                cam = globals()[f"camera_{id}"]
                list_class_cctv_webstreaming.append({f"camera_{id}" : globals()[f"camera_{id}"]})
                data = {"type_analytics" : "AnalyticsCountingCrossing"}
                response_value = {"data": data, "message": f"Success set type of analytics", "code": 200, "status": "success"}
                
            elif type_analytics == "StreamCctv":
                globals()[f"camera_{id}"] = stream_cctv.StreamCctv(response_data[0])
                cam = globals()[f"camera_{id}"]
                list_class_cctv_webstreaming.append({f"camera_{id}" : globals()[f"camera_{id}"]})
                data = {"type_analytics" : "StreamCctv"}
                response_value = {"data": data, "message": f"Success set type of analytics", "code": 200, "status": "success"}
                
            else:
                data = None
                response_value = {"data": data, "message": f"Failed set type of analytics", "code": 400, "status": "error"}
        # Menggunakan metode PUT untuk mengirim data
        if data is not None:
            update_cctv = requests.put(url, headers=headers, data=data)
        return response(**response_value)
    except Exception as e:
        print(e)
        return response(None,message=f"Failed add/set type of analytics", code=500, status="error")
    
def gen_video_feed(id):
    # header = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55IjoiQkMiLCJpZCI6MywiZnVsbF9uYW1lIjoiRGV2ZWxvcGVyIE1pbmluZyBFeWVzIEFuYWx5dGljcyIsInJvbGUiOiJzdXBlcl9hZG1pbiIsInVzZXJuYW1lIjoiZGV2ZWxvcGVyIiwiY3JlYXRlZF9hdCI6IjIwMjMtMDktMDcgMDM6MjI6MTguMDI5OTEzIiwidXBkYXRlZF9hdCI6Ik5vbmUifQ.gulJ2_SyZt6UWpXZVSGSyOtyhvKqpCaOj1dsFXGpXXo"
    # # if "Authorization" in request.headers: headers = { "Authorization": f"{headers}" }
    try:
        url = f"{os.environ.get('API_CCTV')}/server/{id}"
        response_data = requests.get(url, headers={"API-key" : os.environ.get('SECRET_KEY_CCTV')}).json()["data"]
        if response_data is None:
            return response(None,message=f"CCTV not found", code=400, status="error")
        data = response_data[0]
        
        if list_class_cctv_webstreaming:
            cam = cam_object(id)
            if cam:
                return Response(cam.generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
            else:
                if data['type_analytics'] == TypeAnalytics.StreamCctv:
                    globals()["camera_%s" %data["id"]] = stream_cctv.StreamCctv(data, socketio=socketio)
                elif data['type_analytics'] == TypeAnalytics.AnalyticsThreeClass:
                    globals()["camera_%s" %data["id"]] = analytics.AnalyticsThreeClass(data, socketio=socketio)
                elif data['type_analytics'] == TypeAnalytics.AnalyticsCountingCrossing:
                    globals()["camera_%s" %data["id"]] = analytics_yolov8.AnalyticsCountingCrossing(data, socketio=socketio)
                else:
                    globals()["camera_%s" %data["id"]] = stream_cctv.StreamCctv(data, socketio=socketio)
                cam = globals()[f"camera_{data['id']}"]
                list_class_cctv_webstreaming.append({f"camera_{data['id']}" : globals()[f"camera_{data['id']}"]})
                return Response(cam.generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
        else:
            if data['type_analytics'] == TypeAnalytics.StreamCctv:
                globals()["camera_%s" %item["id"]] = stream_cctv.StreamCctv(data, socketio=socketio)
            elif data['type_analytics'] == TypeAnalytics.AnalyticsThreeClass:
                globals()["camera_%s" %data["id"]] = analytics.AnalyticsThreeClass(data, socketio=socketio)
            elif data['type_analytics'] == TypeAnalytics.AnalyticsCountingCrossing:
                globals()["camera_%s" %data["id"]] = analytics_yolov8.AnalyticsCountingCrossing(data, socketio=socketio)
            else:
                globals()["camera_%s" %data["id"]] = stream_cctv.StreamCctv(data, socketio=socketio)
            cam = globals()[f"camera_{data['id']}"]
            list_class_cctv_webstreaming.append({f"camera_{data['id']}" : globals()[f"camera_{data['id']}"]})
            return Response(cam.generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        e = str(e)
        return response(None,message=f"Failed to Generate Cam, {e} ", code=500, status="error")
    

    

def static_dir_image_cctv(filename):
    try:
        return send_from_directory("assets",filename)
    except FileNotFoundError:
        abort(404)

def draw_polygon(request, id):
    input_data = request.get_json(force=True)
    
    # tuple_data_list = [tuple(data) for data in polygon]
    try:
        polygon = input_data['polygon']
        outside_secure_area = input_data['outside_secure_area']
        object_perimeter = input_data['object_perimeter']
        cam = cam_object(id)
        cam.polygon = polygon
        cam.outside_secure_area = bool(outside_secure_area)
        cam.object_perimeter = object_perimeter
        return response(None, message="Success draw polygon", code=200, status="success")
    except Exception as e:
        e = str(e)
        return response(None,message=f"Failed draw polygon in {e} ", code=500, status="error")

def get_polygon(id):
    try:
        cam = cam_object(id)
        polygon = cam.polygon
        outside_secure_area = bool(cam.outside_secure_area)
        object_perimeter = cam.object_perimeter
        data = {"polygon": polygon, "outside_secure_area": outside_secure_area, "object_perimeter": object_perimeter}
        return response(data, message="Success get polygon", code=200, status="success")
    except Exception as e:
        print(e)
        return response(None, message="Failed get polygon", code=500, status="error")
    
def set_var_distance_hd(request, id):
    input_data = request.get_json(force=True)
    
    try:
        var_distance_hd = float(input_data['distance_hd'])
        cam = cam_object(id)
        cam.distance_hd = var_distance_hd
        return response(None, message="Success set variable distance hd", code=200, status="success")
    except Exception as e:
        e = str(e)
        return response(None,message=f"Failed to set variable distance hd in {e} ", code=500, status="error")

def get_var_distance_hd(id):
    try:
        cam = cam_object(id)
        distance_hd = cam.distance_hd
        data = {"Distance": distance_hd}
        return response(data, message="Success get variable distance hd", code=200, status="success")
    except Exception as e:
        print(e)
        return response(None, message="Failed get variable distance hd", code=500, status="error")
    
# create service Onvif
def createServiceONVIF(ip,username,password):
    mycam = ONVIFCamera(ip, 80, username, password)

    # Create media service object
    media = mycam.create_media_service()
    # Create ptz service object
    ptz = mycam.create_ptz_service()

    # Get target profile token
    token = media.GetProfiles()[0]._token

    return ptz,token

def absolute_move(x, y, z, ip, username, password):
    ptz, token = createServiceONVIF(ip, username, password)
    request = ptz.create_type('AbsoluteMove')
    request.ProfileToken = token
    # Stops all other movement to get status
    ptz.Stop({'ProfileToken': token})
    status = ptz.GetStatus({'ProfileToken': token})
    if (status.Position.PanTilt._x + x) >= 0.0 and (status.Position.PanTilt._x + x) <= 1.0:
        status.Position.PanTilt._x = status.Position.PanTilt._x + x
    if (status.Position.PanTilt._y + y) <= 1.0 and (status.Position.PanTilt._y + y) >= 0.0:
        status.Position.PanTilt._y = status.Position.PanTilt._y + y
    if (status.Position.Zoom._x+z) <= 1.0 and (status.Position.Zoom._x+z) >= 0.0:
        status.Position.Zoom._x = status.Position.Zoom._x + z
    request.Position = status.Position
    ptz.Stop({'ProfileToken': token})
    ptz.AbsoluteMove(request)
    return 1, request.Position

def control(request, id):
    input_data = request.get_json(force=True)
    
    try:
        x,y,z = 0,0,0
        control = input_data['control']
        cam = cam_object(id)
        headers = {
                "Authorization": request.headers["Authorization"]
            }
        url = f"{os.environ.get('API_CCTV')}/{id}"
        response_data = requests.get(url, headers=headers).json()["data"]
        if response_data is None:
            return response(None,message=f"CCTV not found", code=400, status="error")
        if cam is None:
            return response(None,message=f"can't control, cctv not already initiate", code=400, status="error")
        if control == "reload":
            cam.reload()
            return response(None, message=f"successfully reload cctv object with id {id}", code=200, status="success")
        elif control == "exit":
            cam.exit_object()
            del cam
            for item in list_class_cctv_webstreaming:
                if f"camera_{id}" in item:
                    del item[f"camera_{id}"]
            temp = list(filter(None, list_class_cctv_webstreaming))
            list_class_cctv_webstreaming.clear()
            list_class_cctv_webstreaming.extend(temp)
            return response(None, message=f"successfully exit cctv object with id {id}", code=200, status="success")
        elif control == "move_right":
            x = 0.01
        elif control == "move_left":
            x = -0.01
        elif control == "move_down":
            y = -0.01
        elif control == "move_up":
            y = 0.01
        elif control == "zoom_in":
            z = 0.1
        elif control == "zoom_out":
            z = -0.1
        else:
            return response(None,message=f"Failed control object cctv", code=400, status="error")
        
        ip = response_data[0]['ip']
        username = response_data[0]['username']
        password = response_data[0]['password']
        (success, status) = absolute_move(x, y, z, ip, username, password)
        if success == 1:
            x = status.PanTilt._x
            y = status.PanTilt._y
            z = status.Zoom._x
            coordinat = (x, y, z)
            result = {'status': 'true',
                    'message': 'success move', 'coordinat': coordinat}
        else:
            result = {'status': 'false'}
        return response(result,message=f"Success move ptz cctv object", code=200, status="success")
        
    except Exception as e:
        print(e)
        return response(None,message=f"Failed control object cctv", code=500, status="error")
    

    
