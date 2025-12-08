"""
Alembic migration: expand naics schema
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251119_expand_naics_schema'
down_revision = None
branch_labels = None
depends_on = None




def upgrade():
    # Add columns if they don't exist
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    cols = [c['name'] for c in inspector.get_columns('naics_codes')]

    def add_col_if_missing(name, col):
        if name not in cols:
            op.add_column('naics_codes', col)

    add_col_if_missing('sector', sa.Column('sector', sa.String(length=100)))
    add_col_if_missing('subsector', sa.Column('subsector', sa.String(length=100)))
    add_col_if_missing('industry_group', sa.Column('industry_group', sa.String(length=100)))
    add_col_if_missing('industry_detail', sa.Column('industry_detail', sa.String(length=100)))
    add_col_if_missing('sba_size_standard', sa.Column('sba_size_standard', sa.String(length=50)))
    add_col_if_missing('sba_source', sa.Column('sba_source', sa.Text()))
    add_col_if_missing('examples', sa.Column('examples', sa.Text()))
    add_col_if_missing('cross_references', sa.Column('cross_references', sa.Text()))
    add_col_if_missing('notes', sa.Column('notes', sa.Text()))
    add_col_if_missing('keywords', sa.Column('keywords', sa.Text()))
    add_col_if_missing('aliases', sa.Column('aliases', sa.Text()))
    add_col_if_missing('data_source', sa.Column('data_source', sa.Text()))

    # Create helper tables
    op.create_table(
        'naics_code_history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('code', sa.String(length=6), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500)),
        sa.Column('description', sa.Text()),
        sa.Column('changes', sa.Text()),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('NOW()'))
    )

    op.create_table(
        'naics_crosswalks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('code_old', sa.String(length=6), nullable=False),
        sa.Column('code_new', sa.String(length=6), nullable=False),
        sa.Column('year_old', sa.Integer(), nullable=False),
        sa.Column('year_new', sa.Integer(), nullable=False),
        sa.Column('relationship', sa.String(length=50)),
        sa.Column('notes', sa.Text())
    )

    op.create_table(
        'sba_size_standards',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('naics_code', sa.String(length=6), nullable=False),
        sa.Column('size_type', sa.String(length=50), nullable=False),
        sa.Column('size_threshold', sa.Numeric(12,2), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False, server_default='USD'),
        sa.Column('notes', sa.Text()),
        sa.Column('effective_date', sa.Date(), server_default=sa.text('CURRENT_DATE'))
    )


def downgrade():
    # Drop helper tables
    op.drop_table('sba_size_standards')
    op.drop_table('naics_crosswalks')
    op.drop_table('naics_code_history')

    # Drop columns from naics_codes table
    columns_to_drop = [
        'sector', 'subsector', 'industry_group', 'industry_detail',
        'sba_size_standard', 'sba_source', 'examples', 'cross_references',
        'notes', 'keywords', 'aliases', 'data_source'
    ]

    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_cols = [c['name'] for c in inspector.get_columns('naics_codes')]

    for col_name in columns_to_drop:
        if col_name in existing_cols:
            op.drop_column('naics_codes', col_name)