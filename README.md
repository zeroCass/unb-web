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
O projeto UNB WEB SAAS tem como objetivo de ser um Software as a Service que possibilite o professor crie turmas e aulas para que seu estudantes assinem a chamada. O aplicativo pretende fazer isso por meio da geração de um QRCODE único para cada aula. Com seu smartphone o estudante irá escanear esse QRCODE provido pelo professor e então será capaz de assinar a chamada. Além disso, os estudantes também podem responder e revisar exames elaboradas pelos professores, promovendo um ambiente interativo de aprendizado.

## Como Usar

Por padrão, existem alguns usuários pré-cadastrados para facilitar a testagem da aplicação.
Login com Estudante:
Email -> ester@unb.com
Password -> asdfg
Login com Professor:
Email -> 456@unb.com
Password -> 123

Ao acessar a aplicação web na página inicial, você normalmente verá opções para "Login" ou "Registrar-se" logo abaixo.
- Na tela de login, insira seu endereço de e-mail e senha nos campos apropriados. Clique no botão "Entrar" para fazer login na conta que deseja. Se as informações estiverem corretas, você será redirecionado para a página principal.
    
  ![Login](https://i.imgur.com/CrlhwrR.gif)

- Clique na opção "Registrar-se" se você ainda não tem uma conta na aplicação. Após preencher todos os campos necessários, clique em "Registrar" para criar sua conta. Se todas as informações estiverem corretas, você será redirecionado logado automaticamente na aplicação.

  ![Registrar](https://i.imgur.com/l9wZpjA.gif)

Agora que você está logado, você pode começar a explorar as diferentes funcionalidades da aplicação web. Vamos começar exemplificando o caso de um usuário do tipo professor:
- A primeira coisa a se fazer e criar uma turma na qual estará lecionando, para fazer isso no menu no topo da aplicação tem uma opção chamada "Turmas". Ao clicar nela você pode ver todas as turmas lecionadas, tanto por você quanto por outros. Contudo, no canto inferior direito há um botão "Adicionar Turma", ao clicar nele você é redirecionado a uma página na qual devera preencher todos os campos necessários para a criação da turma, e por fim clicar em "Criar Turma".
  
  ![Registrar](https://i.imgur.com/mc9c1I0.gif)
  
- O professor também pode montar um banco de questões, assim como para turmas no menu no topo da aplicação tem uma opção chamada "Questões". Lá o professor pode ver todas as questões criadas por ele e pode criar questões com um botão localizado também no canto inferior direito. O processo para criação é similar aos já citados aqui.

  ![Questao](https://i.imgur.com/HiwE6Q9.gif)

  Além disso, o professor pode montar questões diferentes, com base no tipo de questão que ele seleciona na hora da aplicação.
  
  ![Tipo_Questao](https://i.imgur.com/NRrCN6Z.gif)
  
- O professor pode acessar a página da turma na qual leciona clicando no nome da mesma, seja na página home onde lista todas as turmas dele ou na página de turmas. Ao acessar esta pagina o professor pode criar um exame clicando no botão "Criar Exame", no canto inferior direito.

  ![Exame](https://i.imgur.com/hjU3UX2.gif)
  
  Ao fazer isso ele é redirecionado para uma página onde precisa preencher com as informações necessárias para criar um exame e selecionar quais questões do banco de questões dele ele quer neste exame. Depois ele atribui uma nota para cada questão, que sera somada como a nota total do exame e assim pode clicar em "Criar Exame" para concluir.

- Caso o professor queira ver a nota dos estudantes e também revisar as respostas dos mesmos, la na página da turma, onde mostra os exames, terá um botão com os dizeres "Notas", ao clicar nele você será redirecionado a uma página listando o nome, matricula e nota de todos os estudantes que realizaram o exame.

  ![Notas](https://i.imgur.com/JQ0GdwE.gif)
  
  Ao clicar no nome do estudante que deseja, ele vera todas as respostas do estudante para cada questão do exame.
  
Já o caso de um usuário do tipo estudante:
- Assim como professor você pode acessar a página de turmas, a diferença é que ao invés de criar uma você se matricula nela. Ao clicar no nome da Turma que deseja se matricular seja pedido uma senha de acesso para a mesma, após preencher com a senha correta o estudante é matriculado na turma e pode acessá-la normalmente.
  
  ![Matricula](https://i.imgur.com/Go2g4nZ.gif)

- Após se matricular em uma turma, em home você vera todas as turmas na qual você estudante está agora vinculado. Ao clicar no nome da mesma você é redirecionado para a página da turma onde terão disponíveis todos os exames vinculados a turma, para realizar o exame basta clicar no nome do mesmo.
  
  ![Realiza-Exame](https://i.imgur.com/efPTgHa.gif)
  
  Em seguida é só realizar o exame e por fim concluir o mesmo.

- Após ter concluído um exame, você pode revisar sua nota e o que errou/acertou seguindo o mesmo processo para realizá-la. O sistema identifica que você já a realizou e te mostra um relatório com suas respostas.

   ![Revisa-Exame](https://i.imgur.com/neZdlUO.gif)
  
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
