# This is all built off of the example in the README of https://github.com/m-bain/whisperX
from os import environ
import whisperx

import whisperx.utils

if (
    not environ.get("TRANSCRYBE_HF_TOKEN")
    or environ.get("TRANSCRYBE_HF_TOKEN") == "PLEASE_ADD_A_TOKEN"
):
    print("Please set the TRANSCRYBE_HF_TOKEN environment variable.")
    exit(1)

if not environ.get("TRANSCRYBE_MODEL_SIZE") or environ.get(
    "TRANSCRYBE_MODEL_SIZE"
) not in [
    "tiny",
    "tiny.en",
    "base",
    "base.en",
    "small",
    "small.en",
    "medium",
    "medium.en",
    "large",
    "large-v2",
]:
    print("Please set TRANSCRYBE_MODEL_SIZE to a valid size for the whisper model.")
    exit(2)

if not environ.get("TRANSCRYBE_LANGUAGE"):
    print("Please set TRANSCRYBE_LANGUAGE to a valid language for the whisper model.")
    exit(3)

trans_model = whisperx.load_model(environ.get("TRANSCRYBE_MODEL_SIZE"), "cpu", compute_type="int8", language=environ.get("TRANSCRYBE_LANGUAGE"))
align_model, align_model_meta = whisperx.load_align_model(
    language_code=environ.get("TRANSCRYBE_LANGUAGE"), device="cpu"
)
dia_model = whisperx.DiarizationPipeline(
    use_auth_token=environ.get("TRANSCRYBE_HF_TOKEN"), device="cpu"
)


def transcribe(filename: str):
    audio = whisperx.load_audio(filename)
    result = trans_model.transcribe(audio, batch_size=8)
    result = whisperx.align(
        result["segments"],
        align_model,
        align_model_meta,
        audio,
        "cpu",
        return_char_alignments=False,
    )
    dia_segments = dia_model(audio)
    result = whisperx.assign_word_speakers(dia_segments, result)
    return result
