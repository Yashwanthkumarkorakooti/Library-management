from typing import List,Optional 
from database import get_connection
from models import Book,Member,Loan


# --- Book Repo --- # 
class BookRepository:
    @staticmethod
    def add(book: Book) -> int :
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('insert into books (title,author,isbn,total_copies,available_copies) values(?,?,?,?,?)',
                        (book.title,book.author,book.isbn,book.total_copies,book.available_copies))
            conn.commit()
            cur.execute('select cast(scope_identity() as int)')
            row = cur.fetchone()[0]
            return row
    
    @staticmethod
    def list_all() -> List[Book]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('select id,title,author,isbn,total_copies,available_copies,created_at from books order by id')
            rows = cur.fetchall()
            return [Book(*r) for r in rows]
    
    @staticmethod
    def get_by_id(bid: int) -> Optional[Book]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('select id,title,author,isbn,total_copies,available_copies,created_at from books where id=?',(bid,))
            row = cur.fetchone()
            return Book(*row) if row else None 
    
    @staticmethod
    def search_by_title(substr: str) ->List[Book]:
        like = f'%{substr}%'
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('select id,title,author,isbn,total_copies,available_copies,created_at from books where title like ?', (like,))
            rows = cur.fetchall()
            return [Book(*r) for r in rows]
    
    @staticmethod
    def update(book: Book) -> bool :
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('update books set title=?,author=?,isbn=?,total_copies=?,available_copies=? where id=?',
                        (book.title,book.author,book.isbn,book.total_copies,book.available_copies,book.id))
            conn.commit()
            return cur.rowcount > 0 
    
    @staticmethod
    def delete(bid: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('delete from books where id=?',(bid,))
            conn.commit()
            return cur.rowcount > 0 

# --- Member Repo --- # 
class MemberRepository:
    @staticmethod
    def add(member: Member) -> int :
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('insert into members (name,email) values(?,?)',(member.name,member.email))
            conn.commit()
            cur.execute('select cast(scope_identity() as int)')
            return cur.fetchone()[0]
    
    @staticmethod 
    def list_all() -> List[Member]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('select id, name, email, created_at from members order by id')
            rows = cur.fetchall()
            return [Member(*r) for r in rows]
    
    @staticmethod
    def get_by_id(mid: int) -> Optional[Member]:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('select id, name, email, created_at from members where id=?',(mid,))
            row = cur.fetchone()
            return Member(*row) if row else None
    
    @staticmethod
    def search_by_name(substr: str) -> List[Member]:
        like = f'%{substr}%'
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('select id, name, email, created_at from members where name like ?',(like,))
            rows = cur.fetchall()
            return [Member(*r) for r in rows]
    
    @staticmethod
    def update(member: Member) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('update members set name=?,email=? where id=?',(member.name,member.email,member.id))
            conn.commit()
            return cur.rowcount > 0 
    
    @staticmethod
    def delete(mid: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('delete from members where id=?',(mid,))
            conn.commit()
            return cur.rowcount > 0 

# --- Loan Repo --- # 
class LoanRepository:
    @staticmethod
    def add(loan: Loan) -> int :
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('select available_copies from books where id=?',(loan.book_id,))
            row = cur.fetchone()
            if not row or row[0] <= 0 :
                raise Exception('No copies available')
            
            cur.execute('insert into loans (book_id,member_id,loaned_at,due_at,returned_at,notes) values(?,?,?,?,?,?)',
                        (loan.book_id,loan.member_id,loan.loaned_at,loan.due_at,loan.returned_at,loan.notes))
            cur.execute('update books set available_copies = available_copies - 1 where id = ? and available_copies > 0',(loan.book_id,))
            conn.commit()
            cur.execute('select cast(scope_identity() as int)')
            return cur.fetchone()[0]
    
    @staticmethod
    def list_all(active_only: bool = False) -> List[Loan]:
        with get_connection() as conn:
            cur = conn.cursor()
            if active_only:
                cur.execute('select id,book_id,member_id,loaned_at,due_at,returned_at, notes, created_at from loans where returned_at is null')
            else:
                cur.execute('select id,book_id,member_id,loaned_at,due_at,returned_at, notes, created_at from loans order by loaned_at desc')
            rows = cur.fetchall()
            return [Loan(*r) for r in rows]
    
    @staticmethod
    def get_detailed_list():
        with get_connection() as conn :
            cur = conn.cursor()
            cur.execute('''
                        select l.id,b.id,b.title,m.id,m.name,l.loaned_at,l.due_at,l.returned_at,l.notes 
                        from loans l join books b on l.book_id = b.id  join members m on l.member_id = m.id 
                        order by l.loaned_at desc
                        ''')
            rows = cur.fetchall()
            return [{
                'loan_id':r[0],
                'book_id':r[1],
                'book_title':r[2],
                'member_id':r[3],
                'member_name':r[4],
                'loaned_at':r[5],
                'due_at':r[6],
                'returned_at':r[7],
                'notes':r[8]
            }
                for r in rows
            ]
    
    @staticmethod
    def mark_return(loan_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('select book_id from loans where id = ? and returned_at is null',(loan_id,))
            row = cur.fetchone()
            if not row :
                return False
            book_id = row[0]
            cur.execute('update loans set returned_at= getdate() where id=?',(loan_id,))
            cur.execute('update books set available_copies = available_copies + 1 where id = ?',(book_id,))
            conn.commit()
            return cur.rowcount > 0 
    
    @staticmethod
    def delete(loan_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('delete from loans where id=?',(loan_id,))
            conn.commit()
            return cur.rowcount > 0 