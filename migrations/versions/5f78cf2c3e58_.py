"""empty message

Revision ID: 5f78cf2c3e58
Revises: 
Create Date: 2020-05-14 16:49:57.705490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f78cf2c3e58'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('Dept_ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Dept_name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('Dept_ID')
    )
    op.create_table('role',
    sa.Column('role_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('role_id')
    )
    op.create_table('course',
    sa.Column('Course_ID', sa.String(length=64), nullable=False),
    sa.Column('Course_name', sa.String(length=64), nullable=True),
    sa.Column('Classes_held', sa.Integer(), nullable=True),
    sa.Column('dept_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dept_id'], ['department.Dept_ID'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('Course_ID')
    )
    op.create_table('user',
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('fname', sa.String(length=64), nullable=True),
    sa.Column('lname', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('dept', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dept'], ['department.Dept_ID'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('username')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_fname'), ['fname'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_lname'), ['lname'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=False)

    op.create_table('prof_courses',
    sa.Column('prof_id', sa.String(length=64), nullable=True),
    sa.Column('course_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.Course_ID'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['prof_id'], ['user.username'], onupdate='CASCADE', ondelete='CASCADE')
    )
    op.create_table('stud_courses',
    sa.Column('stud_id', sa.String(length=64), nullable=True),
    sa.Column('course_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.Course_ID'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['stud_id'], ['user.username'], onupdate='CASCADE', ondelete='CASCADE')
    )
    op.create_table('ta_courses',
    sa.Column('ta_id', sa.String(length=64), nullable=True),
    sa.Column('course_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.Course_ID'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['ta_id'], ['user.username'], onupdate='CASCADE', ondelete='CASCADE')
    )
    op.create_table('attendance',
    sa.Column('course_id', sa.String(length=64), nullable=False),
    sa.Column('student_id', sa.String(length=64), nullable=False),
    sa.Column('timestamp', sa.Date(), nullable=False),
    sa.Column('faculty_id', sa.String(length=64), nullable=True),
    sa.Column('TA_id', sa.String(length=64), nullable=True),
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
    op.drop_table('course')
    op.drop_table('role')
    op.drop_table('department')
    # ### end Alembic commands ###
