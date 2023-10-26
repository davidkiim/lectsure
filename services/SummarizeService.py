from langchain.chat_models import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
# from langchain.chains.combine_documents.stuff import StuffDocumentsChain

class SummarizeService():
    def __init__(self, api_key):
        self.api_key = api_key # make sure OPENAI_API_KEY is set as env var

        # define LLM chain
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
        
        
    def summarize(self, text):
        # prompt
        prompt_template = """The following is a transcript of a video lecture. 
        Separate the transcript into important concepts with titles. 
        For each concept, write a concise summary of the transcription, in a way as to be easily reviewable as notes. 
        TRANSCRIPT:
        "{text}" 
        SUMMARY:"""
        prompt = PromptTemplate.from_template(prompt_template)
        llm_chain = LLMChain(llm=self.llm, prompt=prompt)

        return llm_chain(text)['text']
    
    def get_chapters(self, time_stamps, summary):
        prompt_template = """The following is a set of timestamps matched to text of a lecture where each timestamp is formatted in seconds:
        {time_stamps}. Your job is to compare the timestamps with the section headers of {summary}. For each section header HEADER, your job
        is to return the first relevant time-stamp TIME seconds, matching HEADER where TIME is converted to minutes and seconds in the form 
        MINUTES:SECONDS hence the output is in the format MINUTES:SECONDS: HEADER
        """
        prompt = PromptTemplate(template = prompt_template, input_variables = ["time_stamps", "summary"])
        llm_chain = LLMChain(llm=self.llm, prompt=prompt)

        return llm_chain.predict(time_stamps=time_stamps, summary=summary)
    
# if __name__ == "__main__":
#     import os
#     from dotenv import load_dotenv
#     load_dotenv()
    
#     API_KEY = os.getenv('OPENAI_API_KEY')
#     ss = SummarizeService(API_KEY)
