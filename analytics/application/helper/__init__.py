import os
if 'CONFIG_PATH' in os.environ:
    AREAPRODUKSI_CONFIG = os.environ.get('CONFIG_PATH')
else:
    AREAPRODUKSI_CONFIG = './application/model_ml/model_area_produksi/4.7/yolov4_AllSite.cfg'
if 'WEIGHTS_PATH' in os.environ:
    AREAPRODUKSI_WEIGHTS = os.environ.get('WEIGHTS_PATH')
else:
    AREAPRODUKSI_WEIGHTS = './application/model_ml/model_area_produksi/4.7/yolov4_AllSite_last.weights'
if 'LABELS_PATH' in os.environ:
    AREAPRODUKSI_DATASET = os.environ.get('LABELS_PATH')
else:
    AREAPRODUKSI_DATASET = './application/model_ml/model_area_produksi/4.7/obj_AllSite.names'

YOLOV8_WEIGHTS = './application/model_ml/model_yolov8/yolov8l.pt'
CUSTOM_TRACK = './application/model_ml/model_yolov8/custom_track.yaml'