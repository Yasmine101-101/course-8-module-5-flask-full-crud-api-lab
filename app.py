from flask import Flask, jsonify, request

app = Flask(__name__)

# Event class to represent each event
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# Our fake database (just a list)
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Home route
@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Events API!"})

# Get all events
@app.route("/events", methods=["GET"])
def get_events():
    all_events = []
    for event in events:
        all_events.append(event.to_dict())
    return jsonify(all_events)

# Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    # Get the data sent by the user
    data = request.get_json()

    # Check if title was provided
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Make a new event and add it to the list
    new_id = len(events) + 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201

# Update an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Get the data sent by the user
    data = request.get_json()

    # Check if title was provided
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Find the event and update it
    for event in events:
        if event.id == event_id:
            event.title = data["title"]
            return jsonify(event.to_dict()), 200

    # Event was not found
    return jsonify({"error": "Event not found"}), 404

# Delete an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Find the event and delete it
    for event in events:
        if event.id == event_id:
            events.remove(event)
            return jsonify({"message": "Event deleted successfully"}), 200

    # Event was not found
    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)