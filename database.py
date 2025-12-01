import os 
import time
import pyodbc
from dotenv import load_dotenv
from contextlib import contextmanager 

load_dotenv()

DRIVER= os.getenv('DB_DRIVER','{ODBC Driver 17 for SQL Server}')
SERVER= os.getenv('DB_SERVER','localhost')
DATABASE= os.getenv('DB_NAME','libraryDB')
ENCRYPT= os.getenv('ENCRYPT','no')

CONN_STR_TEMPLATE = (
    'DRIVER={driver};'
    'SERVER={server};'
    'DATABASE={database};'
    'Encrypt={encrypt};'
    'Trusted_Connection=Yes;'
    'TrustServerCertificate=yes;'
)

def __build_conn_str(server=SERVER, database=DATABASE):
    return CONN_STR_TEMPLATE.format(
        driver=DRIVER,
        server=server,
        database=database,
        encrypt=ENCRYPT
    )
    
    
@contextmanager
def get_connection(server: str=SERVER, database: str=DATABASE,max_retries: int=3, retry_delay: float = 1.0):
    attempts = 0 
    last_exc = None
    while attempts < max_retries:
        try:
            conn = pyodbc.connect(__build_conn_str(server=server, database=database)) 
            try:
                yield conn 
            finally :
                try:
                    conn.close()
                except:
                    pass 
            return 
        except Exception as e :
            attempts += 1 
            last_exc = e 
            time.sleep(retry_delay)
    raise last_exc

def initialize_db():
    master_conn_str = __build_conn_str(server=SERVER,database='master')
    
    with pyodbc.connect(master_conn_str,autocommit=True) as conn :
        cur = conn.cursor()
        cur.execute('select 1 from sys.databases where name = ?', (DATABASE,))
        row = cur.fetchone()
        
        if not row:
            cur.execute(f'CREATE DATABASE [{DATABASE}]')
            
    with get_connection(server=SERVER, database=DATABASE) as conn :
        cur = conn.cursor()
        cur.execute(''' 
                    IF NOT EXISTS (
                        SELECT 1 from information_schema.tables WHERE table_name='books'
                    )
                    begin
                        create table books(
                            id int identity(1,1) primary key,
                            title varchar(100) not null,
                            author varchar(150) null,
                            isbn varchar(20) null,
                            total_copies int not null,
                            available_copies int not null,
                            created_at Datetime2 default getdate()
                        )
                    end
        ''')
        
        cur.execute('''
                    IF NOT EXISTS(
                        SELECT 1 FROM information_schema.tables WHERE table_name = 'members'
                    )
                    begin
                        CREATE TABLE members(
                            id INT IDENTITY(1,1) PRIMARY KEY,
                            name VARCHAR(120) NOT NULL,
                            email VARCHAR(200) NULL,
                            created_at DATETIME2 DEFAULT GETDATE()
                        )
                    end
        ''')
        
        cur.execute(''' 
                    IF NOT EXISTS (
                        SELECT 1 from information_schema.tables WHERE table_name = 'loans'
                    )
                    begin
                        create table loans(
                            id int identity(1,1) primary key, 
                            book_id int not null,
                            member_id int not null,
                            loaned_at datetime2 not null,
                            due_at datetime2 not null,
                            returned_at datetime2 null,
                            notes varchar(500) null,
                            created_at datetime2 default getdate(),
                            CONSTRAINT FK_Loans_Book FOREIGN KEY (book_id) REFERENCES books(id),
                            CONSTRAINT FK_Loans_Member FOREIGN KEY (member_id) REFERENCES members(id)
                        )
                    end
        ''')
        
        conn.commit()