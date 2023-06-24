import openai
from settings import settings
import re
from typing import List
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential
)

class OPENAIService:
    def __init__(self) -> None:
        openai.api_type = "azure"
        openai.api_key = settings.api_key
        openai.api_base = "https://openaiclm.openai.azure.com"
        openai.api_version = "2023-05-15"

    def preprocess_text(self,input_text:str)->str:
        cleaned_text = re.sub(r'([.,;:?!`]{5,})', lambda match: match.group(1)[:5], input_text)
        return cleaned_text
    
    def get_embedding(self,input_text:str) -> List:
        cleaned_text = self.preprocess_text(input_text=input_text)
        text_embedding = openai.Embedding.create(input=cleaned_text,
                                                 engine='text-embedding-ada-002')
        text_embedding = text_embedding['data'][0]['embedding']

        return text_embedding
    
    @retry(wait=wait_random_exponential(min=1, max=15), stop=stop_after_attempt(settings.max_retries),reraise=True)
    def completion_with_backoff(self,**kwargs):
        return openai.ChatCompletion.create(**kwargs)
    
    def summarize_text(self,texts:List) -> List:
        prompt_str = "I want you summarize the following list of product reviews. Also highlight the key aspects of the products mentioned and sentiment of the features of the produc."
        reviews_list = "\n".join([str(idx+1)+"."+i for idx,i in enumerate(texts)])
        user_str = f"These are the product reviews:\n{reviews_list}"
        response = self.completion_with_backoff(
            engine=settings.openai_model,
            messages = [
                {"role":"system","content":prompt_str},
                {"role":"user","content":user_str}
            ]
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content
        return result
    