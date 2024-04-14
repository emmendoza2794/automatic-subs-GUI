import os


class Utils:

    def list_fonts(self):

        fonts_dir = os.listdir('assets/fonts')
        fonts_names = [name.replace('.ttf', '') for name in fonts_dir]

        return fonts_names
