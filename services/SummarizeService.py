from langchain.chat_models import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

class SummarizeService():
    def __init__(self, api_key):
        self.api_key = api_key
        
        # prompt
        self.prompt_template = """Write a concise summary of the following:
        "{text}"
        CONCISE SUMMARY:"""
        self.prompt = PromptTemplate.from_template(self.prompt_template)

        # define LLM chain
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)

        # # define StuffDocumentsChain
        # self.stuff_chain = StuffDocumentsChain(
        #     llm_chain=self.llm_chain, document_variable_name="text"
        # )

    def summarize(self, text):
        return self.llm_chain(text)['text']


