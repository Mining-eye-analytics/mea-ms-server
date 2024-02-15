from flask import send_from_directory, abort, jsonify, Response
from application import app, db
import requests
import os
from application.helper.response import response
from application.model.models import Realtime_images, Realtime_deviations, Crossing_counting
from sqlalchemy import func
from collections import defaultdict
import datetime

def get_notification_profile(request):
    try:
        notification_profile = []

        startDate = datetime.datetime.strptime(request.args.get('startDate') + " 00.00.00", "%Y-%m-%d %H.%M.%S")
        endDate = datetime.datetime.strptime(request.args.get('endDate') + " 23.59.59", "%Y-%m-%d %H.%M.%S")

        data = db.session.query(Realtime_images, Realtime_deviations).join(Realtime_deviations, Realtime_images.id==Realtime_deviations.realtime_images_id).filter(Realtime_deviations.created_at.between(startDate, endDate))
        data = data.all()

        deviations = []
        for item in data:
            json_deviation = [f.to_json() for f in item]
            merged_deviations = {key: value for d in json_deviation for key, value in d.items()}
            deviations.append(merged_deviations)

        for item in deviations:
            if startDate <= item["created_at"] <= endDate:
                if not notification_profile:
                    notification_profile.append({"date": item["created_at"].strftime("%Y-%m-%d"), "cctv_id": item["cctv_id"], "count": 1})
                else:
                    found = False
                    for i in range(len(notification_profile)):
                        if notification_profile[i]["date"] == item["created_at"].strftime("%Y-%m-%d") and notification_profile[i]["cctv_id"] == item["cctv_id"]:
                            notification_profile[i]["count"] += 1
                            found = True
                            break
                    if not found:
                        notification_profile.append({"date": item["created_at"].strftime("%Y-%m-%d"), "cctv_id": item["cctv_id"], "count": 1})

        notification_profile.sort(key=lambda x: datetime.datetime.strptime(x["date"], "%Y-%m-%d"))

        if not notification_profile:
            return response(None, message="Tidak terdapat profile notifikasi yang dicari", code=200, status="success")
        return response(notification_profile, message="Success get notification profile", code=200, status="success")
    except Exception as e:
        return response(None, message="Failed get notification profile", code=500, status="error")
    
def get_validation_profile(request):
    try:
        validation_profile = []

        startDate = datetime.datetime.strptime(request.args.get('startDate') + " 00.00.00", "%Y-%m-%d %H.%M.%S")
        endDate = datetime.datetime.strptime(request.args.get('endDate') + " 23.59.59", "%Y-%m-%d %H.%M.%S")

        data = db.session.query(Realtime_images, Realtime_deviations).join(Realtime_deviations, Realtime_images.id==Realtime_deviations.realtime_images_id).filter(Realtime_deviations.created_at.between(startDate, endDate))
        data = data.filter(Realtime_deviations.type_validation != "not_yet")
        data = data.all()

        deviations = []
        for item in data:
            json_deviation = [f.to_json() for f in item]
            merged_deviations = {key: value for d in json_deviation for key, value in d.items()}
            deviations.append(merged_deviations)

        for item in deviations:
            if startDate <= item["created_at"] <= endDate:
                if not validation_profile:
                    if(item["type_validation"] == "true"):
                        validation_profile.append({"date": item["created_at"].strftime("%Y-%m-%d"), "cctv_id": item["cctv_id"], "true_count": 1, "false_count": 0})
                    else:
                        validation_profile.append({"date": item["created_at"].strftime("%Y-%m-%d"), "cctv_id": item["cctv_id"], "true_count": 0, "false_count": 1})
                else:
                    found = False
                    for i in range(len(validation_profile)):
                        if validation_profile[i]["date"] == item["created_at"].strftime("%Y-%m-%d") and validation_profile[i]["cctv_id"] == item["cctv_id"] and item["type_validation"] == "true":
                            validation_profile[i]["true_count"] += 1
                            found = True
                            break
                        elif validation_profile[i]["date"] == item["created_at"].strftime("%Y-%m-%d") and validation_profile[i]["cctv_id"] == item["cctv_id"] and item["type_validation"] == "false":
                            validation_profile[i]["false_count"] += 1
                            found = True
                            break
                    if not found:
                        if(item["type_validation"] == "true"):
                            validation_profile.append({"date": item["created_at"].strftime("%Y-%m-%d"), "cctv_id": item["cctv_id"], "true_count": 1, "false_count": 0})
                        else:
                            validation_profile.append({"date": item["created_at"].strftime("%Y-%m-%d"), "cctv_id": item["cctv_id"], "true_count": 0, "false_count": 1})

        validation_profile.sort(key=lambda x: datetime.datetime.strptime(x["date"], "%Y-%m-%d"))

        if not validation_profile:
            return response(None, message="Tidak terdapat profile validasi yang dicari", code=200, status="success")
        return response(validation_profile, message="Success get validation profile", code=200, status="success")
    except Exception as e:
        return response(None, message="Failed get validation profile", code=500, status="error")
    
def get_validator_profile(request):
    try:
        validator_profile = []

        startDate = datetime.datetime.strptime(request.args.get('startDate') + " 00.00.00", "%Y-%m-%d %H.%M.%S")
        endDate = datetime.datetime.strptime(request.args.get('endDate') + " 23.59.59", "%Y-%m-%d %H.%M.%S")

        data = db.session.query(Realtime_images, Realtime_deviations).join(Realtime_deviations, Realtime_images.id==Realtime_deviations.realtime_images_id).filter(Realtime_deviations.created_at.between(startDate, endDate))
        data = data.filter(Realtime_deviations.type_validation != "not_yet")
        data = data.filter(Realtime_deviations.user_id != None)
        data = data.all()

        deviations = []
        for item in data:
            json_deviation = [f.to_json() for f in item]
            merged_deviations = {key: value for d in json_deviation for key, value in d.items()}
            deviations.append(merged_deviations)

        for item in deviations:
            if startDate <= item["created_at"] <= endDate:
                if not validator_profile:
                    validator_profile.append({"user_id": item["user_id"], "count": 1})
                else:
                    found = False
                    for i in range(len(validator_profile)):
                        if validator_profile[i]["user_id"] == item["user_id"]:
                            validator_profile[i]["count"] += 1
                            found = True
                            break
                    if not found:
                        validator_profile.append({"user_id": item["user_id"], "count": 1})

        validator_profile.sort(key=lambda x: x["user_id"])

        if not validator_profile:
            return response(None, message="Tidak terdapat profile validator yang dicari", code=200, status="success")
        return response(validator_profile, message="Success get validator profile", code=200, status="success")
    except Exception as e:
        return response(None, message="Failed get validator profile", code=500, status="error")
    
def get_total_average_validation(request):
    try:
        startDate = datetime.datetime.strptime(request.args.get('startDate') + " 23.59.59", "%Y-%m-%d %H.%M.%S")
        endDate = startDate - datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)

        aWeekAgoStartDate = startDate - datetime.timedelta(days=7)
        aWeekAgoEndDate = endDate - datetime.timedelta(days=7)

        this_week_day_average = []
        last_week_day_average = []

        total_average_validation = {
            "this_week": {"date_range": endDate.strftime("%Y-%m-%d") + " - " + startDate.strftime("%Y-%m-%d"), "total": 0},
            "last_week": {"date_range": aWeekAgoEndDate.strftime("%Y-%m-%d") + " - " + aWeekAgoStartDate.strftime("%Y-%m-%d"), "total": 0}
        }

        data = db.session.query(Realtime_images, Realtime_deviations).join(Realtime_deviations, Realtime_images.id==Realtime_deviations.realtime_images_id).filter(Realtime_deviations.created_at.between(endDate, startDate))
        data = data.filter(Realtime_deviations.type_validation != "not_yet")
        data = data.all()

        secondData = db.session.query(Realtime_images, Realtime_deviations).join(Realtime_deviations, Realtime_images.id==Realtime_deviations.realtime_images_id).filter(Realtime_deviations.created_at.between(aWeekAgoEndDate, aWeekAgoStartDate))
        secondData = secondData.filter(Realtime_deviations.type_validation != "not_yet")
        secondData = secondData.all()

        deviations = []
        for item in data:
            json_deviation = [f.to_json() for f in item]
            merged_deviations = {key: value for d in json_deviation for key, value in d.items()}
            deviations.append(merged_deviations)
        for item in secondData:
            json_deviation = [f.to_json() for f in item]
            merged_deviations = {key: value for d in json_deviation for key, value in d.items()}
            deviations.append(merged_deviations)

        for i in range(7):
            count = 0

            for item in deviations:
                if (startDate - datetime.timedelta(days=i)).strftime("%Y-%m-%d") == item["created_at"].strftime("%Y-%m-%d"):
                    count += 1

            this_week_day_average.append(count)

        for i in range(7):
            count = 0

            for item in deviations:
                if (aWeekAgoStartDate - datetime.timedelta(days=i)).strftime("%Y-%m-%d") == item["created_at"].strftime("%Y-%m-%d"):
                    count += 1

            last_week_day_average.append(count)

        print(this_week_day_average, last_week_day_average)

        for item in deviations:
            if endDate <= item["created_at"] <= startDate:                
                total_average_validation["this_week"]["total"] += 1
                    
            elif aWeekAgoEndDate <= item["created_at"] <= aWeekAgoStartDate:
                total_average_validation["last_week"]["total"] += 1

        total_average_validation["this_week"]["day_average"] = (sum(this_week_day_average) / 7)
        total_average_validation["last_week"]["day_average"] = (sum(last_week_day_average) / 7)

        if not total_average_validation:
            return response(None, message="Tidak terdapat total dan rata-rata validasi yang dicari", code=200, status="success")
        return response(total_average_validation, message="Success get total and average validation", code=200, status="success")
    except Exception as e:
        return response(None, message="Failed get total and average validation", code=500, status="error")
    
def get_validation_distribution(request):
    try:
        validation_distribution = []

        startDate = datetime.datetime.strptime(request.args.get('startDate') + " 00.00.00", "%Y-%m-%d %H.%M.%S")
        endDate = datetime.datetime.strptime(request.args.get('endDate') + " 23.59.59", "%Y-%m-%d %H.%M.%S")

        tempDates = []
        tempHours = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]
        validation_count = []

        data = db.session.query(Realtime_images, Realtime_deviations).join(Realtime_deviations, Realtime_images.id==Realtime_deviations.realtime_images_id).filter(Realtime_deviations.created_at.between(startDate, endDate))
        data = data.filter(Realtime_deviations.type_validation != "not_yet")
        data = data.all()

        deviations = []
        for item in data:
            json_deviation = [f.to_json() for f in item]
            merged_deviations = {key: value for d in json_deviation for key, value in d.items()}
            deviations.append(merged_deviations)

        for i in range(((startDate - endDate).days) * -1):
            tempDates.append((startDate + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))

        for date in tempDates:
            dataArr = []

            for hour in tempHours:
                count = 0
                for item in deviations:
                    if date == item["created_at"].strftime("%Y-%m-%d") and int(hour) == int(item["created_at"].strftime("%H")):
                        count += 1
                dataArr.append(count)

            validation_count.append(dataArr)
            
        validation_distribution = {
            "date": tempDates,
            "hours": tempHours,
            "validation_count": validation_count
        }

        if not deviations:
            return response(None, message="Tidak terdapat persebaran validasi yang dicari", code=200, status="success")
        return response(validation_distribution, message="Success get validation distribution", code=200, status="success")
    except Exception as e:
        return response(None, message="Failed get validation distribution", code=500, status="error")