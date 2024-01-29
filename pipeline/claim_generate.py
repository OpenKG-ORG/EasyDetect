import json
import yaml

class ClaimGenerator:
    def __init__(self, config, chat):
        with open(config["prompts"]["claim_generate"],"r",encoding='utf-8') as file:
            self.prompt = yaml.load(file, yaml.FullLoader)
        self.chat = chat
    
    def get_response(self, text):
        user_prompt = self.prompt["user"].format(text=text)
        message = [
                            {"role": "system", "content": self.prompt["system"]},
                            {"role": "user", "content": user_prompt}
                       ]
        response = self.chat.get_response(message=message)
        try:
            response = json.loads(response)
        except Exception as e:
            print(e)
            
        claim_list = []
        cnt = 0
        for seg in response:
            for cla in seg["claims"]:
                cnt=(lambda x:x+1)(cnt)
                claim_list.append("claim{}: {}".format(str(cnt), cla["claim"]))
        claim_list = "\n".join([claim for claim in claim_list])
        return response, claim_list


