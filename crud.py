from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Book


# ------------------ Books ------------------ #
def get_books(db: Session, search: str = None) -> list[Book]:
    """
    Fetch all libros, or filter by search term in title/author
    using case-insensitive matching.
    """
    query = db.query(Book).order_by(Book.authors)

    if search:
        tokens = search.strip().split()
        for token in tokens:
            like_pattern = f"%{token}%"
            query = query.filter(
                or_(
                    Book.title.ilike(like_pattern),
                    Book.authors.ilike(like_pattern)
                )
            )

    return query.all()

