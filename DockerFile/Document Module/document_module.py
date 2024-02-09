import spacy
import pdfplumber
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import os
import io 
from PIL import Image
import fitz
import pika
import bson

FilePath = os.path.dirname(__file__)

def openFile(the_file):
    # Pass file to Meta and Convert file to Text
    Meta_file = Meta(the_file)
    Text_Summerizer, Keyword = ConvertFile_txt(the_file)
    return Meta_file, Text_Summerizer, Keyword

def Meta(the_file):
    with pdfplumber.open(the_file) as pdf:
        with open(FilePath + "/" + 'Meta.txt', 'w') as f:
            print(pdf.metadata, file=f)
            print(pdf.pages, file=f)
    
    # Open Meta.txt as binary
    with open(FilePath + "/" + 'Meta.txt', 'rb') as f:
        return f

def ConvertFile_txt(the_file):
    text_pdf = ''
    with pdfplumber.open(the_file) as pdf:
        for page in pdf.pages:
            text_pdf += page.extract_text()
    Summerizer_file = Text_Summerizer(text_pdf)
    Keyword_file = KeyWord(text_pdf)
    return Summerizer_file, Keyword_file

def Text_Summerizer(text_pdf):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text_pdf)
    tokens = [token.text for token in doc]
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens)*1)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ''.join(final_summary)
    with open(FilePath + "/" + "summary.txt", 'w') as f:
        print(summary, file=f)
    # Open summary.txt as binary
    with open(FilePath + "/" + 'summary.txt', 'rb') as f:
        return f

def KeyWord(text_pdf):
    nlp = spacy.load('en_core_web_sm')
    pos_tag = ['PROPN', 'ADJ', 'NOUN']  # 1
    doc = nlp(text_pdf.lower())  # 2
    result = []
    for token in doc:
       # 3
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
    # 4
        if (token.pos_ in pos_tag):
            result.append(token.text)
    with open(FilePath + "/" + "keywords_from_document.txt", 'w') as f:
        print(result, file=f)
    # Open keywords_from_document.txt as binary
    with open(FilePath + "/" + 'keywords_from_document.txt', 'rb') as f:
        return f

# iterate over PDF pages 
def IteratePDF(pdf_file_path):
    pdf_file = fitz.open(pdf_file_path)
    image_len = 0
    for page_index, page in enumerate(pdf_file):
        image_list = page.get_images() 

        # printing number of images found in this page 
        if image_list: 
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}") 
            image_len += 1
        else: 
            print("[!] No images found on page", page_index) 

        for image_index, img in enumerate(page.get_images(), start=1): 
            # get the XREF of the image 
            xref = img[0] 

            # extract the image bytes 
            base_image = pdf_file.extract_image(xref) 

            image_bytes = base_image["image"] 

            # get the image extension 
            image_ext = base_image["ext"] 

            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))

            # Define the path to the images folder
            image_path = os.path.join(os.path.dirname(__file__), 'images')
            
            # Create the folder if it does not exist
            os.makedirs(image_path, exist_ok=True)
        
            # save it to local disk
            image.save(open(f"{image_path}/image{page_index+1}_{image_index}.{image_ext}", "wb"))
    #return amount of images
    return image_len


def remove_files():
    os.remove(FilePath + "/" + 'Meta.txt')
    os.remove(FilePath + "/" + 'summary.txt')
    os.remove(FilePath + "/" + 'keywords_from_document.txt')
    #remove the entire image folder
    for file in os.listdir(FilePath+"/images"):
        os.remove(FilePath + "/images/" + file)
    
# Function to publish messages to RabbitMQ
def publish_to_rabbitmq(routing_key, message):
    # Establish a connection to the RabbitMQ server
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)

    # Create a channel for communication with RabbitMQ
    channel = connection.channel()
  
    # Serialize the message to BSON
    message = bson.dumps(message)
    
    # Publish the message to the specified routing key
    channel.basic_publish(
        exchange="Topic",
        routing_key=routing_key,
        body=message
    )

    print(f'Message "{message}" sent on routing key "{routing_key}"')

    # Close the connection to RabbitMQ
    connection.close()

def consumer_connection(routing_key):
    # Establish a connection to RabbitMQ server
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)

    # Create a channel
    channel = connection.channel()

    # Declare a queue (queue names are generated based on the routing key)
    queue_name = routing_key

    # Consume messages from the queue
    a=channel.basic_consume(queue=queue_name, auto_ack=True,
        on_message_callback=on_message_received)
    
    print('Preprocess Starting Consuming')
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.close()
        connection.close()

def on_message_received(ch, method, properties, body):
    #load the bson object
    body=bson.loads(body)
    '''
    the body is a dictionary with the following structure:
        {
            "ID": "ObjectID",  
            "DocumentId": "ObjectID",
            "DocumentType": "String",
            "FileName": "String",
            "Payload": "Binary"
        }
    '''
    
    #save the payload to a file
    with open(FilePath + "/" + body['FileName'], 'wb') as f:
        f.write(body['Payload'])
    
    #open the file and convert it to text
    Meta_file, Text_Summerizer, Keyword = openFile(FilePath + "/" + body['FileName'])
    Image_file = IteratePDF(FilePath + "/" + body['FileName'])


    if Image_file > 0:
        for file in os.listdir(FilePath+"/images"):
            _, ext = os.path.splitext(file)
            ext = ext.lstrip('.')  # Remove the leading dot from the extension
            with open(FilePath + "/images/" + file, 'rb') as f:
                image_payload = f.read()
                image = {
                    "ID": body['ID'],
                    "PictureID": body['DocumentId'],
                    "PictureType": ext,  # Set the value to the file extension
                    "FileName": file,
                    "Payload": image_payload
                }
                #send the image to the next module
                publish_to_rabbitmq('.Image.', image)
    else:
        print('No images found in the document')
        
     
    with open('Meta.txt', 'rb') as f:
        file = f.read()
        body['Meta'] = file
        f.close()
    with open('summary.txt', 'rb') as f:
        file = f.read()
        body['Summary'] = file
        f.close()
    with open('keywords_from_document.txt', 'rb') as f:
        file = f.read()
        body['Keywords'] = file
        f.close()
    
    #send the document to the next module
    publish_to_rabbitmq('.Store.', body)
    
    #remove the files
    remove_files()
    #remove the file
    os.remove(FilePath + "/" + body['FileName'])

if __name__ == "__main__":
    # Start consuming messages from the queue
    consumer_connection('Document')
    
