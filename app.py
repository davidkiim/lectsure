import gradio as gr

import asyncio, httpx
import async_timeout

from loguru import logger
from typing import Optional, List
from pydantic import BaseModel

from services.TranscribeService import WhisperService
from services.SummarizeService import SummarizeService

import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

class Message(BaseModel):
    role: str
    content: str

ws = WhisperService()
ss = SummarizeService(API_KEY)
async def make_completion(messages:List[Message], nb_retries:int=3, delay:int=30) -> Optional[str]:
    '''
    Sends a request to the ChatGPT API to retrieve a response based on a list of previous messages.
    '''
    header = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    try:
        async with async_timeout.timeout(delay=delay):
            async with httpx.AsyncClient(headers=header) as aio_client:
                counter = 0
                keep_loop = True
                while keep_loop:
                    logger.debug(f'Chat/Completions Nb Retries : {counter}')
                    try:
                        resp = await aio_client.post(
                            url = 'https://api.openai.com/v1/chat/completions',
                            json = {
                                'model': 'gpt-3.5-turbo',
                                'messages': messages
                            }
                        )
                        logger.debug(f'Status Code : {resp.status_code}')
                        if resp.status_code == 200:
                            return resp.json()['choices'][0]['message']['content']
                        else:
                            logger.warning(resp.content)
                            keep_loop = False
                    except Exception as e:
                        logger.error(e)
                        counter = counter + 1
                        keep_loop = counter < nb_retries
    except asyncio.TimeoutError as e:
        logger.error(f'Timeout {delay} seconds !')
    return None

async def predict(input, history):
    '''
    Predict the response of the chatbot and complete a running list of chat history.
    '''
    history.append({'role': 'user', 'content': input})
    response = await make_completion(history)
    history.append({'role': 'assistant', 'content': response})
    messages = [(history[i]['content'], history[i+1]['content']) for i in range(0, len(history)-1, 2)]
    return messages, history

async def on_upload(video, history):
        file_path = video
        transcript, ts_transcript = ws.transcribe(file_path)
        summary = ss.summarize(transcript)
        chapters = ss.get_chapters(ts_transcript, summary)

        prompt = f"""You are a helpful teaching assistant, your job is to answer questions concisely in a friendly tone based on 
        the following transcription of a lecture video:
        "{transcript}" 
        """
        history.append({'role': 'user', 'content': prompt})
        response = await make_completion(history)
        history.append({'role': 'assistant', 'content': response})

        return transcript, summary, chapters, history

def video_identity(video):
    return video

'''
Gradio Blocks low-level API that allows to create custom web applications (here our chat app and video player)
'''
with gr.Blocks() as demo:
    state = gr.State([]) # chatbot message history

    title = gr.Markdown('#Lectsure AI')

    with gr.Row():
        vid = gr.Video(type='filepath', scale=3)
        chapters = gr.Textbox(interactive=False, label='Chapter List', scale=1)
        
    with gr.Row():
        summary = gr.Textbox(label='Summary', interactive=False, scale=2)
        with gr.Column(scale=0):
            chatbot = gr.Chatbot(label='Lectsure AI', scale=1)
            txt = gr.Textbox(show_label=False, placeholder='Enter text and press enter', scale=1)
            txt.submit(predict, [txt, state], [chatbot, state])

    transcript = gr.Textbox(label='Transcript', interactive=False)

    vid.upload(fn=on_upload, inputs=[vid, state], outputs=[transcript, summary, chapters, state])

    
if __name__ == '__main__':
    logger.info('Starting Demo...')
    demo.launch(server_port=8080)
