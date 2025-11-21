from googletrans import Translator as GT

class Translator:
    def __init__(self):
        self.translator = GT()

    def translate(self, text, src, dest):
        result = self.translator.translate(text, src=src, dest=dest)
        return result.text
