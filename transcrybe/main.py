import os
from fastapi import FastAPI, UploadFile
from transcrybe import lib

app = FastAPI()


@app.post("/transcribe")
def process_route(audio: UploadFile):
    with open(f"to-process_{audio.filename}", "wb") as file:
        file.write(audio.file.read())
    result = lib.transcribe(f"to-process_{audio.filename}")
    os.remove(f"to-process_{audio.filename}")
    return [{"text": s["text"], "speaker": s["speaker"], "start": s["start"], "end": s["end"]} for s in result["segments"]]
