import os
import io
import numpy as np
from PIL import Image
try:
    import tensorflow as tf
except ImportError:
    tf = None
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import database, models, schemas

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Poultry Disease Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Model
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'best_model.keras')
try:
    if tf:
        model = tf.keras.models.load_model(MODEL_PATH)
        print(f"Model loaded successfully from {MODEL_PATH}")
    else:
        print("TensorFlow not installed. Model will not be loaded.")
        model = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Placeholder class names (update based on training)
CLASS_NAMES = ["Coccidiosis", "Healthy", "New Castle Disease", "Salmonella"]

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != "RGB":
        image = image.convert("RGB")
    # Resize assuming 224x224 input
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.post("/predict", response_model=schemas.PredictionResponse)
async def predict_disease(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    image_bytes = await file.read()
    
    # Preprocess and Predict
    img_array = preprocess_image(image_bytes)
    
    if model:
        predictions = model.predict(img_array)
        class_idx = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        if class_idx < len(CLASS_NAMES):
            predicted_class = CLASS_NAMES[class_idx]
        else:
            predicted_class = f"Class {class_idx}"
    else:
        # Fallback if model fails to load
        predicted_class = "Unknown (Model Error)"
        confidence = 0.0

    # Save to DB
    db_prediction = models.PredictionHistory(
        filename=file.filename,
        predicted_disease=predicted_class,
        confidence_score=confidence
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    return db_prediction


# ==================== Flock Endpoints ====================

@app.post("/flocks", response_model=schemas.FlockResponse)
async def create_flock(flock: schemas.FlockCreate, db: Session = Depends(database.get_db)):
    """إنشاء قطيع جديد"""
    db_flock = models.Flock(**flock.dict())
    db.add(db_flock)
    db.commit()
    db.refresh(db_flock)
    return db_flock


@app.get("/flocks/{flock_id}", response_model=schemas.FlockResponse)
async def get_flock(flock_id: int, db: Session = Depends(database.get_db)):
    """الحصول على بيانات قطيع معين"""
    flock = db.query(models.Flock).filter(models.Flock.id == flock_id).first()
    if not flock:
        raise HTTPException(status_code=404, detail="Flock not found")
    return flock


@app.get("/flocks", response_model=list[schemas.FlockResponse])
async def get_all_flocks(db: Session = Depends(database.get_db)):
    """الحصول على جميع القطعان"""
    flocks = db.query(models.Flock).all()
    return flocks


@app.put("/flocks/{flock_id}", response_model=schemas.FlockResponse)
async def update_flock(flock_id: int, flock_update: schemas.FlockUpdate, db: Session = Depends(database.get_db)):
    """تحديث بيانات القطيع"""
    db_flock = db.query(models.Flock).filter(models.Flock.id == flock_id).first()
    if not db_flock:
        raise HTTPException(status_code=404, detail="Flock not found")
    
    update_data = flock_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_flock, key, value)
    
    db.commit()
    db.refresh(db_flock)
    return db_flock


@app.delete("/flocks/{flock_id}")
async def delete_flock(flock_id: int, db: Session = Depends(database.get_db)):
    """حذف قطيع"""
    db_flock = db.query(models.Flock).filter(models.Flock.id == flock_id).first()
    if not db_flock:
        raise HTTPException(status_code=404, detail="Flock not found")
    
    db.delete(db_flock)
    db.commit()
    return {"message": "Flock deleted successfully"}


@app.get("/predictions", response_model=list[schemas.PredictionResponse])
async def get_all_predictions(db: Session = Depends(database.get_db)):
    """الحصول على جميع التشخيصات السابقة"""
    predictions = db.query(models.PredictionHistory).order_by(models.PredictionHistory.timestamp.desc()).all()
    return predictions
