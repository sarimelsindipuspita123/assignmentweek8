import os
from datetime import datetime
import random

from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()


MONGODB_CLIENT=str(os.getenv("MONGODB_CLIENT"))
DEVICE_LABEL = os.getenv('DEVICE_LABEL')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

VARIABLE_LABEL_1 = os.getenv('VARIABLE_LABEL_1')

def getTime():
    '''
    Get date and time
    :return: {date: x, clock: x}
    '''
    now= datetime.now()
    jam = now.strftime("%H:%M:%S")
    tanggal = now.strftime(f'%B %d, %Y')

    dataTime = {
                'date'  : tanggal,
                'time'  : jam
    }
    
    return dataTime

def getLocation():

    """
    :return: dict, latitude, longitude
    """
    import geocoder
    try:
        g = geocoder.ip('me')
        my_string=g.latlng
        longitude=my_string[0]
        latitude=my_string[1]

        location = {"latitude" : latitude, "longitude" : longitude}
   
        return location
    except:
        print('Error make sure you have Geo-Coder Installed ')

def buildLocation(lat, lng):
    '''
    Make dictionary from lat, long
    '''
    loc = {
        'latitude'  : lat,
        'longitude' : lng
    }

    return loc

def initializeDatabase():
    client = MongoClient(MONGODB_CLIENT)
    db = client[DATABASE_NAME]
    my_collections = db[COLLECTION_NAME]

    return my_collections


def randomData():
    '''
    Generate random data for id_transaksi, kecepatan
    '''
    id_transaksi = random.randint(1,100)
    kecepatan = round(random.uniform(40,120),2)

    return id_transaksi, kecepatan


def buildData(id_transaksi, kecepatan, location, timestamp):
    '''
    Accept arguments: id_transaksi, kecepatan, location, timestamp
    '''
    data = {
                'id_transaksi'  : id_transaksi,
                'kecepatan'     : kecepatan,
                'location'      : location,
                'timestamp'     : timestamp
    }
    
    return data

def sendData(data):
    '''
    Insert one data to MongoDB
    '''
    my_collections = initializeDatabase()

    results = my_collections.insert_one(data)

    return results

def getData(criteria={}):
    '''
    Get data from MongoDB with specific criteria
    Accept argument dict {'key': 'value'}
    '''
    my_collections = initializeDatabase()

    result =  my_collections.find_one(criteria,{
        'id_transaksi': 1, 'kecepatan': 1,'location': 1, 'timestamp': 1})

    return result

def getLatestData():
    '''
    Get latest data from MongoDB
    Use for function to print all result
    '''
    my_collections = initializeDatabase()

    result = my_collections.find().sort('id_transaksi', -1).limit(1)

    try:
        a = result[0]

    except IndexError:
        return None

    return result[0]

def updateData(oldData, newData):
    '''
    Accept parameters oldData to update with newData
    '''
    my_collections = initializeDatabase()

    results = my_collections.update_one(oldData, {'$set': newData})

    return results

def deleteData(criteria):
    '''
    Delete data with given criteria
    :accept: dict {'key': 'value'}
    '''
    my_collections = initializeDatabase()

    results = my_collections.delete_one(criteria)

    return results

if __name__ == '__main__':
    dataRandom = randomData()
    id_transaksi = dataRandom[0]
    kecepatan = dataRandom[1]

    location = getLocation()

    timestamp = getTime()

    data = buildData(id_transaksi, kecepatan, location, timestamp)
    try:
        sendData(data)

    except:
        print('[INFO] Error, cannot send data to MongiDB')

    print('[INFO] Data sent!')
    print(f'{data}')