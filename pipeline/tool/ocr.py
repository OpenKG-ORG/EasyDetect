import numpy as np
from PIL import Image
from pipeline.mmocr.mmocr.apis.inferencers import MMOCRInferencer

class OCRModel:
    def __init__(self, config):    
        self.config = config
        self.mmocr_inferencer = MMOCRInferencer(
                det=self.config["tool"]["ocr"]["dbnetpp_config"],
                det_weights=self.config["tool"]["ocr"]["dbnetpp_path"],
                rec=self.config["tool"]["ocr"]["maerec_config"],
                rec_weights=self.config["tool"]["ocr"]["maerec_path"],
                device=self.config["tool"]["ocr"]["device"])
        
    def get_single_result(self, image_path):
        data = Image.open(image_path).convert("RGB")
        img = np.array(data)
        self.mmocr_inferencer.mode = 'rec'
        result = self.mmocr_inferencer(img, return_vis=True)
        result = result['predictions'][0]
        rec_text = result['rec_texts'][0]
        rec_score = result['rec_scores'][0]
        out_results = f'pred: {rec_text} \n score: {rec_score:.2f}'
        return out_results.split("\n")[0][6:]

    def execute(self, image_path_list):
        ocr_det_res = []
        for image_path in image_path_list:
            res = self.get_single_result(image_path)
            ocr_det_res.append(res)
        return ocr_det_res