from datetime import datetime
from typing import Optional
from models import Book,Member,Loan
from utils import parse_int, parse_datetime, parse_positive_int
from repositories import BookRepository,MemberRepository,LoanRepository

# --- Book Service --- # 
class BookService:
    @staticmethod
    def create(title: str,author: str,isbn: str, total_copies_raw: str):
        if not title.strip():
            raise ValueError('Title cannot be empty')
        total = parse_positive_int(total_copies_raw)
        b = Book(
            id=None,
            title=title.strip(),
            author=(author or '').strip() or None ,
            isbn= (isbn or '').strip() or None,
            total_copies= total ,
            available_copies=total,
            created_at=None
            )
        return BookRepository.add(b)
    
    @staticmethod
    def list_all():
        return BookRepository.list_all()
    
    @staticmethod
    def get_by_id(bid: int) -> Optional[Book]:
        return BookRepository.get_by_id(bid)
    
    @staticmethod
    def search_by_title(substr: str):
        return BookRepository.search_by_title(substr)
    
    @staticmethod
    def update(bid: int,title: str,author: str, isbn: str, total_raw: str,available_raw: str) -> bool:
        total = parse_positive_int(total_raw)
        available = parse_positive_int(available_raw)
        
        if available > total :
            raise ValueError('Available copies cannot exceed total copies')
        b = Book(
            id = bid,
            title=title.strip(),
            author=(author or '').strip() or None ,
            isbn= (isbn or '').strip() or None,
            total_copies= total ,
            available_copies=available,
            created_at=None
            )
        return BookRepository.update(b)
    
    @staticmethod
    def delete(bid: int) -> bool:
        return BookRepository.delete(bid)
    
# --- Member Service --- # 
class MemberService:
    @staticmethod
    def create(name: str, email: str) -> int:
        if not name.strip():
            raise ValueError('Member name cannot be empty')
        
        m = Member(id=None , name = name.strip(), email=(email or '').strip() or None,created_at=None)
        return MemberRepository.add(m)
    
    @staticmethod
    def list_all():
        return MemberRepository.list_all()
    
    @staticmethod
    def get_by_id(mid: int) -> Optional[Member]:
        return MemberRepository.get_by_id(mid)
    
    @staticmethod
    def search_name(substr: str):
        return MemberRepository.search_by_name(substr)
    
    @staticmethod
    def update(mid: int,name: str, email: str) -> bool:
        if not name.strip():
            raise ValueError("Member name cannot be empty")
        m = Member(id=mid,name=name.strip(), email=(email or  '').strip() or None, created_at=None)
        return MemberRepository.update(m)
        
    @staticmethod
    def delete(mid: int) -> bool:
        return MemberRepository.delete(mid)

# --- Loan Service --- # 
class LoanService:
    @staticmethod
    def loan(book_id_raw: str,member_id_raw:str,due_raw:str,notes:Optional[str]=None) -> int:
        book_id = parse_positive_int(book_id_raw)
        member_id = parse_positive_int(member_id_raw)
        due_at = parse_datetime(due_raw)
        
        if due_at <= datetime.now():
            raise ValueError('Due date must be in the future')
        
        book = BookRepository.get_by_id(book_id)
        if not book:
            raise ValueError('Book does not exist')
        
        member = MemberRepository.get_by_id(member_id)
        if not member:
            raise ValueError('Member does not exist')
        
        if book.available_copies <= 0:
            raise ValueError('No copies available')
        
        loan = Loan(id=None,book_id=book_id,member_id=member_id, loaned_at=datetime.now(),due_at=due_at,returned_at=None, notes=notes,created_at=None)
        return LoanRepository.add(loan)
    
    @staticmethod
    def list_active():
        return LoanRepository.list_all(active_only=True)
    
    @staticmethod
    def list_detailed():
        return LoanRepository.get_detailed_list() 
    
    @staticmethod
    def return_book(loan_id_raw: str) -> bool :
        loan_id = parse_positive_int(loan_id_raw)
        return LoanRepository.mark_return(loan_id)
    
    @staticmethod
    def delete(loan_id_raw: str)-> bool:
        loan_id = parse_positive_int(loan_id_raw)
        return LoanRepository.delete(loan_id)