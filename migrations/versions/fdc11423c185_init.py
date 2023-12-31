"""init

Revision ID: fdc11423c185
Revises: 
Create Date: 2023-07-22 18:10:22.654988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdc11423c185'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=150), nullable=False),
    sa.Column('matricula', sa.String(length=15), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('senha', sa.String(length=200), nullable=False),
    sa.Column('tipo_usuario', sa.Enum('estudante', 'professor', name='tipo_usuario'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('matricula')
    )
    op.create_table('estudante',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('professor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enunciado', sa.String(length=255), nullable=True),
    sa.Column('resposta', sa.String(length=255), nullable=True),
    sa.Column('tipo_questao', sa.Enum('multipla_escolha', 'verdadeiro_falso', 'numerica', 'dissertativa', name='tipo_questao'), nullable=False),
    sa.Column('professor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['professor_id'], ['professor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('turma',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('horario_inicio', sa.Time(), nullable=False),
    sa.Column('horario_fim', sa.Time(), nullable=False),
    sa.Column('senha', sa.String(length=200), nullable=False),
    sa.Column('semestre', sa.Integer(), nullable=False),
    sa.Column('professor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['professor_id'], ['professor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('aula',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('turma_id', sa.Integer(), nullable=False),
    sa.Column('data_aula', sa.Date(), nullable=False),
    sa.Column('status', sa.Enum('agendado', 'finalizado', 'em andamento', 'cancelado', name='StatusAula'), nullable=False),
    sa.Column('token', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['turma_id'], ['turma.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exame',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_inicio', sa.DateTime(), nullable=True),
    sa.Column('data_fim', sa.DateTime(), nullable=True),
    sa.Column('nome', sa.String(length=255), nullable=True),
    sa.Column('nota_exame', sa.Float(), nullable=True),
    sa.Column('professor_id', sa.Integer(), nullable=False),
    sa.Column('turma_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['professor_id'], ['professor.id'], ),
    sa.ForeignKeyConstraint(['turma_id'], ['turma.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('matricula',
    sa.Column('estudante_id', sa.Integer(), nullable=False),
    sa.Column('turma_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['estudante_id'], ['estudante.id'], ),
    sa.ForeignKeyConstraint(['turma_id'], ['turma.id'], ),
    sa.PrimaryKeyConstraint('estudante_id', 'turma_id')
    )
    op.create_table('questao_multipla_escolha',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('opcao_a', sa.String(length=255), nullable=True),
    sa.Column('opcao_b', sa.String(length=255), nullable=True),
    sa.Column('opcao_c', sa.String(length=255), nullable=True),
    sa.Column('opcao_d', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['questao.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notas_exames',
    sa.Column('exame_id', sa.Integer(), nullable=False),
    sa.Column('estudante_id', sa.Integer(), nullable=False),
    sa.Column('nota_exame_estudante', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['estudante_id'], ['estudante.id'], ),
    sa.ForeignKeyConstraint(['exame_id'], ['exame.id'], ),
    sa.PrimaryKeyConstraint('exame_id', 'estudante_id')
    )
    op.create_table('presenca',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('aula_id', sa.Integer(), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=True),
    sa.Column('estudante_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['aula_id'], ['aula.id'], ),
    sa.ForeignKeyConstraint(['estudante_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questao_exame',
    sa.Column('exame_id', sa.Integer(), nullable=False),
    sa.Column('questao_id', sa.Integer(), nullable=False),
    sa.Column('nota_questao', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['exame_id'], ['exame.id'], ),
    sa.ForeignKeyConstraint(['questao_id'], ['questao.id'], ),
    sa.PrimaryKeyConstraint('exame_id', 'questao_id')
    )
    op.create_table('resposta_questao_exame',
    sa.Column('resposta_estudante', sa.String(length=255), nullable=True),
    sa.Column('nota_estudante_questao', sa.Float(), nullable=True),
    sa.Column('estudante_id', sa.Integer(), nullable=False),
    sa.Column('exame_id', sa.Integer(), nullable=False),
    sa.Column('questao_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['estudante_id'], ['estudante.id'], ),
    sa.ForeignKeyConstraint(['exame_id'], ['exame.id'], ),
    sa.ForeignKeyConstraint(['questao_id'], ['questao.id'], ),
    sa.PrimaryKeyConstraint('estudante_id', 'exame_id', 'questao_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resposta_questao_exame')
    op.drop_table('questao_exame')
    op.drop_table('presenca')
    op.drop_table('notas_exames')
    op.drop_table('questao_multipla_escolha')
    op.drop_table('matricula')
    op.drop_table('exame')
    op.drop_table('aula')
    op.drop_table('turma')
    op.drop_table('questao')
    op.drop_table('professor')
    op.drop_table('estudante')
    op.drop_table('usuario')
    # ### end Alembic commands ###
