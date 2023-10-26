import os
import torch
import whisper
import datetime
import math

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

class ModelSize:
    TINY = 'tiny.en'
    BASE = 'base.en'
    SMALL = 'small.en'
    MED = 'medium.en'

class WhisperService:
    def __init__(self) -> None:
        self.model = whisper.load_model(ModelSize.TINY) # base.en, small.en, medium.en
        # predict without timestamps for short-form transcription
        self.options = whisper.DecodingOptions(language='en', without_timestamps=False)

    def transcribe(self, file_path):
        transcription = self.model.transcribe(file_path)
        formatted_timestamps = '\n'.join([f"{str(datetime.timedelta(seconds = math.floor(int(phrase['start']))))}: {phrase['text']}" for phrase in transcription['segments']])

        return transcription['text'], formatted_timestamps

# if __name__ == '__main__':
#     test = WhisperService()
#     print(test.transcribe('../uploads/test.m4a'))
