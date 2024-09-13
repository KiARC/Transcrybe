import os
from fastapi import FastAPI, UploadFile
from transcrybe import lib
import time

app = FastAPI()


@app.post("/transcribe")
def process_route(audio: UploadFile):
    print(f"Processing \"{audio.filename}\"...")
    with open(f"/tmp/{audio.filename}", "wb") as file:
        file.write(audio.file.read())
    start = time.perf_counter()
    result = lib.transcribe(f"/tmp/{audio.filename}")
    end = time.perf_counter()
    print(f"Done processing \"{audio.filename}\" in {end-start}s"
    os.remove(f"/tmp/{audio.filename}")
    return {"filename": audio.filename, "transcript_segments": [{"text": s["text"], "speaker": s["speaker"], "start": s["start"], "end": s["end"]} for s in result["segments"]]}
