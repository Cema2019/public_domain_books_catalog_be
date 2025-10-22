from sqlalchemy import select, or_
from models import Book

# ------------------ Books ------------------ #
def get_books_query(search: str | None = None):
    """
    Builds and returns a SQLAlchemy 2.0-style Select statement for books.
    Pagination (skip/limit) is applied by fastapi-pagination.
    """
    stmt = select(Book).order_by(Book.authors)

    if search:
        tokens = search.strip().split()
        for token in tokens:
            like_pattern = f"%{token}%"
            stmt = stmt.where(
                or_(
                    Book.title.ilike(like_pattern),
                    Book.authors.ilike(like_pattern)
                )
            )

    return stmt

