import unittest
import unittest.mock
from main_server import compute_unique_id, send_bson_obj, id_generator

class TestMainServerFunctions(unittest.TestCase):

    def test_send_bson_obj_empty_payload(self):
        job_empty_payload = {"ID": "ObjectID", "NumberOfDocuments": 1, "Documents": [{"ID": "ObjectID", "DocumentId": "ObjectID", "DocumentType": "String", "FileName": "String", "Payload": ""}]}
        with unittest.mock.patch('socket.socket') as mock_socket_empty_payload:
            instance_empty_payload = mock_socket_empty_payload.return_value
            send_bson_obj(job_empty_payload)
            instance_empty_payload.connect.assert_called_once_with(('localhost', 12345))
            instance_empty_payload.sendall.assert_called_once()

    def test_send_bson_obj_large_payload(self):
        large_payload = "X" * (1024 * 1024)  # 1 MB payload
        job_large_payload = {"ID": "ObjectID", "NumberOfDocuments": 1, "Documents": [{"ID": "ObjectID", "DocumentId": "ObjectID", "DocumentType": "String", "FileName": "String", "Payload": large_payload}]}
        with unittest.mock.patch('socket.socket') as mock_socket_large_payload:
            instance_large_payload = mock_socket_large_payload.return_value
            send_bson_obj(job_large_payload)
            instance_large_payload.connect.assert_called_once_with(('localhost', 12345))
            instance_large_payload.sendall.assert_called_once()
    
    def test_compute_unique_id(self):
        # Test the compute_unique_id function
        data_object = {"ID": "ObjectID", "DocumentId": "ObjectID", "DocumentType": "String", "FileName": "String", "Payload": "Binary"}
        result = compute_unique_id(data_object)
        self.assertIsNotNone(result)

    def test_id_generator(self):
        # Test the id_generator function
        job = {"ID": "ObjectID", "NumberOfDocuments": 1, "Documents": [{"ID": "ObjectID", "DocumentId": "ObjectID", "DocumentType": "String", "FileName": "String", "Payload": ""}]}
        result = id_generator(job)
        self.assertIsNotNone(result)

    def test_send_bson_obj_with_audio(self):
        # Test the send_bson_obj function with audio data
        job = {"ID": "ObjectID", "NumberOfAudio": 1, "Audio": [{"ID": "ObjectID", "AudioId": "ObjectID", "FileType": "Audio", "FileName": "String", "Payload": "AudioData"}]}
        with unittest.mock.patch('socket.socket') as mock_socket:
            instance = mock_socket.return_value
            send_bson_obj(job)
            instance.connect.assert_called_once_with(('localhost', 12345))
            instance.sendall.assert_called_once()

    def test_send_bson_obj_with_video(self):
        # Test the send_bson_obj function with video data
        job = {"ID": "ObjectID", "NumberOfVideos": 1, "Videos": [{"ID": "ObjectID", "VideoId": "ObjectID", "FileType": "Video", "FileName": "String", "Payload": "VideoData"}]}
        with unittest.mock.patch('socket.socket') as mock_socket:
            instance = mock_socket.return_value
            send_bson_obj(job)
            instance.connect.assert_called_once_with(('localhost', 12345))
            instance.sendall.assert_called_once()

    def test_send_bson_obj_with_image(self):
        # Test the send_bson_obj function with image data
        job = {"ID": "ObjectID", "NumberOfImages": 1, "Images": [{"ID": "ObjectID", "ImageId": "ObjectID", "FileType": "Image", "FileName": "String", "Payload": "ImageData"}]}
        with unittest.mock.patch('socket.socket') as mock_socket:
            instance = mock_socket.return_value
            send_bson_obj(job)
            instance.connect.assert_called_once_with(('localhost', 12345))
            instance.sendall.assert_called_once()

if __name__ == '__main__':
    unittest.main()