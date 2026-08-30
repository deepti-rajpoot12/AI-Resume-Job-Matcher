import asyncio
import logging
import sqlite3

from fastapi import APIRouter, HTTPException, status

from app.models.history import HistoryDetail, HistorySummary
from app.services import history as history_service

router = APIRouter(prefix="/api/history", tags=["history"])
logger = logging.getLogger(__name__)


@router.get("", response_model=list[HistorySummary])
async def list_history():
    try:
        return await asyncio.to_thread(history_service.list_history)
    except sqlite3.Error as error:
        logger.exception("History list failed")
        raise HTTPException(status_code=503, detail="Analysis history is unavailable.") from error


@router.get("/{analysis_id}", response_model=HistoryDetail)
async def get_history(analysis_id: int):
    item = await asyncio.to_thread(history_service.get_history, analysis_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis history item not found.")
    return item


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_history(analysis_id: int):
    if not await asyncio.to_thread(history_service.delete_history, analysis_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis history item not found.")
