import unittest
import unittest.mock
from main_server import compute_unique_id, send_bson_obj, id_generator

class TestMainServerFunctions(unittest.TestCase):

    def test_compute_unique_id(self):
        # Test for the compute_unique_id function
        data_object = {"key": "value"}
        unique_id = compute_unique_id(data_object)
        self.assertIsNotNone(unique_id)
        self.assertIsInstance(unique_id, str)

    def test_send_bson_obj(self):
        # Test for the send_bson_obj function
        job = {"ID": "ObjectID", "NumberOfDocuments": 1, "Documents": [{"ID": "ObjectID", "DocumentId": "ObjectID", "DocumentType": "String", "FileName": "String", "Payload": "Binary"}]}
        # Mock the socket connection to avoid actual network communication
        with unittest.mock.patch('socket.socket') as mock_socket:
            instance = mock_socket.return_value
            send_bson_obj(job)
            instance.connect.assert_called_once_with(('localhost', 12345))
            instance.sendall.assert_called_once()

    def test_id_generator(self):
        # Test for the id_generator function with documents, images, audio, and video
        job = {
            "ID": "ObjectID",
            "NumberOfDocuments": 1,
            "Documents": [
                {"ID": "ObjectID", "DocumentId": "ObjectID", "DocumentType": "String", "FileName": "String", "Payload": "Binary"}
            ],
            "NumberOfImages": 1,
            "Images": [
                {"ID": "ObjectID", "PictureID": "ObjectID", "PictureType": "String", "FileName": "String", "Payload": "Binary"}
            ],
            "NumberOfAudio": 1,
            "Audio": [
                {"ID": "ObjectID", "AudioID": "ObjectID", "AudioType": "String", "FileName": "String", "Payload": "Binary"}
            ],
            "NumberOfVideo": 1,
            "Video": [
                {"ID": "ObjectID", "VideoID": "ObjectID", "VideoType": "String", "FileName": "String", "Payload": "Binary"}
            ],
        }

        id_generator_result = id_generator(job)

        self.assertIsNotNone(id_generator_result)
        self.assertIsInstance(id_generator_result, dict)
        self.assertIn('ID', id_generator_result)
        self.assertEqual(id_generator_result['ID'], compute_unique_id(job))

        # Additional assertions for images, audio, and video
        self.assertIn('PictureID', id_generator_result['Images'][0])
        self.assertIn('AudioID', id_generator_result['Audio'][0])
        self.assertIn('VideoID', id_generator_result['Video'][0])

if __name__ == '__main__':
    unittest.main()