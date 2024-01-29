import time
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
        time1 = time.time()
        response, claim_list = self.claim_generator.get_response(text=text)
        time2 = time.time()    
        objects, attribute_ques_list, scenetext_ques_list, fact_ques_list = self.query_generator.get_response(claim_list=claim_list, type=type)
        time3 = time.time()
        print(objects)
        print(attribute_ques_list)
        print(scenetext_ques_list)
        print(fact_ques_list)

        object_res, attribue_res, text_res, fact_res = self.tool.execute(image_path=image_path,
                                                                        objects=objects,
                                                                        attribute_list=attribute_ques_list, 
                                                                        scenetext_list=scenetext_ques_list, 
                                                                        fact_list=fact_ques_list)
        time4 = time.time()
        response = self.verifier.get_response(type, object_res, attribue_res, text_res, fact_res, claim_list, image_path)
        time5 = time.time()
        print("claim generate time:" + str(time2-time1))
        print("query generate time:" + str(time3-time2))
        print("tool execute time:" + str(time4-time3))
        print("judge time:" + str(time5-time4))
        print(fact_res)
        print("================")
        return response,claim_list
    
if __name__ == '__main__':
    text = "A person is cutting a birthday cake with two red candles that spell out \"21\". The surface of the cake is round, and there is a balloon in the room. The person is using a silver knife to cut the cake."
    image_path = "/newdisk3/wcx/val2014/COCO_val2014_000000297425.jpg"
    pipeline = Pipeline()
    response, claim_list = pipeline.run(text, image_path, "image-to-text")


