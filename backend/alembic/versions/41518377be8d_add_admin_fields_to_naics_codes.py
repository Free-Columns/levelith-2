"""add_admin_fields_to_naics_codes

Adds admin-specific fields to the naics_codes table:
- tags: JSON array for custom tagging and categorization
- custom_category: String field for admin-defined categories
- admin_notes: Text field for internal notes and comments

Revision ID: 41518377be8d
Revises:
Create Date: 2025-11-19 21:33:34.629579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '41518377be8d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Add admin-specific fields to naics_codes table.

    These fields are for internal admin use only and do not affect
    the official NAICS classification data.
    """
    # Add tags column (JSON array, defaults to empty list)
    op.add_column('naics_codes',
        sa.Column('tags',
                  postgresql.JSON(astext_type=sa.Text()),
                  nullable=False,
                  server_default='[]')
    )

    # Add custom_category column (optional string)
    op.add_column('naics_codes',
        sa.Column('custom_category',
                  sa.String(length=100),
                  nullable=True)
    )

    # Add admin_notes column (optional text)
    op.add_column('naics_codes',
        sa.Column('admin_notes',
                  sa.Text(),
                  nullable=True)
    )


def downgrade() -> None:
    """
    Remove admin-specific fields from naics_codes table.

    WARNING: This will permanently delete all admin tags, custom categories,
    and notes. Ensure you have a backup before downgrading.
    """
    # Remove columns in reverse order
    op.drop_column('naics_codes', 'admin_notes')
    op.drop_column('naics_codes', 'custom_category')
    op.drop_column('naics_codes', 'tags')
