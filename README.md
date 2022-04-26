# mini-c-compiler

## Introdução
Este repositório consiste num compilador genérico, em que as suas regras
estarão contidas no arquivo de configuração (*aka* config.py)

## Como usar
Escrito em Python 3, para utilizá-lo basta digitar em seu terminal
```shell
python3 compiler.py arquivo_entrada
```

Este programa também possui duas *flags* que podem ser utilizadas:

- <code>-o output_file</code>: nome do arquivo de saída. Caso não seja especificado nenhum 
nome, será utilizado o nome do arquivo de saída com a sua extensão <code>.out</code>
- <code>-conf</code>: Nome do arquivo usado para configuração do compilador. Caso não seja
especificado, um arquivo chamado config.json será utilizado como padrão.

É importante avisar que, como o compilador não possui nenhuma regra além de que os operadores
lógico/aritméticos tenham no máximo dois caracteres, o arquivo de configuração se faz 
**necessário** para o funcionamento do programa.

### Arquivo de configuração
Neste repositório existe um arquivo de configuração padrão de mini-c, mas é possível editá-lo 
para compilar sua própria linguagem.

No arquivo, temos o objeto
```json
{
  "tokens": [
    ...
  ]
}
```

E os tokens necessários para o funcionamento são:
1. arith_op (operadores aritméticos);
2. log_op (operadores lógicos);
3. sep (separadores);
4. block_sep (separadores de bloco);
5. comment (comentários);
6. number (literais numéricos);
7. identifier (identificadores) e
8. reserved_keywords (palavras reservadas).

Cada um dos tokens são objetos que contém:
```json
{
  "regex": "string",
  "tokens" : []
}
```
Onde o campo *regex* é uma expressão regular para identificação deste token e 
o campo *tokens* é uma lista com os tokens que podem ser utilizados. Este último campo
pode ser removido caso não exista uma lista pré-definida (por exemplo, a lista de identificadores)
