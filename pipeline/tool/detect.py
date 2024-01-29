import yaml
import torch
import os
import shortuuid
import numpy as np
from PIL import Image
from torchvision.ops import box_convert
from pipeline.tool.ocr import *
from pipeline.GroundingDINO.groundingdino.util.inference import load_model, load_image, predict

class DetectModel:
    def __init__(self, config):
        self.config = config
        self.model = load_model(self.config["tool"]["detect"]["groundingdino_config"], 
                                self.config["tool"]["detect"]["model_path"], 
                                device=self.config["tool"]["detect"]["device"])

        
    def execute(self, image_path, content, box_threshold, text_threshold,save_path):
        image_source, image = load_image(image_path)
        boxes, _, phrases = predict(model=self.model,image=image,caption=content,box_threshold=box_threshold,text_threshold=text_threshold,device=self.config["tool"]["detect"]["device"])
        h, w, _ = image_source.shape
        torch_boxes = boxes * torch.Tensor([w, h, w, h])
        xyxy = box_convert(boxes=torch_boxes, in_fmt="cxcywh", out_fmt="xyxy").numpy()
        normed_xyxy = np.around(np.clip(xyxy / np.array([w, h, w, h]), 0., 1.), 3).tolist()
        result = {"boxes":normed_xyxy, "phrases":phrases, "save_path":[]}
        if save_path != None:
            dir_name = image_path.split("/")[-1][:-4]
            cache_dir = save_path + dir_name
            os.makedirs(cache_dir, exist_ok=True)
            image_path_list = []
            for box, norm_box in zip(xyxy, normed_xyxy):
                # filter out too small text
                if (norm_box[2]-norm_box[0]) * (norm_box[3]-norm_box[1]) < self.config["tool"]["detect"]["AREA_THRESHOLD"]:
                    continue
                crop_id = shortuuid.uuid()
                crop_img = Image.fromarray(image_source).crop(box)
                crop_path = os.path.join(cache_dir, f"{crop_id}.jpg")
                crop_img.save(crop_path)
                image_path_list.append(crop_path)
            result["save_path"] = image_path_list
        
        return result