from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SourceDB(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    publisher: Mapped[str] = mapped_column(String(255))
    publication_date: Mapped[date] = mapped_column(Date)
    reporting_period: Mapped[str] = mapped_column(String(100))
    document_type: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(500))


class ProjectDB(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    administrative_code: Mapped[str] = mapped_column(String(50))
    administrative_description: Mapped[str] = mapped_column(String(255))
    project_description: Mapped[str] = mapped_column(String(500))

    budget_year: Mapped[int] = mapped_column()

    original_budget: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 2),
        nullable=True,
    )
    q1_performance: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 2),
        nullable=True,
    )
    ytd_performance: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 2),
        nullable=True,
    )
    performance_percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    balance: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 2),
        nullable=True,
    )

    source_id: Mapped[int] = mapped_column()
    source_page: Mapped[int] = mapped_column()


class BudgetSummaryDB(Base):
    __tablename__ = "budget_summaries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    metric: Mapped[str] = mapped_column(String(255))
    budget_year: Mapped[int] = mapped_column()
    reporting_period: Mapped[str] = mapped_column(String(100))

    original_budget: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 2),
        nullable=True,
    )
    q1_performance: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 2),
        nullable=True,
    )
    performance_percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    source_id: Mapped[int] = mapped_column()
    source_page: Mapped[int] = mapped_column()