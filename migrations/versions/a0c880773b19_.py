"""empty message

Revision ID: a0c880773b19
Revises: 
Create Date: 2020-03-27 11:44:52.879965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0c880773b19'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('Course_ID', sa.Integer(), nullable=False),
    sa.Column('Course_name', sa.String(length=64), nullable=True),
    sa.Column('Classes_held', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('Course_ID')
    )
    op.create_table('department',
    sa.Column('Dept_ID', sa.Integer(), nullable=False),
    sa.Column('Dept_name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('Dept_ID')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('fname', sa.String(length=64), nullable=True),
    sa.Column('lname', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('dept', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['dept'], ['department.Dept_ID'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
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
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Date(), nullable=False),
    sa.Column('faculty_id', sa.Integer(), nullable=True),
    sa.Column('TA_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['TA_id'], ['ta_courses.ta_id'], ),
    sa.ForeignKeyConstraint(['course_id'], ['stud_courses.course_id'], ),
    sa.ForeignKeyConstraint(['faculty_id'], ['prof_courses.prof_id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['stud_courses.stud_id'], ),
    sa.PrimaryKeyConstraint('course_id', 'student_id', 'timestamp')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attendance')
    op.drop_table('ta_courses')
    op.drop_table('stud_courses')
    op.drop_table('prof_courses')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_lname'))
        batch_op.drop_index(batch_op.f('ix_user_fname'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('department')
    op.drop_table('course')
    # ### end Alembic commands ###