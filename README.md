# ⚡automatic-subs-GUI⚡

This project automatically generates subtitles for any mp4 video, for this the following libraries were used:
- Fast-whisper (https://github.com/SYSTRAN/faster-whisper)
- Streamlit (https://streamlit.io/)
- Pillow (https://python-pillow.org/)
- FFmpeg (https://ffmpeg.org/)

🗂 Its operation is simple, the entire graphical interface is on **Streamlit**, with **FFmpeg** we extract the audio from 
the video, we pass it through **Fast-whisper** to convert the audio to text, with **Pillow** we generate the png images 
with the subtitles and the available configurations, and lastly step we superimpose the images on the video 
at the indicated time with **FFmpeg**

## 🚨Prerequisites🚨
- CUDA compatibility
- have FFmpeg installed
- python 3.10 ^


## 🚧local installation🚧

1. create the virtual environment with pip venv and activate it 
```bash
python -m venv venv
source venv/bin/activate # linux
```
2. install dependencies
```bash
pip install -r requirements.txt
```
3. run the app 
```bash
streamlit run app.py 🚀🚀
```
