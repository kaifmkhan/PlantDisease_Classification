import os
from fastapi import FastAPI, File, UploadFile, HTTPException  # web server
import uvicorn  # gateway
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from pydantic import BaseModel
import pickle

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# model_path = os.path.abspath("../saved_models/1")
MODEL = tf.keras.models.load_model("./saved_models/2")
CLASS_NAMES = ['BellPepper__Bacterial_spot',
               'BellPepper___healthy',
               'Potato___Early_blight',  # 2
               'Potato___Late_blight',
               'Potato___healthy',
               'Tomato_Bacterial_spot',
               'Tomato_Early_blight',
               'Tomato_Late_blight',
               'Tomato_Leaf_Mold',
               'Tomato_Septoria_leaf_spot',
               'Tomato_Spider_mites_Two_spotted_spider_mite',
               'Tomato__Target_Spot',
               'Tomato__Tomato_YellowLeaf__Curl_Virus',
               'Tomato__Tomato_mosaic_virus',
               'Tomato_healthy']


@app.get("/ping")
async def ping():
    return "HELLO"


def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        if not file.content_type == 'image/jpeg':
            raise ValueError(
                "Invalid file format. Only JPEG images are supported.")
        image = read_file_as_image(await file.read())
        img_batch = np.expand_dims(image, 0)

        predictions = MODEL.predict(img_batch)

        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]  # 2 - highest
        confidence = np.max(predictions[0])  # 2

        return {
            'class': predicted_class,
            'confidence': float(confidence)
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8010)
