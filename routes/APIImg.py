from fastapi import APIRouter, File, UploadFile
from os import environ as env
from helpers.Inter import Interprete
from typing import List
from threading import Thread
Img = APIRouter()

@Img.post('/imgs')
async def postImgsCompare(files: List[UploadFile] = File(...)):
    filesave = []
    for file in files:
        file_bytes = await file.read()
        filesave.append(file.filename)
        with open(f'./images/{file.filename}', 'wb') as f:
            f.write(file_bytes)
    imgReference = f'./images/{filesave.pop(0)}'
    results = [h.start() or h.join() or {"similitud" :h.similarity, "porcentaje":h.percent, "imagenes a comparar":h.images} for h in [Thread(target=Interprete, args=(imgReference, f'./images/{i}')) for i in filesave]]
    return results
