from flask import Flask, render_template, request,jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import pickle
import time
import eventlet
from apscheduler.schedulers.background import BackgroundScheduler
# from 
from threading import Lock
import uuid
from datetime import datetime

# from flask_pymongo import PyMongo

from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://bharat:bharat@cluster0.rn63pja.mongodb.net/open24?retryWrites=true&w=majority"
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app,cors_allowed_origins='*')
db = PyMongo(app).db

CORS(app)





def load_data(filename):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []





def serialize_document(document):
    serialized = dict(document)
    serialized['_id'] = str(serialized['_id'])  # Convert ObjectId to string
    return serialized



  







@app.route('/', methods=['GET'])
def read():
    
    dishes = db.dishes.find()
    serialized_dishes = []
    for dish in dishes:
        serialized_dish = serialize_document(dish)
        serialized_dishes.append(serialized_dish)
    # print(a)
    return jsonify(list(serialized_dishes))

@app.route('/add_dish', methods=['POST'])
def addDish():
    serialized_dishes = []
    if request.method == 'POST':
        data = request.get_json()

        dishes = db.dishes.find()
        
        for dish in dishes:
            serialized_dish = serialize_document(dish)
            serialized_dishes.append(serialized_dish)


        arrs = serialized_dishes
        for i in arrs:
            # print(i["ID"])
            if i["Name"] == data["Name"]:
                return jsonify("Item has already exists")
        
        
        
            
    
    db.dishes.insert_one(data)
    
    return jsonify("Item added successfully!!")



@app.route('/get_user', methods=['POST'])
def get_User():
    if request.method == "POST":
        data = request.get_json()
        users  = db.user.find()

        user_arr = []
        for i in users:
            serialized_dish = serialize_document(i)
            user_arr.append(serialized_dish)

        arrs = list(user_arr)

        print(data)

        for i in arrs:
            if i["Email"] == data["Email"]:
                if i["Password"] == data["Password"]:
                    return jsonify(i)
                else:
                    return jsonify("Password is incorrect")

    return jsonify("Email not found")


@app.route('/user', methods=['GET'])
def users():
    user_arr = []
    users  = db.user.find()
    for i in users:
        serialized_dish = serialize_document(i)
        user_arr.append(serialized_dish)

    return jsonify(list(user_arr))


@app.route('/delete_user/<Id>', methods=['DELETE'])
def delete_users(Id):
    if request.method == "DELETE":
        user_arr = []
        users  = db.user.find()
        for i in users:
            serialized_dish = serialize_document(i)
            user_arr.append(serialized_dish)  

        arrs = list(user_arr)  
        for i in arrs:
            if i["_id"] == Id:
                deletes = db.user.delete_one({"_id": ObjectId(i["_id"])})
                return jsonify("User deleted successfully")
            
    return jsonify("Can't find user!!")
    

    





@app.route('/set_user', methods=['POST'])
def set_User():
    if request.method == "POST":
        data = request.get_json()

        users  = db.user.find()
        user_arr = []
        for i in users:
            serialized_dish = serialize_document(i)
            user_arr.append(serialized_dish)

        arrs = list(user_arr)

        for i in arrs:
            if i["Email"] == data["Email"]:
                return jsonify("Email already registered!!")
            
        db.user.insert_one(data)
        # save_data(user,'user.pkl')
            
    


    return jsonify("User added successfully")


@app.route('/order_get', methods=['GET'])
def orders_get():
    order_arr = []
    orderes  = db.order.find()
    for i in orderes:
        serialized_dish = serialize_document(i)
        order_arr.append(serialized_dish)

    arrs = list(order_arr)
    return jsonify(arrs)


@app.route('/get_orders', methods=['POST'])
def get_order():
    if request.method == "POST":
        data=request.get_json()

        order_arr = []
        orderes  = db.order.find()
        for i in orderes:
            serialized_dish = serialize_document(i)
            order_arr.append(serialized_dish)

        arrs = list(order_arr)
        arr1=[]

        for i in arrs:
            if i["Email"] == data["Email"]:
                arr1.append(i)


        




    return jsonify(arr1)

@app.route('/new_order', methods=['POST'])
def new_order():
    if request.method == 'POST':
        data = request.get_json()

        order_arr = []
        orderes  = db.order.find()
        for i in orderes:
            serialized_dish = serialize_document(i)
            order_arr.append(serialized_dish)

        arrs = list(order_arr)

        dishes = db.dishes.find()
        serialized_dishes = []
        for dish in dishes:
            serialized_dish = serialize_document(dish)
            serialized_dishes.append(serialized_dish)

        dish_arr= list(serialized_dishes)

        print(data)

        quantity = data["Quantity"]
        p = 0

        for i in dish_arr:
            if i["_id"] == data["dish_id"]:
                if int(data["Quantity"]) > int(i["Quantity"]):
                    return jsonify("Not enough quantity")
                else :
                    print("\n \n This is Bharat here \n \n")
                    q = int(i["Quantity"])
                    quantity1 = int(data["Quantity"])
                    q1 = q-quantity1
                    i["Quantity"] = q1
                    i["_id"] = ObjectId(i["_id"])
                    filter = {"_id": i["_id"]}
                    
                    update = {"$set": i}
                    store = db.dishes.update_one(filter,update)
                    p+=int(i["Price"])
                    data["ItemPrice"] = int(i["Price"])
                    data["ItemName"] = i["Name"]
                    

                    # return jsonify("")
        for i in dish_arr:
            Quantities = int(i["Quantity"])
            # print(type(Quantities))
            if Quantities <= 0 :
                db.dishes.delete_one({"_id":ObjectId(i["_id"])})

        
        q = int(data["Quantity"])
        t = q*p
        


        data["Status"] = "Pending"
        data["Total"] = t

        order_arr = []
        orderes  = db.order.find()
        for i in orderes:
            serialized_dish = serialize_document(i)
            order_arr.append(serialized_dish)

        arrs = list(order_arr)
        
        for i in arrs:
            print(f"\n\n {data} \n\n")
            if i["dish_id"] == data["dish_id"] and i["Name"] == data["Name"]:
                # print(f"\n\n {i} \n\n {data} \n\n")
                
                return jsonify("Item already exists")
                
                
            

        db.order.insert_one(data)
        # save_data(order,"order.pkl")

        # return jsonify("Item added successfull")
    


        
        


        
            
        
    
    return jsonify("Item added successfully")




@app.route('/order_update/<Id>', methods=['PATCH'])
def update_order(Id):
    if request.method == 'PATCH':
        data = request.get_json()

        order_arr = []
        orderes  = db.order.find()
        for i in orderes:
            serialized_dish = serialize_document(i)
            order_arr.append(serialized_dish)

        arrs = list(order_arr)
        


        
        
        for i in arrs:
            if i["_id"] == Id and i["Email"] == data["Email"]:
                i["Quantity"] = int(data["Quantity"])
                
                i["Total"] = i["ItemPrice"]* int(data["Quantity"])

                

                i["_id"] = ObjectId(i["_id"])
                filter = {"_id": i["_id"]}
                
                update = {"$set": i}

        
                result = db.order.update_one(filter, update)

                if result.modified_count > 0:
                    print('Item Updated successfully')
                else:
                    print('Item not found')

                # save_data(order,"order.pkl")

                dishes = db.dishes.find()
                serialized_dishes = []
                for dish in dishes:
                    serialized_dish = serialize_document(dish)
                    serialized_dishes.append(serialized_dish)

                dish_arr= list(serialized_dishes)

                print(f"\n \n {data} \n {i} \n \n")

                for j in dish_arr:
                    if j["Name"] == i["ItemName"]:
                        # a = int(j["Quantity"])
                        # a -=int(data["Value"])
                        j["Quantity"] = int(j["Quantity"]) + data["Value"]

                        # obj={
                        #         "Quantity": int(i["Quantity"]),
                        #         "Price" : int(i["Price"]),
                        #         "ID": int(i["ID"]),
                        #         "Name" : i["Name"],
                        #         "Img": i["Img"]
                        #     }
                        j["_id"] = ObjectId(j["_id"])
                        # save_data(arr,"arr.pkl")
                        filter = {"_id": j["_id"]}
                        update = {"$set": j}

        
                        result = db.dishes.update_one(filter, update)

                        if result.modified_count > 0:
                            print('Item Updated successfully')
                        else:
                            print('Item not found')
                        # db.dishes.update_one({"ID":int(i["ID"])}, i)

                        if j["Quantity"] <= 0:
                            # arr.remove(i)

                            db.dishes.delete_one({"_id": j["_id"]})
                            
                            break;
                
                return jsonify("Item Updated successfully")
            
        
        
    return jsonify("ID not found")




@app.route('/update/<Id>', methods=['PATCH'])
def update_dish(Id):

    

    # print(type(Id))
    if request.method == 'PATCH':
        data = request.get_json()

        dishes = db.dishes.find()
        serialized_dishes = []
        for dish in dishes:
            serialized_dish = serialize_document(dish)
            serialized_dishes.append(serialized_dish)

        dish_arr= list(serialized_dishes)

        for i in dish_arr:
            if i["_id"] == Id:
                print(f"\n\n {data} \n\n")
                data["_id"] = ObjectId(data["_id"])

                filter = {"_id": data["_id"]}
                update = {"$set": data}

        
                result = db.dishes.update_one(filter, update)

                if result.modified_count > 0:
                    print('Item Updated successfully')
                else:
                    print('Item not found')

                return jsonify("Item update successfully")


        
        
    return jsonify("Item not found")

@app.route('/delete/<Id>', methods=['DELETE'])
def remove_dish(Id):
    if request.method == 'DELETE':
        
        dishes = db.dishes.find()
        serialized_dishes = []
        for dish in dishes:
            serialized_dish = serialize_document(dish)
            serialized_dishes.append(serialized_dish)

        dish_arr= list(serialized_dishes)

        
        for i in dish_arr:
            if i["_id"] ==Id:
                
                db.dishes.delete_one({"_id": ObjectId(i["_id"])})
                # save_data(arr,"arr.pkl")
                return jsonify("Item delete successfully")
                
            
        
       
    return jsonify('Item not found')


@app.route('/delete_order/<Id>', methods=['DELETE'])
def remove_order(Id):
    if request.method == 'DELETE':
        
        

        order_arr = []
        orderes  = db.order.find()
        for i in orderes:
            serialized_dish = serialize_document(i)
            order_arr.append(serialized_dish)

        arrs = list(order_arr)
        for i in arrs:
            if i["_id"] == Id:
                data = i
                db.order.delete_one({"_id": ObjectId(i["_id"])})
                # order.remove(i)
                # save_data(order,"order.pkl")

                dishes = db.dishes.find()
                serialized_dishes = []
                for dish in dishes:
                    serialized_dish = serialize_document(dish)
                    serialized_dishes.append(serialized_dish)

                dish_arr= list(serialized_dishes)

                for i in dish_arr:
                    if i["Name"] == data["ItemName"]:
                        a = int(i["Quantity"])
                        a +=int(data["Quantity"])
                        i["Quantity"] = a
                        # save_data(arr,"arr.pkl")
                        i["_id"] = ObjectId(i["_id"])
                        filter = {"_id": i["_id"]}
                        
                        update = {"$set": i}

        
                        result = db.dishes.update_one(filter, update)

                        if result.modified_count > 0:
                            print('Item Updated successfully')
                        else:
                            print('Item not found')


                        
                return jsonify("Item delete successfully")
                
            
        
       
    return jsonify('Item not found')


@app.route('/confirm_order', methods=["POST"])
def confirm_order():
    if request.method == "POST":
        data = request.get_json()


        order_arr = []
        orderes  = db.order.find()
        for i in orderes:
            serialized_dish = serialize_document(i)
            order_arr.append(serialized_dish)

        arrs = list(order_arr)

        def generate_random_id():
           timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
           unique_id = str(uuid.uuid4()).replace("-", "")
           random_id = f"{timestamp}{unique_id[:6]}"
           return random_id

        random_id = generate_random_id()

        print(f"\n\n {random_id} \n\n")



        for i in arrs:
            if i["Email"] == data["Email"]:
                i["Status"] = "Confirm"
                i["order_id"] = random_id
                i["_id"] = ObjectId(i["_id"])
                
                
                
                # successful_order.append(i)
                deletes = db.order.delete_one({"_id": i["_id"]})
                del i["_id"]
                db.confirm.insert_one(i)
                # save_data(order,"order.pkl")
                # save_data(successful_order,"successful_order.pkl")
        
        return jsonify("Order confirm")

@app.route('/get_confirm_order', methods=["GET"])
def confirm():
    confirm_arr = []
    orderes  = db.confirm.find()
    for i in orderes:
        serialized_dish = serialize_document(i)
        confirm_arr.append(serialized_dish)

    confirm_arrs = list(confirm_arr)
    return jsonify(confirm_arrs)



@app.route('/delete_confirm_order/<Id>', methods=["DELETE"])
def delete_confirm(Id):
    if request.method == "DELETE":
        data = request.get_json()
        confirm_arr = []
        orderes  = db.confirm.find()
        for i in orderes:
           serialized_dish = serialize_document(i)
           confirm_arr.append(serialized_dish)

        confirm_arrs = list(confirm_arr)

        for i in confirm_arrs:
            if i["_id"] == Id:
                deletes = db.confirm.delete_one({"_id": ObjectId(data["ID"])})
                return jsonify("Item deleted successfully")
            
    return jsonify("Item not found")



@app.route('/status_change/<Id>', methods=["PATCH"])
def status_change(Id):
    if request.method == "PATCH":
        data = request.get_json()
        confirm_arr = []
        orderes  = db.confirm.find()
        for i in orderes:
           serialized_dish = serialize_document(i)
           confirm_arr.append(serialized_dish)

        confirm_arrs = list(confirm_arr)

        for i in confirm_arrs:
            if i["order_id"] == Id:    
                i['Status'] = data["Status"]
                i["_id"] = ObjectId(i["_id"])
                filter = {"_id": i["_id"]}

                update = {"$set": i}
                result = db.confirm.update_one(filter, update)   
                confirm_arr1 = []
                orderes1  = db.confirm.find()
                for j in orderes1:
                   serialized_dish = serialize_document(j)
                   confirm_arr1.append(serialized_dish)

                confirm_arrs1 = list(confirm_arr1)         

                socketio.emit('updater', confirm_arrs1)  

                for j in confirm_arrs1:
                    if j['Status'] == 'Delivered':
                          deleted = db.confirm.delete_one({"_id": ObjectId(j["_id"])})
                          del j["_id"]
                          db.successfull.insert_one(j)


                

                
                
            
    return jsonify("Item State Updated")



@app.route('/get_success_order', methods=["GET"])
def success():
    success_arr = []
    orderes  = db.successfull.find()
    for i in orderes:
        serialized_dish = serialize_document(i)
        success_arr.append(serialized_dish)

    success_arrs = list(success_arr)
    return jsonify(success_arrs)



@app.route('/get_success_order_with_email', methods=["POST"])
def successPost():
         data = request.get_json()
         if request.method == "POST":
            success_arr = []
         orderes  = db.successfull.find()
         for i in orderes:
             serialized_dish = serialize_document(i)
             success_arr.append(serialized_dish)

         success_arrs = list(success_arr)

         arr5 = []

         for i in success_arrs:
             if i["Email"] == data["Email"]:
                 arr5.append(i)


         return jsonify(arr5)     


@app.route('/delete_success_order/<Id>', methods=["DELETE"])
def delete_success(Id):
    if request.method == "DELETE":
        success_arr = []
        orderes  = db.successfull.find()
        for i in orderes:
            serialized_dish = serialize_document(i)
            success_arr.append(serialized_dish)

        success_arrs = list(success_arr)
        for i in success_arrs:
            if i["_id"] == Id:
                deletes = db.successfull.delete_one({"_id": ObjectId(i["_id"])})
                return jsonify("Item deleted successfully")
        
    return jsonify("Item not found")


        
        




    

            




 

@socketio.on('connect')
def handle_connect():
    # background_task()
    print("user connected")

    confirm_arr1 = []
    orderes1  = db.confirm.find()
    for i in orderes1:
        serialized_dish = serialize_document(i)
        confirm_arr1.append(serialized_dish)

    confirm_arrs1 = list(confirm_arr1)     
           

    socketio.emit('updater', confirm_arrs1)  
    
    



            




if __name__ == '__main__':
    socketio.run(app, debug=True)
    