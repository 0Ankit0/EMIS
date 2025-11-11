"""Library API routes for EMIS."""
from datetime import date
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.middleware.rbac import require_permissions
from src.models.auth import User


router = APIRouter(prefix="/api/v1/library", tags=["Library"])


class BookCreate(BaseModel):
    isbn: str
    title: str = Field(..., min_length=1, max_length=500)
    author: str
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    category: Optional[str] = None
    quantity: int = Field(default=1, ge=1)
    available_quantity: Optional[int] = None


class BookResponse(BaseModel):
    id: UUID
    isbn: str
    title: str
    author: str
    publisher: Optional[str]
    category: Optional[str]
    quantity: int
    available_quantity: int

    class Config:
        from_attributes = True


class BookIssueRequest(BaseModel):
    member_id: UUID
    book_id: UUID
    issue_date: date
    due_date: date


class BookReturnRequest(BaseModel):
    transaction_id: UUID
    return_date: date
    condition: Optional[str] = None


@router.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("library:create")),
):
    """Add a new book to the library."""
    # Implementation would use LibraryService
    return {"message": "Book added successfully"}


@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("library:read")),
):
    """Get book details."""
    # Implementation would use LibraryService
    return {"message": "Book details"}


@router.post("/books/issue")
async def issue_book(
    issue_data: BookIssueRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("library:issue")),
):
    """Issue a book to a member."""
    # Implementation would use LibraryService
    return {"message": "Book issued successfully"}


@router.post("/books/return")
async def return_book(
    return_data: BookReturnRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("library:return")),
):
    """Return a book."""
    # Implementation would use LibraryService
    return {"message": "Book returned successfully"}


@router.get("/books/search")
async def search_books(
    query: str = Query(..., min_length=1),
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("library:read")),
):
    """Search books by title, author, or ISBN."""
    # Implementation would use LibraryService
    return {"message": "Search results"}


# Lost Book Management Endpoints

class LostBookReportRequest(BaseModel):
    """Request model for reporting lost book"""
    issue_id: int
    member_id: int
    book_id: int
    book_title: str
    book_isbn: Optional[str] = None
    book_price: float = Field(..., gt=0)
    loss_date: Optional[date] = None
    notes: Optional[str] = None


class LostBookResponse(BaseModel):
    """Response model for lost book"""
    id: int
    member_id: int
    book_title: str
    book_price: float
    processing_fine: float
    total_fine: float
    amount_paid: float
    is_paid: bool
    status: str
    reported_date: date
    
    class Config:
        from_attributes = True


class LostBookPaymentRequest(BaseModel):
    """Request model for lost book payment"""
    amount: float = Field(..., gt=0)


class LostBookSettingsUpdate(BaseModel):
    """Request model for updating lost book settings"""
    processing_fine_percentage: Optional[float] = Field(None, ge=0, le=100)
    minimum_processing_fine: Optional[float] = Field(None, ge=0)
    maximum_processing_fine: Optional[float] = Field(None, ge=0)
    grace_period_days: Optional[int] = Field(None, ge=0)


@router.post("/books/lost", response_model=LostBookResponse, status_code=status.HTTP_201_CREATED)
async def report_lost_book(
    request: LostBookReportRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions(["library:manage"])),
):
    """Report a book as lost
    
    This endpoint creates a lost book record with automatic fine calculation
    based on the book price and system settings.
    
    Fine Calculation:
    - Total Fine = Book Price + Processing Fine
    - Processing Fine = Book Price * (processing_fine_percentage / 100)
    - Processing Fine is capped between min and max limits
    """
    from src.services.book_loss_service import BookLossService
    
    service = BookLossService(db)
    
    try:
        book_loss = await service.report_lost_book(
            issue_id=request.issue_id,
            member_id=request.member_id,
            book_id=request.book_id,
            book_title=request.book_title,
            book_isbn=request.book_isbn,
            book_price=request.book_price,
            loss_date=request.loss_date,
            reported_by=current_user.id
        )
        
        return book_loss
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/books/lost/{loss_id}", response_model=LostBookResponse)
async def get_lost_book(
    loss_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions(["library:read"])),
):
    """Get lost book details by ID"""
    from src.services.book_loss_service import BookLossService
    from sqlalchemy import select
    from src.models.book_loss import BookLoss
    
    result = await db.execute(
        select(BookLoss).where(BookLoss.id == loss_id)
    )
    book_loss = result.scalar_one_or_none()
    
    if not book_loss:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lost book record {loss_id} not found"
        )
    
    return book_loss


@router.get("/books/lost/member/{member_id}", response_model=List[LostBookResponse])
async def get_member_lost_books(
    member_id: int,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions(["library:read"])),
):
    """Get all lost books for a specific member"""
    from src.services.book_loss_service import BookLossService
    from src.models.book_loss import LossStatus
    
    service = BookLossService(db)
    
    loss_status = LossStatus(status) if status else None
    losses = await service.get_losses_by_member(member_id, loss_status)
    
    return losses


@router.post("/books/lost/{loss_id}/investigate")
async def investigate_lost_book(
    loss_id: int,
    notes: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions(["library:manage"])),
):
    """Mark a lost book as under investigation"""
    from src.services.book_loss_service import BookLossService
    
    service = BookLossService(db)
    
    try:
        book_loss = await service.investigate_loss(
            loss_id=loss_id,
            investigator_id=current_user.id,
            notes=notes
        )
        
        return {
            "message": "Lost book marked as under investigation",
            "loss_id": book_loss.id,
            "status": book_loss.status
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/books/lost/{loss_id}/confirm")
async def confirm_lost_book(
    loss_id: int,
    resolution_notes: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions(["library:manage"])),
):
    """Confirm a book loss"""
    from src.services.book_loss_service import BookLossService
    
    service = BookLossService(db)
    
    try:
        book_loss = await service.confirm_loss(
            loss_id=loss_id,
            confirmed_by=current_user.id,
            resolution_notes=resolution_notes
        )
        
        return {
            "message": "Book loss confirmed",
            "loss_id": book_loss.id,
            "total_fine": book_loss.total_fine,
            "status": book_loss.status
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/books/lost/{loss_id}/payment", response_model=LostBookResponse)
async def record_lost_book_payment(
    loss_id: int,
    payment: LostBookPaymentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions(["library:manage", "finance:manage"])),
):
    """Record payment for a lost book
    
    When the total amount is paid, the loss status automatically changes to RESOLVED.
    """
    from src.services.book_loss_service import BookLossService
    
    service = BookLossService(db)
    
    try:
        book_loss = await service.record_payment(
            loss_id=loss_id,
            amount=payment.amount
        )
        
        return book_loss
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/books/lost/{loss_id}/waive")
async def waive_lost_book(
    loss_id: int,
    reason: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions(["library:admin"])),
):
    """Waive a lost book fine (requires admin permission)"""
    from src.services.book_loss_service import BookLossService
    
    service = BookLossService(db)
    
    try:
        book_loss = await service.waive_loss(
            loss_id=loss_id,
            reason=reason,
            waived_by=current_user.id
        )
        
        return {
            "message": "Lost book fine waived",
            "loss_id": book_loss.id,
            "status": book_loss.status
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/books/lost/unpaid")
async def get_unpaid_lost_books(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions(["library:read", "finance:read"])),
):
    """Get all unpaid lost book fines"""
    from src.services.book_loss_service import BookLossService
    
    service = BookLossService(db)
    losses = await service.get_unpaid_losses()
    
    total_unpaid = sum(loss.total_fine - loss.amount_paid for loss in losses)
    
    return {
        "count": len(losses),
        "total_unpaid_amount": total_unpaid,
        "losses": losses
    }


@router.get("/settings/lost-books")
async def get_lost_book_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions(["library:read"])),
):
    """Get current lost book fine settings"""
    from src.services.book_loss_service import BookLossService
    
    service = BookLossService(db)
    settings = await service.get_lost_book_settings()
    
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lost book settings not configured"
        )
    
    return settings


@router.put("/settings/lost-books")
async def update_lost_book_settings(
    settings_update: LostBookSettingsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions(["library:admin", "settings:manage"])),
):
    """Update lost book fine settings (requires admin permission)"""
    from src.services.book_loss_service import BookLossService
    
    service = BookLossService(db)
    
    settings = await service.update_lost_book_settings(
        processing_fine_percentage=settings_update.processing_fine_percentage,
        minimum_processing_fine=settings_update.minimum_processing_fine,
        maximum_processing_fine=settings_update.maximum_processing_fine,
        grace_period_days=settings_update.grace_period_days
    )
    
    return {
        "message": "Lost book settings updated successfully",
        "settings": settings
    }
