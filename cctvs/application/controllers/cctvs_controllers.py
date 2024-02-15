from application import db
from application.model.models import Cctv
from application.helper.response import response, objects_to_dict
import requests
import os

# get all data
def get_cctvs():
    try:
        cctvs = Cctv.query.all()
        data = objects_to_dict(cctvs)
        
        return response(data, message="Success Get All Cctvs", code=200, status="success")

    except Exception as e:
        print(e)
        return response(None, message="Failed to Get CCTV's", code=500, status="error")

def get_cctv(id):
    try:
        cctv = Cctv.query.filter_by(id=id).first()
        if not cctv:
            return response(None, message="Cctv Not Found", code=404, status="error")
        
        data = cctv.to_json()
    
        return response([data], message="Success", code=200, status="success")
    
    except Exception as e:
        print(e)
        return response(None, message="Failed to Get CCTV", code=500, status="error")

# create data
def create_cctv(link_rtsp, name, location, ip, username, password, type_analytics):
    try:
        cctv = Cctv(link_rtsp=link_rtsp, name=name, location=location, ip=ip, username=username, password=password, type_analytics=type_analytics)
        db.session.add(cctv)
        db.session.commit()

        data = cctv.to_json()

        return response([data], message="Success Create Cctv", code=201, status="success")

    except Exception as e:
        print(e)
        return response(None, message="Failed to Create CCTV", code=500, status="error")

# update data
def update_cctv(id, link_rtsp, name, location, ip, username, password, type_analytics):
    try:
        cctv = Cctv.query.filter_by(id=id).first()
        if not cctv:
            return response(None, message="Cctv Not Found", code=404, status="error")

        if link_rtsp is not None: cctv.link_rtsp = link_rtsp
        if name is not None: cctv.name = name
        if location is not None: cctv.location = location
        if ip is not None: cctv.ip = ip
        if username is not None: cctv.username = username
        if password is not None: cctv.password = password
        if type_analytics is not None: cctv.type_analytics = type_analytics

        db.session.commit()

        data = cctv.to_json()

        return response([data], message="Success Update Cctv", code=200, status="success")

    except Exception as e:
        print(e)
        return response(None, message="Failed to Update CCTV", code=500, status="error")

# delete data
def delete_cctv(request, id):
    try:
        try:
            url = f"{os.environ.get('API_ANALYTICS')}/{id}/control"
            headers = {
                "Authorization": request.headers["Authorization"]
            }
            delete_obj = requests.post(url, headers=headers, json={"control" : "exit"}).json()
            print(delete_obj)
        except:
            pass

        cctv = Cctv.query.filter_by(id=id).first()
        if not cctv:
            return response(None, message="Cctv Not Found", code=404, status="error")

        db.session.delete(cctv)
        db.session.commit()

        return response(None, message="Success Delete Cctv", code=200, status="success")

    except Exception as e:
        print(e)
        return response(None, message="Failed to Delete CCTV", code=500, status="error")