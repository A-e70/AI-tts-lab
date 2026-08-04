# AI TTS Lab

A small Flask web interface for the ElevenLabs text to speech API. Type text, pick a voice, get an MP3 back, and keep a history of what you generated.

To be clear about what this is: the speech synthesis is done by ElevenLabs. This is the interface around it, not a synthesis engine.

## Running it

```bash
pip install -r requirements.txt
export ELEVEN_API_KEY='your-key'     # from elevenlabs.io
python app.py
```

Then open <http://127.0.0.1:5000>.

The key is read from the environment and is never written to disk or committed.

## What it does

- Sends text to the ElevenLabs API and saves the returned MP3 to `static/`, timestamped
- Two preset voices, selectable from a dropdown
- A running list of everything generated this session, each downloadable

## What it does not do yet

The interface has speed and volume sliders. Their values reach the backend but are not applied to the request, so moving them currently changes nothing about the output. They are left visible rather than removed, because wiring them to the API's voice settings is the obvious next change.

## Fixed since the first version

**The API key was never assigned.** It was referenced when building the request headers but never set anywhere in the file, so a fresh clone raised a `NameError` on the first generation. It now comes from `ELEVEN_API_KEY`, and the app refuses to start without it.

**The download route could serve any file on the machine.** The filename came from the query string and was interpolated straight into a path, so `?file=../../../etc/passwd` walked out of the static folder. The path is now resolved and checked to be inside `static/` before anything is sent.

## Licence

MIT.
