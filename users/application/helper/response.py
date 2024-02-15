from flask import make_response, jsonify

def response(data, message, code, status):
    meta= {
        "message": message,
        "code": code,
        "status": status
    }
    response = {"meta": meta, "data": data}
    return make_response(jsonify(response), code)

def objects_to_dict(objects):
    data = []
    for row in objects:
        data.append(row.to_json())
    return data