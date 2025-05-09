import json
import os
import shutil
import subprocess

import streamlit as st

from src.generate_images import GenerateImages
from src.generate_subtitles import GenerateSubtitles
from src.generate_video import GenerateVideo
from src.utils import Utils

if 'text_preview_path' not in st.session_state:
    st.session_state.text_preview_path = None

if 'final_video' not in st.session_state:
    st.session_state.final_video = None


def generate_video_subs():
    if st.session_state.video_file is None:
        st.toast('video file not found', icon="🚨")
        return

    with st.spinner(f'Extracting audio...'):
        ffmpeg_command = [
            "ffmpeg",
            "-loglevel", "warning",
            "-i", "temp/video.mp4",
            "temp/audio.mp3",
            "-y"
        ]

        subprocess.run(ffmpeg_command)

    with st.spinner(f'generating substitutes...'):

        if st.session_state.subtitle_length == "Automatic":
            text_subs = GenerateSubtitles().generate_automatic()

        if st.session_state.subtitle_length == "Custom":
            text_subs = GenerateSubtitles().generate_custom(len_segment=st.session_state.min_chars)

    with st.spinner(f'generating video with subs...'):

        width, height = GenerateImages().dimensions_video()

        shutil.rmtree('temp/subs', ignore_errors=True)
        os.makedirs('temp/subs', exist_ok=True)

        for index, sub in enumerate(text_subs):
            text_subs[index]["img_path"] = GenerateImages().multi_line_img(
                text=sub["text"],
                font=st.session_state.font,
                font_size=st.session_state.font_size,
                text_color=st.session_state.color_text,
                border_color=st.session_state.color_border,
                text_position=st.session_state.text_position,
                name=f"subtitle_{index}",
                width=width,
                height=height,
            )

        GenerateVideo().generate(subtitles=text_subs)

        st.session_state.final_video = "output/final_video.mp4"


def generate_text_preview():
    GenerateImages().preview_text(
        uploaded_video=False if st.session_state.video_file is None else True,
        text="Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
        font=st.session_state.font,
        font_size=st.session_state.font_size,
        text_color=st.session_state.color_text,
        border_color=st.session_state.color_border,
        text_position=st.session_state.text_position
    )

    st.session_state.text_preview_path = "temp/text_preview.jpg"


st.set_page_config(
    page_title="Automatic Subs GUI test",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    unsafe_allow_html=True,
    body="""
    <style>
           img {
               max-height: 700px;         
           }
           .block-container {
                padding-top: 2rem;
           }
           video {
               max-height:700px;
           }
    </style>
    """
)

st.header('Automatic Subtitle Generator', divider='rainbow')

col1, col2, col3 = st.columns([0.25, 0.375, 0.375])

with col1:
    with st.container(border=True):
        st.subheader("Video file")

        st.file_uploader(
            label="Video file",
            key="video_file",
            label_visibility="collapsed",
            type=['mp4']
        )

        if st.session_state.video_file is not None:
            with open(f'temp/video.mp4', 'wb') as f:
                f.write(st.session_state.video_file.getvalue())

    with st.container(border=True):
        st.subheader("Subtitle settings")

        st.selectbox(
            label='Font',
            key="font",
            options=Utils().list_fonts()
        )

        st.slider(
            label="Font size",
            min_value=30,
            max_value=90,
            value=70,
            key="font_size",
            step=1
        )

        col_color_1, col_color_2 = st.columns([0.5, 0.5])

        with col_color_1:
            st.color_picker(
                label="Text color",
                key="color_text",
                value="#ffffff"
            )

        with col_color_2:
            st.color_picker(
                label="Border color",
                key="color_border",
                value="#000"
            )

        st.radio(
            label="Text position",
            key="text_position",
            index=2,
            options=["Top", "Center", "Bottom"],
            horizontal=True,
        )

        st.radio(
            label="Subtitle length",
            key="subtitle_length",
            index=0,
            options=["Automatic", "Custom"],
            horizontal=True,
        )

        st.slider(
            label="Minimum characters",
            min_value=10,
            max_value=150,
            value=70,
            key="min_chars",
            step=1,
            disabled=st.session_state.subtitle_length == "Automatic"
        )

    st.button(
        label="Generate video",
        type="primary",
        on_click=generate_video_subs,
        use_container_width=True,
    )

with col2:
    with st.container(border=True):
        st.subheader("Subtitle preview")

        generate_text_preview()

        if st.session_state.text_preview_path is not None:
            st.image(st.session_state.text_preview_path)

with col3:
    with st.container(border=True):
        st.subheader("Final video")

        if st.session_state.final_video is not None:
            st.video(st.session_state.final_video)

            with open(st.session_state.final_video, "rb") as file:
                st.download_button(
                    type="primary",
                    label="Download video",
                    data=file,
                    file_name="final_video.mp4",
                    mime="video/mp4"
                )
