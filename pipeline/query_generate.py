import json
import yaml
import copy
import asyncio
from nltk.corpus import wordnet

class QueryGenerator:
    def __init__(self, config, chat):
        with open(config["prompts"]["query_generate"],"r",encoding='utf-8') as file:
            self.prompt = yaml.load(file, yaml.FullLoader)
        self.chat = chat
        
    def objects_extract(self, claim_list):
        user_prompt = self.prompt[self.type]["object"]["user"].format(claims=claim_list)
        message = [[
                                {"role": "system", "content": self.prompt[self.type]["object"]["system"]},
                                {"role": "user", "content": user_prompt}
                        ],]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(self.chat.get_response(messages=message))

        try:
            response = json.loads(response[0])
        except Exception as e:
            print(e)
            
        objects = set(())
        for key in response:
            object_list = response[key].split(".")
            response[key] = object_list
            for object in object_list:
                if object != "none":
                    objects.add(object)
    
        objects = ".".join([object for object in list(objects)])
        return response, objects
    
    def get_hypernyms(self, word):
        synsets = wordnet.synsets(word)
        hypernyms = []

        for synset in synsets:
            for hypernym in synset.hypernyms():
                hypernyms.extend(hypernym.lemma_names())

        hypernyms = list(set(hypernyms))
        hypernyms = ".".join([hypernym for hypernym in hypernyms])
        return hypernyms
    
    def remove_hypernyms(self, objects):
        hypernyms_dict = {}
        for object in objects:
            hypernyms = self.get_hypernyms(object)
            hypernyms_dict[object] = hypernyms
        
        backup = copy.deepcopy(objects)
        for object in objects:
            hypernyms_list = []
            for key in hypernyms_dict:
                if key != object:
                    hypernyms_list.append(hypernyms_dict[key])
            hypernyms_list = ".".join([hypernym for hypernym in hypernyms_list])
            if object in hypernyms_list:
                backup.remove(object)
                
        objects = ".".join([object for object in backup])
        return objects
    
    def filter(self, res, object_list):
        attribute_ques_list = json.loads(res[0])
        scenetext_ques_list = json.loads(res[1])
        fact_ques_list = json.loads(res[2])
        objects = set(())
        for idx, key in enumerate(fact_ques_list):
            if fact_ques_list[key][0] != "none":
                object_list[idx] = "none"
                attribute_ques_list[key] = ["none"]
                scenetext_ques_list[key] = ["none"]
            else:
                for object in object_list[key]:
                    if object != "none":
                        objects.add(object)

        objects = self.remove_hypernyms(objects)
        return attribute_ques_list, scenetext_ques_list, fact_ques_list, objects
            
    def get_response(self, claim_list, type):
        self.type = type
        object_list, objects = self.objects_extract(claim_list=claim_list)
        self.message_list = [
                [{"role": "system", "content": self.prompt[type]["attribute"]["system"]}, {"role": "user", "content": self.prompt[type]["attribute"]["user"].format(objects=objects,claims=claim_list)}],
                [{"role": "system", "content": self.prompt[type]["scene-text"]["system"]}, {"role": "user", "content": self.prompt[type]["scene-text"]["user"].format(claims=claim_list)}],
                [{"role": "system", "content": self.prompt[type]["fact"]["system"]}, {"role": "user", "content": self.prompt[type]["fact"]["user"].format(claims=claim_list)}]
            ]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = loop.run_until_complete(self.chat.get_response(messages=self.message_list))
        if self.type == "image-to-text":
            attribute_ques_list, scenetext_ques_list, fact_ques_list, objects = self.filter(res, object_list)
        else:
            attribute_ques_list, scenetext_ques_list, fact_ques_list = json.loads(res[0]), json.loads(res[1]), json.loads(res[2])
                
        return objects, attribute_ques_list, scenetext_ques_list, fact_ques_list