import yaml
import base64


class Verifier:
    def __init__(self, config, chat):
        with open(config["prompts"]["verify"],"r",encoding='utf-8') as file:
            self.prompt = yaml.load(file, yaml.FullLoader)
        self.chat = chat
        
    def get_response(self, type, object_res, attribue_res, text_res, fact_res, claim_list, image_path):
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        input = '''
                Here is the object detection expert model's result:
                {object}

                Here is the scene text recognition expert model's result:
                {text}
                
                Here is the attribute information:
                {attribute}

                Here is the external knowledge:
                {fact}

                Here is the claim list:
                {claims}

                Output: 
            '''
            
        object_det_res, text_det_res = "", ""
        for object_name, box in zip(object_res["phrases"], object_res["boxes"]):
            object_det_res += "{} {} \n".format(object_name, str(box)) 
                
        if text_res != None:
            for text_name, box in zip(text_res["phrases"], text_res["boxes"]):
                text_det_res += text_name + " " + str(box) +  "\n" 
        else:
            text_det_res = "none information"
            
        if type == "image-to-text":
            img1 = encode_image("pipeline/examples/sandbeach.jpg")
            img2 = encode_image("pipeline/examples/football.jpg")
        else:
            img1 = encode_image("pipeline/examples/animal.jpg")
            img2 = encode_image("pipeline/examples/ball.jpg")
        base64_source_image = encode_image(image_path)
        content = [
                    {"type": "text", "text": self.prompt[type]["user"]},
                    {"type": "image_url","image_url": f"data:image/jpeg;base64,{img1}"},
                    {"type": "text", "text": self.prompt[type]["example1"]},
                    {"type": "image_url","image_url": f"data:image/jpeg;base64,{img2}"},
                    {"type": "text", "text": self.prompt[type]["example2"]},
                    {"type": "image_url","image_url": f"data:image/jpeg;base64,{base64_source_image}"},
                    {"type": "text", "text": input.format(object=object_det_res,text=text_det_res,attribute=attribue_res,fact=fact_res,claims=claim_list)}
                ]

        
        message = [
                {
                    'role': 'system',
                    'content': self.prompt[type]["system"]
                },
                {
                    "role": "user",
                    "content": content,
                }
            ]
            
        response = self.chat.get_response(message=message)
        return response
        