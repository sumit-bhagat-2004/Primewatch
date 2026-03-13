from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.schemas.watchlist import WatchlistItemCreate, WatchlistItemUpdate, WatchlistItemResponse
from app.crud.watchlist import (
    create_watchlist_item,
    get_user_watchlist_items,
    get_watchlist_item_by_id,
    update_watchlist_item,
    delete_watchlist_item,
    get_all_watchlist_items
)
from app.core.dependencies import get_current_user, get_current_admin
from app.models.models import User

router = APIRouter()


@router.post("/", response_model=WatchlistItemResponse, status_code=status.HTTP_201_CREATED)
def create_watchlist(
    watchlist_item: WatchlistItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new watchlist item for the current user.

    Args:
        watchlist_item: Watchlist item data
        current_user: The authenticated user
        db: Database session

    Returns:
        The created watchlist item
    """
    return create_watchlist_item(db=db, user_id=current_user.id, watchlist_item=watchlist_item)


@router.get("/", response_model=List[WatchlistItemResponse])
def get_my_watchlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all watchlist items for the current user.

    Args:
        current_user: The authenticated user
        db: Database session

    Returns:
        List of user's watchlist items
    """
    return get_user_watchlist_items(db=db, user_id=current_user.id)


@router.put("/{item_id}", response_model=WatchlistItemResponse)
def update_watchlist(
    item_id: UUID,
    watchlist_update: WatchlistItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a watchlist item (only owner can update).

    Args:
        item_id: Watchlist item UUID
        watchlist_update: Updated data
        current_user: The authenticated user
        db: Database session

    Returns:
        The updated watchlist item

    Raises:
        HTTPException: If item not found or user not authorized
    """
    # Get the item
    db_item = get_watchlist_item_by_id(db, item_id)

    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist item not found"
        )

    # Check ownership
    if db_item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this item"
        )

    # Update the item
    updated_item = update_watchlist_item(db, item_id, watchlist_update)
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_watchlist(
    item_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a watchlist item (owner or admin can delete).

    Args:
        item_id: Watchlist item UUID
        current_user: The authenticated user
        db: Database session

    Raises:
        HTTPException: If item not found or user not authorized
    """
    # Get the item
    db_item = get_watchlist_item_by_id(db, item_id)

    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist item not found"
        )

    # Check ownership or admin role
    from app.models.models import UserRole
    if db_item.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this item"
        )

    # Delete the item
    delete_watchlist_item(db, item_id)
    return None


# ============= Admin Endpoints =============

@router.get("/admin/all", response_model=List[WatchlistItemResponse])
def get_all_watchlists(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get all watchlist items across all users (admin only).

    Args:
        current_admin: The authenticated admin user
        db: Database session

    Returns:
        List of all watchlist items
    """
    return get_all_watchlist_items(db)
