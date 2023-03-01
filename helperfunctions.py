import os
import gdown
from pymongo import MongoClient
import datetime
import base64
import cv2
from constants import *

def download_weights():
    if not os.path.exists(yolo_pretrained_pth):
        gdown.download('https://drive.google.com/uc?id=1obEbWBSm9bXeg10FriJ7R2cGLRsg-AfP', yolo_pretrained_pth, quiet=False)
    if not os.path.exists(yolo_pretrained_cfg):
        gdown.download('https://drive.google.com/uc?id=19sPzBZjAjuJQ3emRteHybm2SG25w9Wn5', yolo_pretrained_cfg, quiet=False)
    if not os.path.exists(tsstg_pretrained_pth):
        gdown.download('https://drive.google.com/uc?id=1mQQ4JHe58ylKbBqTjuKzpwN2nwKOWJ9u', tsstg_pretrained_pth, quiet=False)
    if not os.path.exists(resnet101_pretrained_pth):
        gdown.download('https://drive.google.com/uc?id=1N2MgE1Esq6CKYA6FyZVKpPwHRyOCrzA0', resnet101_pretrained_pth, quiet=False)
    if not os.path.exists(resnet50_pretrained_pth):
        gdown.download('https://drive.google.com/uc?id=1IPfCDRwCmQDnQy94nT1V-_NVtTEi4VmU', resnet50_pretrained_pth, quiet=False)

def create_db_connection():
    client = MongoClient(mongo_db_connection_string)
    return client

def insert_image_into_mongodb(frame,client):
    # Select the database and collection to use
    db = client["mydatabase"]
    recorded_falls = db["recorded_falls"]
    
    retval, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)
    
    # Insert a new document into the "recorded_falls" collection
    timestamp = datetime.datetime.now()
    recorded_falls.insert_one({
        "image": jpg_as_text,
        "timestamp": timestamp
    })
    