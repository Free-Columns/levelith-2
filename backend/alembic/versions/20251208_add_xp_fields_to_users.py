"""add xp fields to users

Revision ID: add_xp_fields
Revises: 41518377be8d
Create Date: 2025-12-08

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_xp_fields'
down_revision = '41518377be8d'
branch_labels = None
depends_on = None


def upgrade():
    """Add XP and leveling fields to users table."""
    # Add XP category fields
    op.add_column('users', sa.Column('professional_xp', sa.Float(), nullable=False, server_default='0.0'))
    op.add_column('users', sa.Column('education_xp', sa.Float(), nullable=False, server_default='0.0'))
    op.add_column('users', sa.Column('skills_xp', sa.Float(), nullable=False, server_default='0.0'))
    op.add_column('users', sa.Column('vocational_xp', sa.Float(), nullable=False, server_default='0.0'))
    op.add_column('users', sa.Column('total_xp', sa.Float(), nullable=False, server_default='0.0'))
    op.add_column('users', sa.Column('level', sa.Integer(), nullable=False, server_default='0'))


def downgrade():
    """Remove XP and leveling fields from users table."""
    op.drop_column('users', 'level')
    op.drop_column('users', 'total_xp')
    op.drop_column('users', 'vocational_xp')
    op.drop_column('users', 'skills_xp')
    op.drop_column('users', 'education_xp')
    op.drop_column('users', 'professional_xp')
