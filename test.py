from datetime import datetime

data = [
    {"id": 7, "created_at": "2023-11-24 09:00:44.896+07", "cctv_id": 1},
    {"id": 3, "created_at": "2023-11-21 09:00:44.896+07", "cctv_id": 1},
    {"id": 6, "created_at": "2023-11-23 09:00:44.896+07", "cctv_id": 4},
    {"id": 1, "created_at": "2023-11-20 09:00:44.896+07", "cctv_id": 2},
    {"id": 2, "created_at": "2023-11-21 09:00:44.896+07", "cctv_id": 1},
    {"id": 5, "created_at": "2023-11-22 09:00:44.896+07", "cctv_id": 2},
    {"id": 4, "created_at": "2023-11-22 09:00:44.896+07", "cctv_id": 3},
]

# Initialize an empty dictionary to store counts of each date
array = []

# Define the date range
start_date = datetime.strptime("2023-11-20", "%Y-%m-%d")
end_date = datetime.strptime("2023-11-23", "%Y-%m-%d")

# Count occurrences of each date within the range
for item in data:
    item_date = datetime.strptime(item["created_at"][:10], "%Y-%m-%d")
    
    if start_date <= item_date <= end_date:
        if not array:
            array.append({"created_at": item_date.strftime("%Y-%m-%d"), "cctv_id": item["cctv_id"], "count": 1})
        else:
            found = False
            for i in range(len(array)):
                if array[i]["created_at"] == item_date.strftime("%Y-%m-%d") and array[i]["cctv_id"] == item["cctv_id"]:
                    array[i]["count"] += 1
                    found = True
                    break
            if not found:
                array.append({"created_at": item_date.strftime("%Y-%m-%d"), "cctv_id": item["cctv_id"], "count": 1})

array.sort(key=lambda x: datetime.strptime(x["created_at"], "%Y-%m-%d"))
print(array)