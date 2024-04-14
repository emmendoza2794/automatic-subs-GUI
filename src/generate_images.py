import os
import subprocess

from PIL import Image, ImageDraw, ImageFont


class GenerateImages:

    def __init__(self):
        self.draw = None

    def _wrap_text(self, text, font, max_width):

        lines = []
        words = text.split(" ")
        temp_line = ""
        for word in words:
            if self.draw.textbbox((0, 0), temp_line + word, font=font)[2] <= max_width:
                temp_line += " " + word if temp_line else word
            else:
                lines.append(temp_line)
                temp_line = word
        lines.append(temp_line)

        return "\n".join(lines)

    def dimensions_video(self):
        ffmpeg_command = [
            'ffmpeg',
            '-loglevel', 'warning',
            '-i', 'temp/video.mp4',
            '-ss', '00:00:3',
            '-vframes', '1',
            'temp/video_preview.jpg',
            '-y'
        ]

        subprocess.run(ffmpeg_command)

        img = Image.open("temp/video_preview.jpg")

        width, height = img.size

        return width, height

    def multi_line_img(
            self,
            text: str,
            font: str,
            font_size: int,
            text_color: str,
            border_color: str,
            text_position: str,
            name: str,
            width: int,
            height: int,
    ):

        image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(image)

        margin = height * 0.05

        font = ImageFont.truetype(f"assets/fonts/{font}.ttf", font_size)

        lines_text = self._wrap_text(text, font, width - 2 * margin)

        text_box = self.draw.textbbox(
            xy=(0, 0),
            text=lines_text,
            font=font,
            spacing=int(font_size / 10),
            align="center",
            stroke_width=int(font_size / 15)

        )

        if text_position == "Top":
            position_x = height * 0.1

        if text_position == "Center":
            position_x = (height - (text_box[3] * 1.5)) // 2

        if text_position == "Bottom":
            position_x = (height * 0.8) - (text_box[3] // 2)

        self.draw.multiline_text(
            xy=((width-text_box[2]) // 2, position_x),
            text=lines_text,
            font=font,
            fill=text_color,
            spacing=int(font_size / 10),
            align="center",
            stroke_fill=border_color,
            stroke_width=int(font_size / 15)
        )

        name = f"temp/subs/{name}.png"

        image.save(name)

        return name

    def preview_text(
            self,
            uploaded_video: bool,
            text: str,
            font: str,
            font_size: int,
            text_color: str,
            border_color: str,
            text_position: str,
    ):

        if uploaded_video and os.path.exists('temp/video.mp4'):
            width, height = self.dimensions_video()
            image = Image.open("temp/video_preview.jpg")

        else:
            width = 1920
            height = 1080
            image = Image.new("RGB", (width, height), (234, 234, 234))

        margin = width * 0.05

        self.draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(f"assets/fonts/{font}.ttf", font_size)

        lines_text = self._wrap_text(text, font, width - 2 * margin)

        text_box = self.draw.textbbox(
            xy=(0, 0),
            text=lines_text,
            font=font,
            spacing=int(font_size / 10),
            align="center",
            stroke_width=int(font_size / 15)

        )

        if text_position == "Top":
            position_x = height * 0.1

        if text_position == "Center":
            position_x = (height - (text_box[3] * 1.5)) // 2

        if text_position == "Bottom":
            position_x = (height * 0.8) - (text_box[3] // 2)

        self.draw.multiline_text(
            xy=((width - text_box[2]) // 2, position_x),
            text=lines_text,
            font=font,
            fill=text_color,
            spacing=int(font_size / 10),
            align="center",
            stroke_fill=border_color,
            stroke_width=int(font_size / 15)
        )

        image.save("temp/text_preview.jpg")
