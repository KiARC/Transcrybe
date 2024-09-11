# This is all built off of the example in the README of https://github.com/m-bain/whisperX
from os import environ
import whisperx

import whisperx.utils

trans_model = whisperx.load_model(
    "small", "cpu", compute_type="int8", language="en")
align_model, align_model_meta = whisperx.load_align_model(
    language_code="en", device="cpu")
dia_model = whisperx.DiarizationPipeline(
    use_auth_token=environ.get("TRANSCRYBE_HF_TOKEN"), device="cpu")


def transcribe(filename: str):
    audio = whisperx.load_audio(filename)
    result = trans_model.transcribe(audio, batch_size=8)
    result = whisperx.align(result["segments"], align_model,
                            align_model_meta, audio, "cpu", return_char_alignments=False)
    dia_segments = dia_model(audio)
    result = whisperx.assign_word_speakers(dia_segments, result)
    return result
