import requests 
import json
from kafka import KafkaProducer
import time
import os

API_ENDPOINT = "https://randomuser.me/api/?results=1"
KAFKA_BOOTSTRAP_SERVERS = ['kafka1:9092']
START_STREAMING = 0
STOP_STREAMING = 200
PAUSE_INTERVAL = 10
KAFKA_TOPIC = 'Dataingestion_topic'

def retrieve_user_data(url=API_ENDPOINT):
    response = requests.get(url)
    return response.json()["results"]
def transform_user_data(response):
    
    for resp in response:
        
        data= {
            
            "name":f"{resp['name']['first']}.{resp['name']['last']}",
            "gender":resp["gender"],
            "address": f"{resp['location']['street']['number']}, {resp['location']['street']['name']}",  
            "city": resp['location']['city'],
            "nation": resp['location']['country'],  
            "zip": resp['location']['postcode'],  
            "latitude": float(resp['location']['coordinates']['latitude']),
            "longitude": float(resp['location']['coordinates']['longitude']),
            "email": resp["email"]
        }
        
        return data

def configure_kafka_server(servers=KAFKA_BOOTSTRAP_SERVERS):
    
    producer= KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,value_serializer= lambda x: json.dumps(x).encode('utf8'))
    return producer

def publish_to_kafka(producer,topic,data):
    producer.send(topic,value=data)
    

def delivery_status(err,msg):
    
    if err is not None:
        print("Message Delivery Failed: ",err)
    else:
        print("Message Delivered Successfull to: {0} Partition:{1} ".format(msg.topic(),msg.partition()))           

def initiate_stream():
    
    kafka_producer= configure_kafka_server()
    for _ in range(START_STREAMING,STOP_STREAMING):
        response=retrieve_user_data(API_ENDPOINT)
        user_data=transform_user_data(response)
        print(user_data)
        print(type(user_data))
        publish_to_kafka(kafka_producer,KAFKA_TOPIC,user_data)
        time.sleep(PAUSE_INTERVAL)
    
    