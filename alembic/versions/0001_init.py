
"""initial tables

Revision ID: 0001_init
Revises: 
Create Date: 2025-11-03 00:00:00

"""
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('conversations',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('channel', sa.Enum('sms','web', name='channelenum'), nullable=False),
        sa.Column('user_ref', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table('messages',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('conversation_id', sa.String(), sa.ForeignKey('conversations.id')),
        sa.Column('role', sa.Enum('user','assistant','system', name='roleenum')),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('crisis_flag', sa.Boolean(), server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table('feedback',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('conversation_id', sa.String(), sa.ForeignKey('conversations.id')),
        sa.Column('rating', sa.Integer()),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('feedback')
    op.drop_table('messages')
    op.drop_table('conversations')
    op.execute('DROP TYPE IF EXISTS channelenum')
    op.execute('DROP TYPE IF EXISTS roleenum')
