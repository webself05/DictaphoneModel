from flask import Flask, request, jsonify, send_from_directory
from recorder import Recorder
from storage import MemoryStorage
from battery import Battery
from power_manager import PowerManager

app = Flask(__name__)
from flask_cors import CORS
CORS(app)

memory = MemoryStorage()
battery = Battery()
power = PowerManager(battery)
recorder = Recorder(memory, battery, power)

@app.route('/')
def serve_index():
    return send_from_directory('UI', 'index.html')

@app.get("/messages")
def get_messages():
    return jsonify(memory.list_messages())


@app.post("/record/start")
def api_start_record():
    return jsonify({"status": recorder.start_recording()})


@app.post("/record/stop")
def api_stop_record():
    return jsonify({"status": recorder.stop_recording()})


@app.post("/play/<int:msg_id>")
def api_play(msg_id):
    return jsonify({"status": recorder.start_playback(msg_id)})


@app.delete("/message/<int:msg_id>")
def api_delete(msg_id):
    ok, msg = memory.delete_message(msg_id)
    return jsonify({"status": msg})


@app.get("/battery")
def api_battery():
    return {"battery": battery.level}


app.run(port=5000)
