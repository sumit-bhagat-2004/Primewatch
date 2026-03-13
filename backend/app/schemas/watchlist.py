from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


# ============= Watchlist Schemas =============

class WatchlistItemBase(BaseModel):
    """Base watchlist item schema with common fields."""
    token_symbol: str = Field(..., min_length=1, max_length=10, description="Cryptocurrency symbol (e.g., BTC, ETH)")
    target_price: float = Field(..., gt=0, description="Target price must be greater than 0")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes about this watchlist item")


class WatchlistItemCreate(WatchlistItemBase):
    """Schema for creating a new watchlist item."""
    pass


class WatchlistItemUpdate(BaseModel):
    """Schema for updating a watchlist item (all fields optional)."""
    token_symbol: Optional[str] = Field(None, min_length=1, max_length=10)
    target_price: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = Field(None, max_length=500)


class WatchlistItemResponse(WatchlistItemBase):
    """Schema for watchlist item response."""
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class WatchlistItemInDB(WatchlistItemResponse):
    """Schema for watchlist item in database."""

    class Config:
        from_attributes = True
