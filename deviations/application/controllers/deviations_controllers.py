from flask import send_from_directory, abort, jsonify, Response
from application import app, db
import requests
import os
from application.helper.response import response
from application.model.models import Realtime_images, Realtime_deviations, Crossing_counting
from sqlalchemy import func
from collections import defaultdict
    
# get all data from realtime_deviations
def index_rd():
    try:
        deviation = Realtime_deviations.query.all()

        if not deviation:
            return response(None, message='There is no realtime deviation data', code=200, status='success')
        data = [d.to_json() for d in deviation]
        
        return response(data, message="success get all realtime deviation data",code=200, status='success')

    except Exception as e:
        return response(None, message="Failed get all realtime deviation data", code=500, status="error")

# get detail data from realtime_deviations
def detail_rd(id):
    try:
        deviation = Realtime_deviations.query.filter(Realtime_deviations.id==id).first()

        if not deviation:
            return response(None, message='There is no realtime deviation data', code=404, status='error')

        data = deviation.to_json()
        
        return response(data, message="success get realtime deviation data",code=200, status='success')

    except Exception as e:
        return response(None, message="Failed get realtime deviation data", code=500, status="error")

# get all data from realtime_images
def index_ri():
    try:
        images = Realtime_images.query.all()

        if not images:
            return response(None, message='There is no realtime images data', code=200, status='success')
        data = [d.to_json_all() for d in images]
        
        return response(data, message="success get all realtime images data",code=200, status='success')

    except Exception as e:
        return response(None, message="Failed get all realtime images data", code=500, status="error")

# get detail data from realtime_images
def detail_ri(id):
    try:
        image = Realtime_images.query.filter(Realtime_images.id==id).first()

        if not image:
            return response(None, message='There is no realtime images data', code=404, status='error')

        data = image.to_json_all()
        
        return response(data, message="success get realtime images data",code=200, status='success')

    except Exception as e:
        return response(None, message="Failed get realtime images data", code=500, status="error")
    
# get_type_object
def type_object():
    arr = []
    try:
        deviation = Realtime_deviations.query.with_entities(Realtime_deviations.type_object).distinct()

        for data in deviation:
            arr.append(data.type_object)

        if not deviation:
            return response(None, message='There is no type object', code=200, status='success')
        
        return response(arr, message="success get all type object",code=200, status='success')

    except Exception as e:
        return response(None, message="Failed get all type objec", code=500, status="error")

# update data from realtime_deviations
def update_rd(request, id):
    try:
        type_validation = request.form.get('type_validation')
        comment = request.form.get('comment')
        user_id = request.form.get('user_id')
        input = [
            {
                'type_validation' : type_validation, 
                'comment' : comment,
                'user_id' : user_id
            }
        ]

        deviation = Realtime_deviations.query.filter(Realtime_deviations.id==id).first()
        if type_validation is not None: deviation.type_validation = type_validation
        if comment is not None: deviation.comment = comment
        if user_id is not None: deviation.user_id = user_id

        db.session.commit()

        return response(input, message="success update deviation",code=200, status='success')

    except Exception as e:
        return response(input, message="failed update deviation",code=500, status='error')


def get_deviations(request):
    try:
        cctv_id = request.args.get('cctv_id')
        filter_notification = request.args.get('filter_notification')
        type_object = request.args.get('type_object')
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')
        limit = request.args.get('limit')


        data = db.session.query(Realtime_images, Realtime_deviations).join(Realtime_deviations, Realtime_images.id==Realtime_deviations.realtime_images_id).filter(Realtime_images.id > 0)

        if cctv_id:
            data = data.filter(Realtime_images.cctv_id == cctv_id)
            
        if filter_notification:
            if filter_notification =="ALLvalidation":
                data = data
            elif filter_notification == "Tervalidasi" or  filter_notification == "Perlu Validasi":
                if filter_notification == 'Perlu Validasi':
                    data = data.filter(Realtime_deviations.type_validation == 'not_yet')
                elif filter_notification == "Tervalidasi": 
                    data = data.filter(Realtime_deviations.type_validation != 'not_yet')
            else:
                data = data.filter(Realtime_deviations.type_validation == filter_notification)

        if type_object:
                data = data.filter(Realtime_deviations.type_object == type_object)
        if startDate or endDate:
            if startDate != "" and endDate != "":
                data = data.filter(Realtime_deviations.created_at.between(startDate, endDate))
            elif startDate == "" and endDate != "":
                data = data.filter(Realtime_deviations.created_at < endDate)
            elif endDate == "" and startDate !="":
                data = data.filter(Realtime_deviations.created_at > startDate)

        if limit:
            data = data.order_by(Realtime_deviations.created_at.desc()).limit(limit)
        else:
            data = data.order_by(Realtime_deviations.created_at.desc())
        
        data = data.all()

        if not data:
            return response(None, message="Tidak terdapat deviasi yang dicari", code=200, status="success")
        deviations = []
        for item in data:
            json_deviation = [f.to_json() for f in item]
            merged_deviations = {key: value for d in json_deviation for key, value in d.items()}
            deviations.append(merged_deviations)
        return response(deviations, message="Success get deviations", code=200, status="success")
    except Exception as e:
        return response(None, message="Failed get deviations", code=500, status="error")
    
def get_deviations_with_child(request):
    try:
        cctv_id = request.args.get('cctv_id')
        filter_notification = request.args.get('filter_notification')
        type_object = request.args.get('type_object')
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')
        limit = request.args.get('limit')


        data = db.session.query(Realtime_images, Realtime_deviations).join(Realtime_deviations, Realtime_images.id==Realtime_deviations.realtime_images_id).filter(Realtime_images.id > 0)

        if cctv_id:
            data = data.filter(Realtime_images.cctv_id == cctv_id)
            
        if filter_notification:
            if filter_notification =="ALLvalidation":
                data = data
            elif filter_notification == "Tervalidasi" or  filter_notification == "Perlu Validasi":
                if filter_notification == 'Perlu Validasi':
                    data = data.filter(Realtime_deviations.type_validation == 'not_yet')
                elif filter_notification == "Tervalidasi": 
                    data = data.filter(Realtime_deviations.type_validation != 'not_yet')
            else:
                data = data.filter(Realtime_deviations.type_validation == filter_notification)

        if type_object:
                data = data.filter(Realtime_deviations.type_object == type_object)
        if startDate or endDate:
            if startDate != "" and endDate != "":
                data = data.filter(Realtime_deviations.created_at.between(startDate, endDate))
            elif startDate == "" and endDate != "":
                data = data.filter(Realtime_deviations.created_at < endDate)
            elif endDate == "" and startDate !="":
                data = data.filter(Realtime_deviations.created_at > startDate)

        parent_query = data.filter(Realtime_deviations.parent_id == None)
        if limit:
            parent_query = parent_query.order_by(Realtime_deviations.created_at.desc()).limit(limit)
        else:
            parent_query = parent_query.order_by(Realtime_deviations.created_at.desc())
        
        parent = parent_query.all()

        if not parent:
            return response(None, message="Tidak terdapat deviasi yang dicari", code=200, status="success")
        deviations = []
        for item in parent:
            json_deviation = [f.to_json() for f in item]
            merged_deviations = {key: value for d in json_deviation for key, value in d.items()}
            deviations.append(merged_deviations)

        child_query = data.filter(Realtime_deviations.parent_id != None)
        child_query = child_query.filter(Realtime_deviations.id > deviations[-1]["id"])
        child_query = child_query.order_by(Realtime_deviations.created_at.asc())
        child = child_query.all()

        if not child:
            return response(deviations, message="Success get detail of view", code=200, status="success")
        
        child_data = []
        for item in child:
            json_deviation = [f.to_json() for f in item]
            merged_child = {key: value for d in json_deviation for key, value in d.items()}
            child_data.append(merged_child)

        id_to_child = {}
        for child in child_data:
            parent_id = child['parent_id']
            if parent_id not in id_to_child:
                id_to_child[parent_id] = []
            id_to_child[parent_id].append(child)
        for item in deviations:
            item['children'] = id_to_child.get(item['id'], [])
        return response(deviations, message="Success get deviations with child", code=200, status="success")
    except Exception as e:
        return response(None, message="Failed get deviations with child", code=500, status="error")

def get_crossing_counting(request):
    try:
        cctv_id = request.args.get('cctv_id')
        type_object = request.args.get('type_object')
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')
        limit = request.args.get('limit')


        data = db.session.query(Realtime_images, Crossing_counting).join(Crossing_counting, Realtime_images.id==Crossing_counting.realtime_images_id).filter(Realtime_images.id > 0)

        if cctv_id:
            data = data.filter(Realtime_images.cctv_id == cctv_id)

        if type_object:
                data = data.filter(Crossing_counting.type_object == type_object)
        if startDate or endDate:
            if startDate != "" and endDate != "":
                data = data.filter(Crossing_counting.created_at.between(startDate, endDate))
            elif startDate == "" and endDate != "":
                data = data.filter(Crossing_counting.created_at < endDate)
            elif endDate == "" and startDate !="":
                data = data.filter(Crossing_counting.created_at > startDate)

        if limit:
            data = data.order_by(Crossing_counting.created_at.desc()).limit(limit)
        else:
            data = data.order_by(Crossing_counting.created_at.desc())
        
        data = data.all()

        if not data:
            return response(None, message="Tidak terdapat data yang dicari", code=200, status="success")
        datas = []
        for item in data:
            json_deviation = [f.to_json() for f in item]
            merged_datas = {key: value for d in json_deviation for key, value in d.items()}
            datas.append(merged_datas)
        return response(datas, message="Success get data", code=200, status="success")
    except Exception as e:
        return response(None, message="Failed get data", code=500, status="error")

def get_count_crossing_counting(request):
    try:
        cctv_id = request.args.get('cctv_id')
        date = request.args.get('date')

        data = db.session.query(Crossing_counting.type_object, 
                                Crossing_counting.direction, 
                                func.count().label('total_count')) \
                .filter(Crossing_counting.direction.in_(['in', 'out'])) \
                .join(Realtime_images, Realtime_images.id==Crossing_counting.realtime_images_id)
        
        if cctv_id:
            data = data.filter(Realtime_images.cctv_id == cctv_id)
        if date:
            data = data.filter(Crossing_counting.created_at.between(f"{date} 00:00:00", f"{date} 23:59:59")) \

        data = data.group_by(Crossing_counting.type_object, Crossing_counting.direction).all()

        if not data:
            return response(None, message="Tidak terdapat data yang dicari", code=200, status="success")

        # Membuat dictionary sementara
        temp_dict = {}
        result = []

        for item in data:
            obj, direction, count = item
            if obj not in temp_dict:
                temp_dict[obj] = {'object': obj, 'count': {'in': 0, 'out': 0}}
            
            temp_dict[obj]['count'][direction] = count

        # Menyusun ulang data
        for obj in temp_dict:
            result.append(temp_dict[obj])
        return response(result, message="Success get data", code=200, status="success")
    except Exception as e:
        return response(None, message="Failed get data", code=500, status="error")
    
def get_count_cctv(request):
    try:
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')
        query = db.session.query(
                    func.SUBSTRING_INDEX(Realtime_images.created_at, ' ', 1).label('tanggal'),
                    func.count().label('jumlah_notifikasi'),
                    Realtime_images.cctv_id.label('cctv_id')
                ).select_from(Realtime_deviations).join(Realtime_images, Realtime_deviations.realtime_images_id == Realtime_images.id) \
                .filter(Realtime_deviations.parent_id.is_(None)) \
                .filter(Realtime_images.created_at.between(startDate, endDate)) \
                .group_by('tanggal', 'cctv_id')
        data = query.all()
        if not data:
            return response(None, message='Tidak ada data pada tanggal tersebut', code=200, status='success')

        formatted_data = defaultdict(list)
        
        try:
            headers = {
                    "Authorization": request.headers["Authorization"]
                }
            for item in data:
                formatted_data[item.tanggal].append({"id": item.cctv_id,"camera": requests.get(f'{os.environ.get("API_CCTV")}/{item.cctv_id}', headers=headers).json()["data"][0]['location'], "jumlah": item.jumlah_notifikasi})
        except:
            for item in data:
                formatted_data[item.tanggal].append({"id": item.cctv_id, "camera": None, "jumlah": item.jumlah_notifikasi})

        result = [{"tanggal": tanggal, "data": data} for tanggal, data in formatted_data.items()]

        return response(result, message="Success get count notif", code=200, status="success")
    except Exception as e:
        print(e)
        return response(None, message="Failed get count notif",code=500, status='error')

def get_count_object(request):
    try:
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')

        query = db.session.query(
            func.SUBSTRING_INDEX(Realtime_images.created_at, ' ', 1).label('tanggal'),
            func.count().label('jumlah_notifikasi'),
            Realtime_deviations.type_object.label('objek')
        ).select_from(Realtime_deviations).join(Realtime_images, Realtime_deviations.realtime_images_id == Realtime_images.id)\
        .filter(Realtime_deviations.parent_id.is_(None))\
        .filter(Realtime_images.created_at.between(startDate, endDate)) \
        .group_by('tanggal', 'objek')
        
        data = query.all()

        if not data:
            return response(None, message='Tidak ada data pada tanggal tersebut', code=200, status='success')

        formatted_data = defaultdict(list)
        for item in data:
            formatted_data[item.tanggal].append({"objek": item.objek, "jumlah": item.jumlah_notifikasi})

        result = [{"tanggal": tanggal, "data": data} for tanggal, data in formatted_data.items()]

        return response(result, message="Success get count object", code=200, status="success")
    except Exception as e:
        print(e)
        return response(None, message="Failed get count object",code=500, status='error')