### --------- External Imports --------- ###
from fastapi import APIRouter, HTTPException, status
from transformers import pipeline
from pydantic import BaseModel

### --------- Internal Imports --------- ###
from database.history_operations import save_analysis

### --------- Routes --------- ###
classify_router = APIRouter(
    prefix="/api/v1",
    tags=["Text Classifier"],
)


### --------- Pydantic Models --------- ###
class ClassifyRequest(BaseModel):
    text: str


class ClassifyResponse(BaseModel):
    text: str
    label: str
    score: float


### --------- Functions --------- ###
# Handle text classification
def text_classifier(text: str):
    classifier_pipeline = pipeline(
        task="text-classification",
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    )
    result = classifier_pipeline(text)
    return result


@classify_router.post(
    "/classify", response_model=ClassifyResponse, status_code=status.HTTP_200_OK
)
async def classify(request: ClassifyRequest) -> ClassifyResponse:
    if not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Text is required"
        )
    try:
        # Get text classification result
        result = text_classifier(request.text)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing text",
            )

        label = result[0]["label"]
        score = result[0]["score"]

        # Auto save to history
        analysis = save_analysis(
            text=request.text,
            label=label,
            confidence=score,
            positive_score=score if label == "POSITIVE" else 1 - score,
            negative_score=score if label == "NEGATIVE" else 1 - score,
        )

        print(f"Analysis saved to history: {analysis['id']}")

        # Return response
        return ClassifyResponse(
            text=request.text,
            label=result[0]["label"],
            score=round(result[0]["score"], 4),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
