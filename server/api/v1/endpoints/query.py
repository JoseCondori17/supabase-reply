from fastapi import APIRouter, HTTPException, UploadFile, File
from pydub import AudioSegment
from pathlib import Path
import uuid

from server.api.v1.dependencies import PinPomDep
from server.api.v1.model.query import Query

router = APIRouter()

UPLOAD_DIR = Path("uploads_musics")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/sql", status_code=201)
async def query_sql(pp_service: PinPomDep, body: Query):
    try:
        result = pp_service.execute(body.query)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        error_msg = f"Error obtaining databases: {str(e)}"
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": error_msg
            }
        )
    
@router.post("/top/{music_id}", status_code=201)
async def query_sql(pp_service: PinPomDep, music_id: int):
    try:
        result = pp_service.get_top_music(music_id)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        error_msg = f"Error obtaining databases: {str(e)}"
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": error_msg
            }
        )
    
@router.post("/upload-music", status_code=201)
async def upload_music(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith((".mp3", ".mpeg")):
            raise HTTPException(status_code=400, detail="File format not allowed")

        file_path = UPLOAD_DIR / file.filename

        # save in server
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
            
        return {
            "success": True,
            "data": str(file_path)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e)
            }
        )
    

@router.post("/record-audio", status_code=201)
async def record_audio(file: UploadFile = File(...)):
    try:
        allowed_extensions = (".webm", ".ogg")
        ext = Path(file.filename).suffix.lower()

        if ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Unsupported audio format")

        original_filename = f"{uuid.uuid4().hex}{ext}"
        input_path = UPLOAD_DIR / original_filename

        with open(input_path, "wb") as buffer:
            buffer.write(await file.read())

        if input_path.stat().st_size == 0:
            raise HTTPException(status_code=400, detail="Empty audio file received")

        audio = AudioSegment.from_file(input_path)
        output_path = input_path.with_suffix(".mp3")
        audio.export(output_path, format="mp3", bitrate="192k")

        input_path.unlink(missing_ok=True)

        return {
            "success": True,
            "data": str(output_path)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e)
            }
        )