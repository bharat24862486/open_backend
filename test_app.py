from server import app, db
from flask import jsonify
import json


def serialize_document(document):
    serialized = dict(document)
    serialized['_id'] = str(serialized['_id'])  # Convert ObjectId to string
    return serialized


def test_get():
    # Insert a sample document for testing
    # data = {"Name": "Dal", "Price": 150, "Quantity": 200, "Img": "Img1","ID":200}
    # db.dishes.insert_one(data)

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        datas = db.dishes.find()
        
        serialized_dishes = []
        for dish in datas:
            serialized_dish = serialize_document(dish)
            serialized_dishes.append(serialized_dish)


        assert response.status_code == 200
        print(list(serialized_dishes))
        assert response.get_data() == f"{jsonify(list(serialized_dishes))}\n"
        assert response.data.decode('utf-8') == response.get_data()
        # assert response.get_data(as_text=True) == expected_response

    # Clean up the inserted test data
    # db.dishes.delete_one(data)
