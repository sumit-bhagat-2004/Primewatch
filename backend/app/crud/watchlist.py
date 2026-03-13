from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.models.models import WatchlistItem
from app.schemas.watchlist import WatchlistItemCreate, WatchlistItemUpdate


def create_watchlist_item(
    db: Session,
    user_id: UUID,
    watchlist_item: WatchlistItemCreate
) -> WatchlistItem:
    """
    Create a new watchlist item for a user.

    Args:
        db: Database session
        user_id: Owner's user ID
        watchlist_item: Watchlist item data

    Returns:
        The created watchlist item
    """
    db_item = WatchlistItem(
        user_id=user_id,
        token_symbol=watchlist_item.token_symbol.upper(),  # Normalize to uppercase
        target_price=watchlist_item.target_price,
        notes=watchlist_item.notes
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_user_watchlist_items(db: Session, user_id: UUID) -> List[WatchlistItem]:
    """
    Get all watchlist items for a specific user.

    Args:
        db: Database session
        user_id: User's UUID

    Returns:
        List of watchlist items
    """
    return db.query(WatchlistItem).filter(WatchlistItem.user_id == user_id).all()


def get_all_watchlist_items(db: Session) -> List[WatchlistItem]:
    """
    Get all watchlist items across all users (admin only).

    Args:
        db: Database session

    Returns:
        List of all watchlist items
    """
    return db.query(WatchlistItem).all()


def get_watchlist_item_by_id(db: Session, item_id: UUID) -> Optional[WatchlistItem]:
    """
    Get a watchlist item by its ID.

    Args:
        db: Database session
        item_id: Watchlist item UUID

    Returns:
        WatchlistItem if found, None otherwise
    """
    return db.query(WatchlistItem).filter(WatchlistItem.id == item_id).first()


def update_watchlist_item(
    db: Session,
    item_id: UUID,
    watchlist_update: WatchlistItemUpdate
) -> Optional[WatchlistItem]:
    """
    Update a watchlist item.

    Args:
        db: Database session
        item_id: Watchlist item UUID
        watchlist_update: Updated data

    Returns:
        Updated watchlist item if found, None otherwise
    """
    db_item = get_watchlist_item_by_id(db, item_id)
    if not db_item:
        return None

    # Update only provided fields
    update_data = watchlist_update.model_dump(exclude_unset=True)

    # Normalize token symbol if provided
    if "token_symbol" in update_data:
        update_data["token_symbol"] = update_data["token_symbol"].upper()

    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_watchlist_item(db: Session, item_id: UUID) -> bool:
    """
    Delete a watchlist item.

    Args:
        db: Database session
        item_id: Watchlist item UUID

    Returns:
        True if deleted, False if not found
    """
    db_item = get_watchlist_item_by_id(db, item_id)
    if not db_item:
        return False

    db.delete(db_item)
    db.commit()
    return True
