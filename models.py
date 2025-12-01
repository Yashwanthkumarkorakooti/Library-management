from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Book:
    id: Optional[int]
    title: str 
    author: Optional[str]
    isbn: Optional[str]
    total_copies: int
    available_copies: int
    created_at: Optional[datetime] = None 
    
@dataclass
class Member:
    id: Optional[int]
    name: str 
    email: Optional[str]
    created_at: Optional[datetime] = None 
    
@dataclass
class Loan:
    id: Optional[int]
    book_id: int
    member_id: int
    loaned_at: datetime 
    due_at: datetime 
    returned_at: Optional[datetime] = None 
    notes: Optional[str] = None 
    created_at: Optional[datetime] = None