from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():

    if request.method == 'GET':

        all_messages = []
        for message in Message.query.order_by(Message.created_at).all():
            all_messages.append(message.to_dict())

        return make_response(all_messages, 200)
    
    elif request.method == 'POST':

        #request JSON is transfered into dictionary
        params = request.json

        #turned into an object - instance
        new_message = Message(
            body = params['body'],
            username = params['username']
        )

        #instance is added to db
        #only objects can be added to db w SQLAlchemy
        db.session.add(new_message)
        db.session.commit()


        #changes new_message from object (instance) to dictionary
        return make_response(new_message.to_dict(), 201)



@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    # Retrieve the message with the given ID from the database
    message = Message.query.get(id)
    
    # Check if the message exists
    if message:
        # Handle PATCH request to update the message
        if request.method == 'PATCH':
            
            # Convert the incoming JSON request to a dictionary
            params = request.json

            # Update the message body with the new data from the request
            message.body = params['body']
            
            # Commit the changes to the database
            db.session.commit()

            # Return the updated message as a JSON response with status code 200
            return make_response(message.to_dict(), 200)
        
        # Handle DELETE request to delete the message
        elif request.method == 'DELETE':
            # Delete the message from the database
            db.session.delete(message)
            
            # Commit the deletion to the database
            db.session.commit()
            
            # Return an empty response with status code 204 (No Content)
            return make_response('', 204)





if __name__ == '__main__':
    app.run(port=5555)
