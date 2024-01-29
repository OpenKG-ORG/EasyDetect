import yaml
from pipeline.openai_wrapper import *
from pipeline.claim_generate import * 
from pipeline.query_generate import *
from pipeline.tool_execute import *
from pipeline.verify import *

class Pipeline:
    def __init__(self):
        with open("pipeline/config/config.yaml", 'r', encoding='utf-8') as file:
            self.config = yaml.load(file, yaml.FullLoader)

        self.syncchat = SyncChat(model="gpt-4-1106-preview", config=self.config["openai"])
        self.asyncchat = AsyncChat(model="gpt-4-1106-preview", config=self.config["openai"])
        self.visionchat = SyncChat(model="gpt-4-vision-preview", config=self.config["openai"])

        self.claim_generator = ClaimGenerator(config=self.config,chat=self.syncchat)
        self.query_generator = QueryGenerator(config=self.config,chat=self.asyncchat)
        self.tool = Tool(config=self.config)
        self.verifier = Verifier(config=self.config, chat=self.visionchat)

    def run(self, text, image_path, type):
        response, claim_list = self.claim_generator.get_response(text=text)
        objects, attribute_ques_list, scenetext_ques_list, fact_ques_list = self.query_generator.get_response(claim_list=claim_list, type=type)
        object_res, attribue_res, text_res, fact_res = self.tool.execute(image_path=image_path,
                                                                        objects=objects,
                                                                        attribute_list=attribute_ques_list, 
                                                                        scenetext_list=scenetext_ques_list, 
                                                                        fact_list=fact_ques_list)
        response = self.verifier.get_response(type, object_res, attribue_res, text_res, fact_res, claim_list, image_path)
        return response,claim_list


