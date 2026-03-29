from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# GET / - Welcome message
@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Events API!"})

# GET /events - Return all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events])

# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # Task 2 - Get JSON data from the request body
    data = request.get_json()

    # Task 3 - Validate that 'title' exists in the payload
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Task 4 - Build and store the new event, return 201 Created
    new_id = max((e.id for e in events), default=0) + 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Task 2 - Get JSON data from the request body
    data = request.get_json()

    # Task 3 - Loop through events to find the matching ID
    for event in events:
        if event.id == event_id:
            # Validate that 'title' is present before updating
            if not data or "title" not in data:
                return jsonify({"error": "Title is required"}), 400

            event.title = data["title"]

            # Task 4 - Return the updated event with 200 OK
            return jsonify(event.to_dict()), 200

    # Task 4 - Return 404 if no matching event was found
    return jsonify({"error": "Event not found"}), 404


# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Task 2 - Loop through events to find the matching ID
    for event in events:
        if event.id == event_id:
            events.remove(event)
            return jsonify({"message": "Event deleted successfully"})

    # Task 4 - Return 404 if no matching event was found
    return jsonify({"error": "Event not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)