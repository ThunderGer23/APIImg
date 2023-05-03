from fastapi import FastAPI
from routes.APIImg import Img
from docs.docs import tags_metadata
from os import environ as env
from notigram import ping


TOKEN='daa39d53-6283-47a1-b945-b7ee6528dde0'

ping(TOKEN, 'Aquí APIImg Listo!')
app = FastAPI(
    title= "Someone title :v/ vrgs",
    description= "Aquí una descripción chingona que nadie va leer nunca jámas a menos que esto falle o quieran una actualización >:'v, desgraciados flojos, lean la documentación!!, está hecha con mis lagrimas e.e",
    version= "1.1.0",
    openapi_tags= tags_metadata
)

app.include_router(Img)