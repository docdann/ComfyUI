import json
import os
import time
import random

import cv2
import numpy as np
import requests

from PIL import Image


URL = "http://127.0.0.1:8188/prompt"
INPUT_DIR = "C:\\Users\\dunde\\source\\repos\\ComfyUI\\input"
OUTPUT_DIR = "C:\\Users\\dunde\\source\\repos\\ComfyUI\\output"

cached_seed = 0

def get_latest_image(folder):
    files = os.listdir(folder)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
    latest_image = os.path.join(folder, image_files[-1]) if image_files else None
    return latest_image


def start_queue(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    requests.post(URL, data=data)


def generate_image():
    while True:
        
        cap = cv2.VideoCapture(0)  # Open the default camera

        ret, frame = cap.read()
        with open("workflows\\workflow_api.json", "r") as file_json:
            prompt = json.load(file_json)

            prompt["3"]["inputs"]["seed"] = random.randint(1, 1500000)
            global cached_seed
            if cached_seed == prompt["3"]["inputs"]["seed"]:
                return get_latest_image(OUTPUT_DIR)
            cached_seed = prompt["3"]["inputs"]["seed"]

            ret, frame = cap.read()

            image = Image.fromarray(frame)
            min_side = min(image.size)
            scale_factor = 720 / min_side
            new_size = (round(image.size[0] * scale_factor), round(image.size[1] * scale_factor))
            resized_image = image.resize(new_size)

            resized_image.save(os.path.join(INPUT_DIR, "test_api.jpg"))

            previous_image = get_latest_image(OUTPUT_DIR)
    
            start_queue(prompt)
            time.sleep(6)
            
            if not ret:
                break



generate_image()