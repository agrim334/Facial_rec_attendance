"""empty message

Revision ID: 6d0e583a60ad
Revises: 
Create Date: 2020-02-04 15:21:11.438412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d0e583a60ad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('Course_ID', sa.Integer(), nullable=False),
    sa.Column('Course_name', sa.String(length=64), nullable=True),
    sa.Column('Classes_held', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('Course_ID')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('fname', sa.String(length=64), nullable=True),
    sa.Column('lname', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('dept', sa.String(length=20), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_dept'), ['dept'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_fname'), ['fname'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_lname'), ['lname'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('prof_courses',
    sa.Column('prof_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.Course_ID'], ),
    sa.ForeignKeyConstraint(['prof_id'], ['user.id'], )
    )
    op.create_table('stud_courses',
    sa.Column('stud_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.Course_ID'], ),
    sa.ForeignKeyConstraint(['stud_id'], ['user.id'], )
    )
    op.create_table('ta_courses',
    sa.Column('ta_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.Course_ID'], ),
    sa.ForeignKeyConstraint(['ta_id'], ['user.id'], )
    )
    op.create_table('attendance',
    sa.Column('Attd_ID', sa.Integer(), nullable=False),
    sa.Column('Course_ID', sa.Integer(), nullable=True),
    sa.Column('Stud_ID', sa.Integer(), nullable=True),
    sa.Column('Present', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('Faculty', sa.Integer(), nullable=True),
    sa.Column('TA', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Course_ID'], ['stud_courses.course_id'], ),
    sa.ForeignKeyConstraint(['Faculty'], ['prof_courses.prof_id'], ),
    sa.ForeignKeyConstraint(['Stud_ID'], ['stud_courses.stud_id'], ),
    sa.ForeignKeyConstraint(['TA'], ['ta_courses.ta_id'], ),
    sa.PrimaryKeyConstraint('Attd_ID')
    )
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_attendance_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_attendance_timestamp'))

    op.drop_table('attendance')
    op.drop_table('ta_courses')
    op.drop_table('stud_courses')
    op.drop_table('prof_courses')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_lname'))
        batch_op.drop_index(batch_op.f('ix_user_fname'))
        batch_op.drop_index(batch_op.f('ix_user_email'))
        batch_op.drop_index(batch_op.f('ix_user_dept'))

    op.drop_table('user')
    op.drop_table('course')
    # ### end Alembic commands ###
