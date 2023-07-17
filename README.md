# Unb Web
### estudantes: Mateus Valério e Maylla Krislainy
### Engenharia de Software 2023.1

O projeto Chamadas UNB SAAS tem como objetivo de ser um Software as a Service que possibilite o professor crie turmas e aulas para que seu estudantes assinem a chamada. O aplicativo pretende fazer isso por meio da geração de um QRCODE único para cada aula. Com seu smartphone o estudante irá escanear esse QRCODE provido pelo professor e então será capaz de assinar a chamada.

## Instalar as Dependencias

Clone este repositório ou simplesmente baixe-o. Para instalar as dependência: `pip install -r requirements.txt`

## Run App

` python -m flask --app application run` or `flask --app application run`

## Criar migration incial para app (Não necessário se a pasta migration já estiver presente no diretório)

`flask --app application db init` (Caso não haja um banco de dados presente) `flask --app application db migrate -m "Initial migration."` `flask --app application db upgrade`

## Criar novo banco de dados

Se desejas criar uma nova base de dados, será preciso:
1 - Deletar a pasta migrations e o arquio data.sqlite dentro de /app
2 - Executar os comandos para criar a migration inicial, explicados acima (db init, dg migrate e db upgrade)
3 - (Opcional mas recomendado) Popular o banco de dados com dados fictícios

## Popular o banco de dados com dados iniciais fictícios
Para dar seed em todas as tabelas basta usar este comando: `flask --app application seed seed-all`
No entanto é possivel dar seed nas tabelas individualmente seguindo a seguinte ordem:
`flask --app application seed professores`
`flask --app application seed turmas`
`flask --app application seed estudantes` 
`flask --app application seed aulas`
`flask --app application seed questoes`
`flask --app application seed questoes_multipla_escolha`
`flask --app application seed exames` 
`flask --app application seed respostas_questoes_exames`
`flask --app application seed notas_exames`
