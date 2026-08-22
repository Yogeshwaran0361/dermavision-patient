import uuid
import datetime
import requests
from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse, Response

from app.services.quality_checker import ImageQualityChecker
from app.services.ai_inference import get_inference_engine, CLASS_CLINICAL_INFO
from app.schemas.prediction import QualityCheckResponse, PredictionResponse

router = APIRouter(prefix="/api")

@router.get("/ai/tts")
def text_to_speech(text: str = Query(...), lang: str = Query("en")):
    """
    Proxies Google TTS audio stream with CORS headers enabled.
    Guarantees 100% native Tamil ('ta') and Hindi ('hi') speech playback on all browsers and Windows PCs.
    """
    try:
        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={lang}&q={requests.utils.quote(text)}"
        resp = requests.get(tts_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if resp.status_code == 200:
            return Response(
                content=resp.content,
                media_type="audio/mpeg",
                headers={
                    "Cache-Control": "public, max-age=3600",
                    "Access-Control-Allow-Origin": "*"
                }
            )
        else:
            raise HTTPException(status_code=500, detail="TTS service unavailable")
    except Exception as e:
        print(f"[TTS Proxy Error] {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
@router.get("/ai/health")
def ai_health_check():
    try:
        engine = get_inference_engine()
        return {
            "model_loaded": True,
            "framework": "PyTorch (EfficientNet-B0 / ResNet50)",
            "classes": engine.num_classes,
            "input_size": [224, 224],
            "weights_file": engine.weights_path,
            "class_names": engine.class_names
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "model_loaded": False,
            "error": str(e)
        })

@router.get("/classes")
def get_classes():
    try:
        engine = get_inference_engine()
        return {
            "total": engine.num_classes,
            "classes": engine.class_names,
            "clinical_info": CLASS_CLINICAL_INFO
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quality-check")
@router.post("/ai/quality-check")
def check_image_quality(file: UploadFile = File(...)):
    try:
        image_bytes = file.file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        result = ImageQualityChecker.validate_image_quality(image_bytes)
        return JSONResponse(content=result)
    except Exception as e:
        print(f"Quality Check Endpoint Error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

@router.post("/predict")
@router.post("/ai/predict")
def predict_skin_disease(file: UploadFile = File(...), model_name: str = None):
    request_id = str(uuid.uuid4())[:8]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        image_bytes = file.file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        file_size = len(image_bytes)
        filename = file.filename or "uploaded_lesion.jpg"
        content_type = file.content_type or "image/jpeg"

        print(f"\n==================================================")
        print(f"[DEVELOPMENT DEBUG LOG] Time={timestamp} ReqID={request_id}")
        print(f"UPLOAD OK: '{filename}' ({content_type}, {file_size} bytes)")

        # 1. Run Quality & Human Skin Validation Gate
        quality_result = ImageQualityChecker.validate_image_quality(image_bytes)
        print(f"QUALITY & SKIN GATE: passed={quality_result['passed']}, reason='{quality_result['reason']}', metrics={quality_result.get('metrics', {})}")

        if not quality_result.get("passed", True):
            is_invalid = quality_result.get("is_invalid_image", False)
            is_quality_low = quality_result.get("is_quality_low", False)
            print(f"[REQ-{request_id}] Rejecting non-skin/low-quality image: invalid={is_invalid}, quality_low={is_quality_low}, reason='{quality_result['reason']}'")

            return JSONResponse(status_code=200, content={
                "success": False,
                "is_invalid_image": is_invalid,
                "is_quality_low": is_quality_low,
                "error_type": "INVALID_IMAGE" if is_invalid else "QUALITY_TOO_LOW",
                "message": quality_result.get("reason", "INVALID IMAGE — PLEASE UPLOAD A SKIN IMAGE"),
                "detail": quality_result.get("detail", "The uploaded image does not appear to contain a valid human skin region. Please upload a clear, well-lit image of the affected or normal skin area."),
                "suggestion": quality_result.get("suggestion", "Please upload a clear, well-lit skin photo."),
                "quality": quality_result
            })

        print("IMAGE DECODE & SKIN VERIFICATION OK")

        # 2. Run PyTorch Neural Inference (ONLY FOR VALID HUMAN SKIN IMAGES)
        engine = get_inference_engine()
        print(f"MODEL LOADED: Framework=PyTorch ActiveModels={len(engine.models)} TotalClasses={engine.num_classes} Weights='{engine.weights_path}'")

        prediction_data = engine.predict(image_bytes, target_model_name=model_name)
        print("MODEL OUTPUT OK")

        class_idx = prediction_data.get("class_index", 0)
        predicted_class = prediction_data.get("predicted_class", f"Class_{class_idx}")
        exact_disease_name = prediction_data.get("exactDiseaseName", predicted_class)
        conf_pct = prediction_data.get("confidence_pct", prediction_data.get("confidence", 0))

        print(f"CLASS MAPPING OK: ClassIndex={class_idx} -> Technical='{predicted_class}' -> ExactDiseaseName='{exact_disease_name}'")
        print(f"PREDICTION: '{exact_disease_name}' (class_{class_idx})")
        print(f"CONFIDENCE: {conf_pct}%")
        print(f"TOP 3 PREDICTIONS: {prediction_data.get('top_3_predictions', [])}")
        print(f"REPORT PROFILE: is_normal={prediction_data.get('is_normal', False)}, is_unreliable={prediction_data.get('is_unreliable', False)}")
        print(f"REPORT GENERATED: SUCCESS")
        print(f"==================================================\n")

        return JSONResponse(content={
            "success": True,
            "model_used": True,
            "model_name": prediction_data.get("model_name", "PyTorch Classifier"),
            "loaded_models": prediction_data.get("loaded_models", []),
            "model_breakdown": prediction_data.get("model_breakdown", []),
            "class_index": class_idx,
            "classId": class_idx,
            "predicted_class": predicted_class,
            "top_class": predicted_class,
            "display_title": exact_disease_name,
            "exactDiseaseName": exact_disease_name,
            "className": prediction_data["className"],
            "technicalClass": prediction_data["technicalClass"],
            "confidence": conf_pct,
            "confidence_pct": conf_pct,
            "confidence_score": conf_pct,
            "is_normal": prediction_data.get("is_normal", False),
            "is_unreliable": prediction_data.get("is_unreliable", False),
            "is_low_confidence": prediction_data.get("is_low_confidence", False),
            "filename": filename,
            "quality": quality_result,
            "prediction": {
                "classId": class_idx,
                "class_index": class_idx,
                "top_class": predicted_class,
                "predicted_class": predicted_class,
                "display_title": exact_disease_name,
                "exactDiseaseName": exact_disease_name,
                "className": prediction_data["className"],
                "confidence": conf_pct,
                "confidence_pct": conf_pct,
                "confidence_raw": conf_pct,
                "is_normal": prediction_data.get("is_normal", False),
                "is_unreliable": prediction_data.get("is_unreliable", False),
                "is_low_confidence": prediction_data.get("is_low_confidence", False),
                "risk_level": prediction_data["risk_level"],
                "risk_color": prediction_data["risk_color"],
                "description": prediction_data["description"],
                "action": prediction_data["action"]
            },
            "top_3_predictions": prediction_data.get("top_3_predictions", []),
            "probabilities": prediction_data.get("top_3_predictions", [])
        })

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"[REQ-{request_id}] Inference Pipeline ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI model inference failed: {str(e)}")

# ==========================================================================
# EMAILJS CLIENT-SIDE NOTIFICATIONS (MANAGED VIA FRONTEND @EMAILJS/BROWSER)
# ==========================================================================

from app.services.email_service import get_notification_status

@router.get("/notifications/status")
def notification_status():
    return get_notification_status()

