import os
from fastapi import FastAPI, UploadFile
from transcrybe import lib

app = FastAPI()


@app.post("/transcribe")
def process_route(audio: UploadFile):
    with open(f"/tmp/{audio.filename}", "wb") as file:
        file.write(audio.file.read())
    result = lib.transcribe(f"/tmp/{audio.filename}")
    os.remove(f"/tmp/{audio.filename}")
    return {"filename": audio.filename, "transcript_segments": [{"text": s["text"], "speaker": s["speaker"], "start": s["start"], "end": s["end"]} for s in result["segments"]]}
