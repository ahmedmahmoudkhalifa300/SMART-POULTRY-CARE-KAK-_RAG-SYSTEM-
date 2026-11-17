"""
FastAPI routes for the image-based disease diagnosis service.
"""

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.core.logger import get_logger
from app.vision.explainer import DiagnosisExplainer

logger = get_logger(__name__)
router = APIRouter(prefix="/image", tags=["image"])

_explainer = None


def get_explainer():
    global _explainer
    if _explainer is None:
        from app.api.chat import get_pipeline
        # Get the warmed-up pipeline (will wait if needed, thread-safe)
        warmed_up_pipeline = get_pipeline()
        _explainer = DiagnosisExplainer(rag_pipeline=warmed_up_pipeline)
    return _explainer


class DiagnosisResponse(BaseModel):
    disease: str
    confidence: float
    explanation: str
    sources: list[dict]
    all_probabilities: dict


@router.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_image(file: UploadFile = File(...)) -> DiagnosisResponse:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload an image.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    try:
        explainer = get_explainer()
        result = explainer.diagnose_and_explain(file_bytes)

        try:
            from app.database.history import log_diagnosis
            log_diagnosis(result["disease"], result["confidence"], result["explanation"])
        except Exception as db_exc:
            logger.warning("Failed to log diagnosis to database: %s", db_exc)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("Image diagnosis failed")
        raise HTTPException(status_code=500, detail="Diagnosis failed.") from exc

    return DiagnosisResponse(
        disease=result["disease"],
        confidence=result["confidence"],
        explanation=result["explanation"],
        sources=result["sources"],
        all_probabilities=result["all_probabilities"],
    )
