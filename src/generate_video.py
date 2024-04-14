import subprocess

LOGLEVEL = "warning"


class GenerateVideo:

    def generate(self, subtitles: list):

        video_final = [
            "ffmpeg",
            "-loglevel", LOGLEVEL,
            "-i", "temp/video.mp4",
            '-y'
        ]

        overlays = []

        for index, subtitle in enumerate(subtitles):
            if index == 0:
                overlays.append(
                    f"[0:v][1:v]"
                    f"overlay=0:0:enable='between(t,{subtitle['start']},{subtitle['end']})'"
                    f"[v1]"
                )
            else:
                overlays.append(
                    f"[v{index}][{index + 1}:v]"
                    f"overlay=0:0:enable='between(t,{subtitle['start']},{subtitle['end']})'"
                    f"[v{index + 1}]"
                )

            video_final.extend(["-i", subtitle["img_path"]])

        video_final += [
            "-filter_complex",
            ";".join(overlays),
            "-map", "0:a",
            '-c:a', 'copy',
            "-map",
            f"[v{len(subtitles)}]",
            "output/final_video.mp4",
            "-y"
        ]

        subprocess.run(video_final)

        return True
