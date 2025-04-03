from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from server import Catalog, History, Base  # falls alles in server.py definiert ist

# DB-Verbindung wie im server.py
engine = create_engine('sqlite:///Catalog_with_Vue_Wieder/flask/catalog/catalog.db')
Session = sessionmaker(bind=engine)
session = Session()

def copy_all_to_history():
    cards = session.query(Catalog).all()
    for card in cards:
        history_entry = History(
            card_id=card.id,
            description=card.description,
            change_date=datetime.now()
        )
        session.add(history_entry)

    session.commit()
    print(f"{len(cards)} Einträge wurden erfolgreich in die history-Tabelle kopiert.")

if __name__ == "__main__":
    copy_all_to_history()
