# application/models.py
from application import db
from datetime import datetime
from enum import IntEnum

class TypeAnalytics:
    AnalyticsThreeClass = "AnalyticsThreeClass"
    StreamCctv = "StreamCctv"
    AnalyticsCountingCrossing = "AnalyticsCountingCrossing"
    
class Role(IntEnum):
    SUPER_ADMIN = 3
    ADMIN = 2
    USER = 1