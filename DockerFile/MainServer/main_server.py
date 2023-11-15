import socket
import bson
import hashlib
import datetime
import json

def compute_unique_id(data_object):
    # Convert the object to a string
    data_str = json.dumps(data_object, default=object)
    
    # Append the current date and time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    combined_data = data_str + current_time
    
    # Generate SHA-256 hash
    unique_id = hashlib.sha256(combined_data.encode()).hexdigest()
    
    return unique_id

def send_bson_obj(job):   
    serialized_data = bson.dumps(job)  # Serializing the object
    
    print(serialized_data)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12345))  # Connecting to the localhost on port 12345
        s.sendall(serialized_data)
        print('Data sent!')

def id_generator(job):
    job['ID'] = compute_unique_id(job)  # Assigning unique ID as a string
    for document in job['Documents']:
        document['ID'] = job['ID'] # Assigning unique ID as a string
        document['DocumentId'] = compute_unique_id(document)  # Assigning unique ID as a string
    for image in job['Images']:
        image['ID'] = job['ID'] # Assigning unique ID as a string
        image['PictureID'] = compute_unique_id(image) # Assigning unique ID as a string

if __name__ == '__main__':
    job = { 
    "ID": "ObjectID",  
    "NumberOfDocuments": 2,
    "NumberOfImages": 2,
    "Documents": [
        {
            "ID": "ObjectID",  
            "DocumentId": "ObjectID",
            "DocumentType": "String",
            "FileName": "String",
            "Payload": "Binary"
        },
        {
            "ID": "ObjectID",  
            "DocumentId": "ObjectID",
            "DocumentType": "String",
            "FileName": "String",
            "Payload": "Binary2"
        }
        
    ],
    "Images": [
        {
            "ID": "ObjectID", 
            "PictureID": "ObjectID",
            "PictureType": "String",
            "FileName": "String",
            "Payload": "Binary"
        }
       ,
        {
            "ID": "ObjectID", 
            "PictureID": "ObjectID",
            "PictureType": "String",
            "FileName": "String",
            "Payload": "Binary2"
        }
    ],
    "Audio": [],
    "Video": [],
}
    id_generator(job)
    print(job)
    send_bson_obj(job)
    




    
