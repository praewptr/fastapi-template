import logging

from sqlmodel import Session

from app.core.db import engine, init_db, init_db_without_alembic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def init_without_alembic() -> None:
    with Session(engine) as session:
        init_db_without_alembic(session)


def main() -> None:
    logger.info("Creating initial data")
    # init()
    init_without_alembic()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
