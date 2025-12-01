from encrypt import MultiAccountEncrypt   
from gui import Base_page 

def main():
    manager = MultiAccountEncrypt()
    try:
        manager.load_accounts_from_file("multi_accounts.bin")
    except Exception:
        pass

    app = Base_page(manager=manager) 
    app.home_page()

if __name__ == "__main__":
    main()