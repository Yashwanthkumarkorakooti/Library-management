from database import initialize_db
from services import BookService, MemberService, LoanService 

def print_menu():
    print('\n --- Library Management ---')
    print('1. Add Book')
    print('2. View All Books')
    print('3. Search Books by Title')
    print('4. View Book by ID')
    print('5. Update Book')
    print('6. Delete Book')
    print('7. Add Member')
    print('8. View All Members')
    print('9. Search Members by Name')
    print('10. View Member by ID')
    print('11. Update Member')
    print('12. Delete Member')
    print('13. Loan a Book')
    print('14. View Active Loans')
    print('15. View Loans (detailed)')
    print('16. Return a Book')
    print('17. Delete a Loan')
    print('0. Exit')
    
    
def main():
    initialize_db()
    
    while True:
        print_menu()
        ch = input('Enter choice: ').strip()
        
        try:
            if ch == '1':
                title = input('Title: ')
                author = input('Author (optional): ')
                isbn = input('ISBN (optional): ')
                total = input('Total copies: ')
                bid = BookService.create(title,author,isbn,total)
                print(f'✅ Book added with Id : {bid}')
            
            elif ch == '2':
                books = BookService.list_all()
                if not books:
                    print('No books found')
                else:
                    for b in books:
                        print(b)
                        
            elif ch == '3':
                q = input('Title substring: ')
                for b in BookService.search_by_title(q):
                    print(b)
                    
            elif ch == '4':
                bid = int(input('Enter the bookId: '))
                book = BookService.get_by_id(bid)
                print(book if book else '❌ Book not found')
                
            elif ch == '5':
                bid = int(input('Book ID: '))
                title = input('New Title: ')
                author = input('New Author (optional): ')
                isbn = input('New ISBN (optional): ')
                total = input('Total copies: ')
                available = input('Available copies: ') 
                ok = BookService.update(bid,title,author,isbn,total,available)
                print('✅ Updated' if ok else '❌ Not found')
                
            elif ch == '6':
                bid = int(input('Book ID to delete: '))
                ok = BookService.delete(bid)
                print('■ Deleted' if ok else '❌ Not Found')
                
            elif ch == '7':
                name = input('Member name: ')
                email = input('Email (optional): ')
                mid = MemberService.create(name,email)
                print(f'✅ Member added with Id: {mid}')
                
            elif ch == '8':
                members = MemberService.list_all()
                if not members:
                    print('No members found')
                else:
                    for m in members:
                        print(m)
                        
            elif ch == '9':
                q = input('Name substring: ')
                for m in MemberService.search_name(q):
                    print(m)
                    
            elif ch == '10':
                mid = int(input('Enter Member ID: '))
                member = MemberService.get_by_id(mid)
                print(member if member else "❌ Member not found")
                
            elif ch == '11':
                mid = int(input("Member ID: "))
                name = input("New Name: ")
                email = input("New Email (optional): ")
                ok = MemberService.update(mid, name, email)
                print("✅ Updated" if ok else "❌ Not Found")

            elif ch == '12':
                mid = int(input("Member ID to delete: "))
                ok = MemberService.delete(mid)
                print("✅ Deleted" if ok else "❌ Not Found")

            elif ch == '13':
                print('Provide book_id, member_id and due date (YYYY-MM-DD HH:MM)')
                bid = input('Book ID: ')
                mid = input('Member ID: ')
                due = input('Due At: ')
                notes = input('Notes (optional): ')
                lid = LoanService.loan(bid, mid, due, notes)
                print(f'✅ Loan created (ID: {lid})')

            elif ch == '14':
                for l in LoanService.list_active():
                    print(l)

            elif ch == '15':
                for d in LoanService.list_detailed():
                    print(d)

            elif ch == '16':
                lid = input('Loan ID to return: ')
                ok = LoanService.return_book(lid)
                print('✅ Returned' if ok else '❌ Not found / already returned')

            elif ch == '17':
                lid = input('Loan ID to delete: ')
                ok = LoanService.delete(lid)
                print('✅ Deleted' if ok else '❌ Not found')

            elif ch == '0':
                print("Exiting...")
                break

            else:
                print('Invalid Option')
                
        except Exception as e :
            print(f'Error: {e}')
            
if __name__ == '__main__':
    main()