### --------- External Imports --------- ###
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Query, status


### --------- Internal Imports --------- ###
from database.history_operations import (
    get_all_analyses,
    get_single_analysis,
    search_analyses,
    save_analysis,
    delete_analysis,
)


### --------- Routes --------- ###
history_router = APIRouter(
    prefix="/api/v1/history",
    tags=["Analysis History"],
)


### --------- Pydantic Models --------- ###
class AnalysisHistoryResponse(BaseModel):
    id: int
    text: str
    sentiment_label: str
    confidence_score: float
    positive_score: float
    negative_score: float
    created_at: datetime


class AnalysisHistoryListResponse(BaseModel):
    total: int
    analyses: List[AnalysisHistoryResponse]


class SaveHistoryRequest(BaseModel):
    text: str
    label: str
    confidence: float
    positive_score: Optional[float] = None
    negative_score: Optional[float] = None


### --------- API Endpoint --------- ###
@history_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=AnalysisHistoryListResponse
)
async def get_history(
    limit: int = Query(
        default=20, ge=1, le=50, description="Number of items to retrieve"
    ),
):
    """Get all analysis history with pagination"""
    analyses = get_all_analyses(limit=limit)

    if not analyses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis history not found",
        )

    return AnalysisHistoryListResponse(
        total=len(analyses),
        analyses=[AnalysisHistoryResponse(**analysis) for analysis in analyses],
    )


# @history_router.get(
#     "/{analysis_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=AnalysisHistoryResponse,
# )
# async def get_single_analysis(analysis_id: int):
#     """Get single analysis by ID"""
#     analysis = get_single_analysis(analysis_id=analysis_id)

#     if not analysis:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Analysis history not found",
#         )

#     return AnalysisHistoryResponse(**analysis)


@history_router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=AnalysisHistoryListResponse,
)
async def search_history(
    search_query: str = Query(default="", min_length=1),
    limit: int = Query(default=20, ge=1, le=50),
):
    """Search through analysis history"""
    analyses = search_analyses(search_text=search_query, limit=limit)

    if not analyses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis history not found",
        )

    return AnalysisHistoryListResponse(
        total=len(analyses),
        analyses=[AnalysisHistoryResponse(**analysis) for analysis in analyses],
    )


@history_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=AnalysisHistoryResponse
)
async def save_history(request: SaveHistoryRequest):
    """Save analysis to history"""
    try:
        analysis = save_analysis(
            text=request.text,
            label=request.label,
            confidence=request.confidence,
            positive_score=request.positive_score,
            negative_score=request.negative_score,
        )

        return AnalysisHistoryResponse(**analysis)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving analysis: {e}",
        )


@history_router.delete(
    "/{analysis_id}", status_code=status.HTTP_200_OK, response_model=bool
)
async def delete_history(analysis_id: int):
    """Delete specific analysis by ID"""
    try:
        return delete_analysis(analysis_id=analysis_id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting analysis: {e}",
        )
