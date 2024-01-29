import asyncio
from openai import OpenAI, AsyncOpenAI

class SyncChat:
    def __init__(self, model, config):
        if config["base_url"] != None:
            self.sync_client = OpenAI(base_url=config["base_url"],api_key=config["api_key"])
        else:
            self.sync_client = OpenAI(api_key=config["api_key"])
        self.model = model
        
    def get_response(self, message, temperature=0.2, max_tokens=1024):
        response  = self.sync_client.chat.completions.create(
                        model=self.model,
                        messages=message,
                        temperature=temperature,
                        max_tokens=max_tokens)
        return response.choices[0].message.content

            
class AsyncChat:
    def __init__(self, model, config):
        if config["base_url"] != None:
            self.async_client = AsyncOpenAI(base_url=config["base_url"], api_key=config["api_key"])
        else:
            self.async_client = AsyncOpenAI(api_key=config["api_key"])
        self.model = model
    
    async def get_response(self, messages,temperature=0.2,max_tokens=1024):
        async def openai_reply(message):
            response = await self.async_client.chat.completions.create(
                        model=self.model,
                        messages=message,
                        temperature=temperature,
                        max_tokens=max_tokens,)
            return response.choices[0].message.content

        response_list = [openai_reply(message) for message in messages]
        return await asyncio.gather(*response_list)
    