import io
import json
from faster_whisper import WhisperModel
import streamlit as st


@st.cache_resource
def load_model():
    return WhisperModel(
        model_size_or_path="large-v3",
        device="cuda",
        compute_type="float16"
    )


class GenerateSubtitles:

    def __init__(self):
        self.model = None

    def generate_automatic(self):

        model = load_model()

        segments, info = model.transcribe(
            audio="temp/audio.mp3",
            beam_size=5,
        )

        data_segments = []

        for segment in segments:
            data_segments.append({
                'start': segment.start,
                'end': segment.end,
                'text': segment.text
            })

        return data_segments

    def generate_custom(self, len_segment: int):

        model = load_model()

        segments, info = model.transcribe(
            audio="temp/audio.mp3",
            beam_size=5,
            word_timestamps=True
        )

        data_words = []

        for segment in segments:
            for word in segment.words:
                data_words.append({
                    "start": word.start,
                    "end": word.end,
                    "word": word.word
                })

        text = ""
        pos_start = 0

        data_word_expanded = []

        for index, data in enumerate(data_words):

            if text == "":
                pos_start = data["start"]

            text += data["word"]

            if len(text) >= len_segment or index == len(data_words) - 1:
                data_word_expanded.append({
                    'start': pos_start,
                    'end': data["end"],
                    'text': text.strip()
                })

                text = ""

        return data_word_expanded

