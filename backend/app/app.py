from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import sys

sys.path.append("./backend/core")
# sys.path.append("../core")
import generate_code
import voice_recognition

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="./frontend")


class CodeGeneration(BaseModel):
    query: str
    idioma: str


@app.get("/", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/traslate-to-code")
async def translating_to_code(traduccion_codigo: CodeGeneration):
    print(traduccion_codigo.dict())
    translate_to_code = traduccion_codigo.dict()
    text_spanish, text, decoded_code = generate_code.generate_text_to_code(
        translate_to_code["query"], translate_to_code["idioma"]
    )
    print(text_spanish, text, decoded_code)
    return {
        "textES": str(text_spanish),
        "textEN": str(text),
        "generateCode": str(decoded_code),
    }


# Audio en español a transcribir
@app.websocket("/listen-es")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Revisa que se tengan permisos de micrófono en el pc

    try:
        await websocket.receive_bytes()  # Hace que se imprima texto en frontend

        print(
            "Por favor empieza a hablar lo que quieres transcribir"
        )  # Esto es para consola, se puede quitar

        # Indica en pantalla que ya puede empezar a hablar
        await websocket.send_text(
            "Por favor empieza a hablar lo que quieres transcribir..."
        )
        # Se traduce lo hablado a texto
        audio_reconocido = voice_recognition.reconocimiento_audio("spanish")

        # Se envía el texto reconocido de vuelta
        await websocket.send_text(audio_reconocido)

        print(audio_reconocido)

    except Exception as e:
        raise Exception(f"Could not process audio: {e}")
    finally:
        await websocket.close()  # Se cierra


# Audio en inglés a transcribir
@app.websocket("/listen-en")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Revisa que se tengan permisos de micrófono en el pc

    try:
        await websocket.receive_bytes()  # Hace que se imprima texto en frontend

        print(
            "Start talking what you want to transcribe"
        )  # Esto es para consola, se puede quitar

        # Indica en pantalla que ya puede empezar a hablar
        await websocket.send_text("Please start talking what you want to transcribe...")
        # Se traduce lo hablado a texto
        audio_reconocido = voice_recognition.reconocimiento_audio("english")

        # Se envía el texto reconocido de vuelta
        await websocket.send_text(audio_reconocido)

        print(audio_reconocido)

    except Exception as e:
        raise Exception(f"Could not process audio: {e}")
    finally:
        await websocket.close()  # Se cierra


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)  # Prueba en el sistema
