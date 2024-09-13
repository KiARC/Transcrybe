# Transcrybe

FastAPI based service that transcribes and diarizes audio files.

## Usage

### Setup

See [docker-compose.example.yml](docker-compose.example.yml) for an example configuration.

The `TRANSCRYBE_HF_TOKEN` environment variable **must be set** to a Hugging Face Access Token with the permission "Read access to contents of all public gated repos you can access". You must fill out the access forms for [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0) and [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1) on the same Hugging Face account that the token is created from.

The `TRANSCRYBE_MODEL_SIZE` environment variable is **optional**. The default value is `base.en`, which slightly prioritizes speed over accuracy and should be fine for most use cases. If another version is needed, this variable can be set to any of: `tiny`, `tiny.en`, `base`, `base.en`, `small`, `small.en`, `medium`, `medium.en`, `large` or `large-v2`. Larger models will provide more accurate results, and those not suffixed with `.en` can handle non-English speech, but these come at the cost of speed as well as storage and memory usage. Generally speaking, you should probably use the smallest model that is accurate enough for your use case. If your deployment will only be processing English speech, the `.en` models will be more accurate compared to the non-`.en` models of the same size.

The `TRANSCRYBE_LANGUAGE` environment variable is **optional**. The default value is `en`.

### Endpoints

#### FastAPI Builtins

|Path|Methods|Description|
|:---|:------|:----------|
|`/docs`|GET|Swagger UI documentation|
|`/redoc`|GET|ReDoc documentation|
|`/openapi.json`|GET|OpenAPI spec for consumption by other tools and services|

#### Transcrybe
|Path|Methods|Description|
|:---|:------|:----------|
|`/transcribe`|POST|Submit files for transcription. Request body should be `multipart/form-data` and should have a single field, `audio`, which contains the file to transcribe. The return value will be an `application/json` object in the format described below.|

##### `/transcribe` Response Format
```json
{
  "filename": "The name of the file that was transcribed",
  "transcript_segments": [
    {
      "text": "The transcribed content of the segment",
      "speaker": "The identified speaker, i.e. SPEAKER_00, SPEAKER_01...",
      "start": "The starting point in fractional seconds",
      "end": "The ending point in fractional seconds"
    },
  ]
}
```
