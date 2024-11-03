# Bot de Download de XML da NF-e
Um bot automatizado para acessar o portal da SEFAZ, preencher o formulário de Download XML da NF-e e baixar o XML, utilizando dados extraídos de uma planilha Excel.

Índice
Sobre o Projeto
Funcionalidades
Instalação
Como Usar
Tecnologias Utilizadas
Contribuição
Licença
Contato
Sobre o Projeto
Este projeto é um bot desenvolvido em Python com o framework BotCity, projetado para automatizar o processo de download de XML da NF-e no portal da SEFAZ. Ele navega até a seção de Download XML da NF-e, preenche o formulário automaticamente com os dados da planilha Excel e realiza o download dos arquivos XML.

Funcionalidades
Acessa automaticamente o portal da SEFAZ e navega até a seção de Download XML da NF-e.
Preenche o formulário com dados extraídos de uma planilha Excel localizada na pasta resources.
Realiza o download dos arquivos XML de forma automatizada.

Instalação
Clone o repositório:
git clone https://github.com/seu-usuario/nome-do-repositorio.git

Entre no diretório do projeto:
cd nome-do-repositorio

Instale as dependências do projeto com o seguinte comando:
pip install -r requirements.txt

Todas as dependências de framework estão listadas no arquivo requirements.txt. Esse comando instalará automaticamente BotCity, Pandas, OpenPyXL, Tkinter, entre outras necessárias.

Como Usar
Abra o terminal na pasta do projeto.

Execute o bot com o comando:
python main.py

Nota: Certifique-se de que a planilha com as informações está na pasta resources e devidamente preenchida para que o bot possa extrair os dados.

Tecnologias Utilizadas:
BotCity
Pandas
OpenPyXL
Tkinter
Contribuição
Faça um fork do projeto.
Crie uma branch para sua funcionalidade (git checkout -b minha-nova-funcionalidade).
Faça o commit (git commit -m 'Adiciona nova funcionalidade').
Faça o push para a branch (git push origin minha-nova-funcionalidade).
Abra um Pull Request.
