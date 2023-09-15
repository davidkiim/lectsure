# Project Lectsure

### Goal
Make it easier to digest & review recordings? Learn faster? Help ADHD students

### Features
- Upload lecture (audio/video)
- Transcription, display transcription
- Summary of transcription
- Display video with chapters
- Chatbot with the lecture transcription

### Techstack
Gradio, GPT/other LLM API, Whisper/other transcription API

### User Flow
1. Upload the video -> submit
2. Video needs to be sent to OpenAI(or best vid transcription softwares)
3. Once transcript received, display in text box
4. Send transcript to OpenAI to get summary
5. Once summary received, display summary
6. Adjust prompt for chatbot to include summary
