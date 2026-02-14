from flask import Flask, render_template, request, send_file
import requests
import os
from datetime import datetime

# Voices: Male and Female
VOICES = {
    "Male": "21m00Tcm4TlvDq8ikWAM",
    "Female": "EXAVITQu4vr4xnSDxMaL"  # your female voice
}

# Make sure static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

app = Flask(__name__)

# Keep history of generated files
history = []

def generate_audio(text, voice_id, speed=1.0, volume=1.0, stability=0.75, similarity_boost=0.85):
    """Call ElevenLabs TTS API and save audio to static folder with timestamp"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"output_{timestamp}.mp3"
        path = f"static/{filename}"
        with open(path, "wb") as f:
            f.write(response.content)
        history.append(filename)
        return filename
    else:
        print("Error:", response.text)
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    if request.method == "POST":
        text = request.form.get("text")
        voice = request.form.get("voice", "Female")
        speed = float(request.form.get("speed", 1.0))
        volume = float(request.form.get("volume", 1.0))
        if text:
            audio_file = generate_audio(text, VOICES.get(voice, VOICES["Female"]), speed, volume)
    return render_template("index.html", audio_file=audio_file, voices=VOICES.keys(), history=history)

@app.route("/download")
def download():
    file = request.args.get("file")
    if file and os.path.exists(f"static/{file}"):
        return send_file(f"static/{file}", as_attachment=True)
    return "No audio found", 404

if __name__ == "__main__":
    app.run(debug=True)

