import os
import torch
import whisper

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class WhisperService:
    def __init__(self) -> None:
        self.model = whisper.load_model('base.en') # base.en, small.en, medium.en
        # predict without timestamps for short-form transcription
        self.options = whisper.DecodingOptions(language="en", without_timestamps=True)

    def transcribe(self, file_path):
        transcription = self.model.transcribe(file_path)
        return transcription['text']

if __name__ == '__main__':
# test = WhisperService()
# print(test.transcribe('../uploads/test.m4a'))
