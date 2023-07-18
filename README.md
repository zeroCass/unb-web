# Unb Web
### Estudantes: Mateus Valério e Maylla Krislainy
### Engenharia de Software 2023.1

## Índice
- [Sobre](#sobre)
- [Como Usar](#como-usar)
- [Configuração e Uso](#configuração-e-uso)
- [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
  - [Criar migração inicial para o aplicativo](#criar-migração-inicial-para-o-aplicativo)
  - [Criar um novo banco de dados](#criar-um-novo-banco-de-dados)
    
## Sobre
O projeto UNB WEB SAAS tem como objetivo de ser um Software as a Service que possibilite o professor crie turmas e aulas para que seu estudantes assinem a chamada. O aplicativo pretende fazer isso por meio da geração de um QRCODE único para cada aula. Com seu smartphone o estudante irá escanear esse QRCODE provido pelo professor e então será capaz de assinar a chamada. Além disso, os alunos também podem responder e revisar exames elaboradas pelos professores, promovendo um ambiente interativo de aprendizado.

## Como Usar


## Configuração e Uso
Para utilizar este projeto, siga as seguintes etapas:

1. Faça o download ou clone o repositório.
2. Execute o comando `pip install -r requirements.txt` para instalar as dependências.
3. Execute o comando ` python -m flask --app application run` or `flask --app application run` para iniciar o projeto.
4. Acesse o projeto em `http://127.0.0.1:5000`.

## Configuração do Banco de Dados

### Criar migração inicial para o aplicativo
(Não necessário se a pasta "migrations" estiver presente no diretório e haja um banco de dados )

Execute os seguintes comandos:
```shell
flask --app application db init
flask --app application db migrate -m "Initial migration."
flask --app application db upgrade
```

### Criar um novo banco de dados
Se desejar criar um novo banco de dados, siga os passos abaixo:

  1. Delete a pasta "migrations" e o arquivo "data.sqlite" dentro do diretório /app.
  2. Execute os comandos para criar a migração inicial, como mencionado acima (db init, db migrate e db upgrade).
  3. (Opcional, mas recomendado) Popule o banco de dados com dados fictícios.

Para popular todas as tabelas, execute o seguinte comando:
`flask --app application seed seed-all`

No entanto, é possível popular as tabelas individualmente seguindo a ordem abaixo:
```shell
flask --app application seed professores
flask --app application seed turmas
flask --app application seed estudantes
flask --app application seed aulas
flask --app application seed questoes
flask --app application seed questoes_multipla_escolha
flask --app application seed exames
flask --app application seed respostas_questoes_exames
flask --app application seed notas_exames
```
