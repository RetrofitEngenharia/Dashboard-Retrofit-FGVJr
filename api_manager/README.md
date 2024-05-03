# API manager

Esse módulo é responsável por atualizar diariamente a planilha de dados do projeto. A decisão de se utilizar uma planilha e não apenas fazer as requisições em tempo de execução tem dois motivos principais:

1. O tempo de request dos dados no Google Sheets é extremamente mais rápido se comparado com a API do Sienge;

2. O volume de dados e a necessidade de dados redundantes que poderiam ser salvos em cache levaria a uma solução parecida, mas local.

Com essas considerações, apenas esse módulo terá permissão de altera a planilha.

Prezou-se que todas as classes e funções fossem bem documentadas para fins de posterior manutenção.

Além disso, existe uma pasta de log, na qual diariamente será salvo um registro das atividades executadas para posterior verificação e debug.

## Sheets

A classe `Sheets` é responsável por salvar e obter dados da planilha utilizando uma conta de serviço do google cloud e é construida em cima do `pygsheets` que é uma abstração da API disponibilizada pela Google.

## Sienge

Essa classe lida com as requisições de dados direto na API da sienge e prioriza sempre a utilização do `bulk` devido ao grande volume de dados. Foram criados acessos apenas aos endpoints que serão utilizados nesse projeto.