import base64
from pipeline.openai_wrapper import *
from pipeline.tool.detect import *
from pipeline.tool.ocr import *
from pipeline.tool.google_serper import *

class Tool:
    def __init__(self, config):
        self.config = config
        self.detector = DetectModel(config=self.config)
        self.ocr = OCRModel(config=self.config)
        self.visionchat = SyncChat(model="gpt-4-vision-preview",config=self.config["openai"])
        self.search = GoogleSerperAPIWrapper(config=self.config)
        
    def get_object_res(self, image_path, objects):
        object_res = self.detector.execute(image_path=image_path,
                                           content=objects,
                                           box_threshold=self.config["tool"]["detect"]["BOX_TRESHOLD"], 
                                           text_threshold=self.config["tool"]["detect"]["TEXT_TRESHOLD"],
                                           save_path=None) 
        return object_res
        
    def get_ocr_res(self, image_path, scenetext_list):
        use_ocr = False
        for key in scenetext_list:
            if scenetext_list[key][0] != "none":
                use_ocr = True  
        ocr_res = None
        if use_ocr:  
            ocr_res = self.detector.execute(image_path=image_path,
                                             content=self.config["tool"]["ocr"]["content"],
                                             box_threshold=self.config["tool"]["ocr"]["BOX_TRESHOLD"], 
                                             text_threshold=self.config["tool"]["ocr"]["TEXT_TRESHOLD"],
                                             save_path=self.config["tool"]["ocr"]["cachefiles_path"])
            
            ocr_res["phrases"] = self.ocr.execute(image_path_list=ocr_res["save_path"])
        return ocr_res
    
    def get_attribute_res(self, image_path, attribute_list):
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        queries = ""
        cnt = 1
        for key in attribute_list:
            if attribute_list[key][0] != "none":
                for query in attribute_list[key]:
                    queries += str(cnt) + "." + query + "\n"
                    cnt += 1
        if queries == "":
            attribue_res = "none information"
        else:
            img = encode_image(image_path)
            message = [{"role": "user","content": [{"type": "image_url","image_url": f"data:image/jpeg;base64,{img}"},{"type": "text", "text": queries}]}]
            attribue_res = self.visionchat.get_response(message=message)
        return attribue_res
    
    def get_fact_res(self, fact_list):
        fact_res = ""
        cnt = 1
        for key in fact_list:
            if fact_list[key][0] != "none": 
                evidences = self.search.execute(content=str(fact_list[key]))
                for evidence in evidences:
                    fact_res += str(cnt) + "." + evidence + "\n"
                    cnt += 1
        if fact_res == "":
            fact_res = "none information"
        return fact_res
        
    def execute(self, image_path, objects, attribute_list, scenetext_list, fact_list):
        object_res = self.get_object_res(image_path, objects)
        attribue_res = self.get_attribute_res(image_path, attribute_list)
        ocr_res = self.get_ocr_res(image_path, scenetext_list)
        fact_res = self.get_fact_res(fact_list)
        return object_res, attribue_res, ocr_res, fact_res



            
            
            
   