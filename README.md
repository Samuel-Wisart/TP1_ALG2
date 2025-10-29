# Máquina de Busca BBC News

## Trabalho Prático 1 - DCC207 Algoritmos 2
**Universidade Federal de Minas Gerais**  
**Prof. Renato Vimieiro**

---

| Autores                     | Matrícula   |
|-----------------------------------|--------------|
| **Samuel Lucca Viana Miranda**    | 2022043566   |
| **Layla Raissa**     | XXXXXXXXXX |

---

## Descrição do Projeto

Este projeto implementa um **protótipo de máquina de busca** para o corpus de notícias da BBC News. A implementação utiliza uma **Trie Compacta (Patricia Trie)** para construir um **índice invertido**, permitindo buscas booleanas eficientes com ordenação por relevância.

### Funcionalidades Implementadas

- **Trie Compacta**: Estrutura de dados implementada do zero para armazenamento eficiente do índice invertido
- **Índice Invertido**: Associa termos aos documentos onde aparecem
- **Persistência em Disco**: Salva e carrega o índice em formato JSON customizado
- **Consultas Booleanas**: Suporte para operadores `AND`, `OR` e parênteses
- **Ranking por Relevância**: Ordenação dos resultados usando z-scores
- **Geração de Snippets**: Exibe trechos dos documentos com os termos destacados
- **Interface Web**: Aplicação Flask com design moderno e responsivo
- **Paginação**: Exibição de 10 resultados por página

---

## Arquitetura do Sistema

### Módulos Implementados

1. **`compact_trie.py`**: Implementação da Trie Compacta
   - Classe `TrieNode`: Representa um nó da Trie
   - Classe `CompactTrie`: Estrutura principal com operações de inserção, busca e serialização

2. **`inverted_index.py`**: Módulo de índice invertido
   - Utiliza a Trie Compacta para armazenar termos
   - Mantém estatísticas de frequência de termos
   - Funções para indexação, carregamento e salvamento

3. **`query_processor.py`**: Processamento de consultas
   - Parser de expressões booleanas
   - Avaliação usando algoritmo Shunting Yard (notação polonesa reversa)
   - Cálculo de relevância com z-scores
   - Geração de snippets

4. **`app.py`**: Aplicação Flask
   - Rotas para busca, visualização de documentos e APIs
   - Interface web responsiva

---

## Como Executar

### Pré-requisitos

- Python 3.9 ou superior
- Bibliotecas do requirements.txt instaladas

### Passo 1: Clone o repositório

```bash
git clone git@github.com:Samuel-Wisart/TP1_ALG2.git
cd TP1_ALG_2
```

### Passo 2: Instale as dependências

```bash
pip install -r requirements.txt
```

### Passo 3: Baixe o corpus BBC News

1. Baixe o corpus do link: http://mlg.ucd.ie/files/datasets/bbc-fulltext.zip
2. Extraia o arquivo ZIP
3. Copie a pasta `bbc` (contendo as subpastas business, entertainment, politics, sport, tech) para o diretório raiz do projeto

A estrutura deve ficar assim:
```
TP1_ALG_2/
├── bbc/
│   ├── business/
│   ├── entertainment/
│   ├── politics/
│   ├── sport/
│   └── tech/
├── app.py
├── ...
```

### Passo 4: Execute a aplicação

```bash
python app.py
```

Na primeira execução, o sistema irá:
1. Ler todos os documentos do corpus
2. Construir o índice invertido usando a Trie Compacta
3. Salvar o índice em disco (`index.json`)

Nas execuções seguintes, o índice será carregado do disco, tornando a inicialização mais rápida.

### Passo 5: Acesse a aplicação

Abra seu navegador e acesse:
```
http://localhost:5000
```

---

## Como Usar

### Exemplos de Consultas

1. **Busca simples**:
   ```
   football
   ```
   Retorna todos os documentos que contêm a palavra "football"

2. **Busca com AND**:
   ```
   football AND player
   ```
   Retorna documentos que contêm ambas as palavras

3. **Busca com OR**:
   ```
   football OR basketball
   ```
   Retorna documentos que contêm qualquer uma das palavras

4. **Busca complexa com parênteses**:
   ```
   (economy AND growth) OR recession
   ```
   Retorna documentos que contêm "economy" E "growth", OU que contêm "recession"

### Navegação

- **Página inicial**: Exibe estatísticas do corpus e campo de busca
- **Página de resultados**: Lista paginada com 10 resultados por página
- **Visualização de documento**: Exibe o conteúdo completo de um documento

---

## Detalhes de Implementação

### Trie Compacta

A Trie Compacta é uma otimização da Trie tradicional onde cadeias de nós com um único filho são compactadas em um único nó. Isso reduz significativamente o uso de memória.

**Características**:
- Cada nó armazena um prefixo (string) em vez de um único caractere
- Nós são divididos quando há bifurcação no caminho
- Suporta inserção, busca exata e busca por prefixo

### Cálculo de Relevância (Z-Score)

A relevância de um documento para uma consulta é calculada como a **média dos z-scores** dos termos da consulta.

O z-score de um termo em um documento mede o quão atípica é a frequência desse termo no documento em relação ao corpus

Documentos com z-scores maiores são considerados mais relevantes.

### Processamento de Consultas Booleanas

O sistema utiliza o algoritmo Shunting Yard para converter expressões booleanas em notação polonesa reversa (RPN) e depois avalia a expressão usando uma pilha:

1. Tokeniza a consulta
2. Converte para RPN respeitando precedência (AND > OR)
3. Avalia a RPN usando operações de conjunto (interseção para AND, união para OR)

### Formato de Persistência

O índice é salvo em formato JSON com a seguinte estrutura:
- Serialização recursiva da Trie
- Metadados dos documentos
- Frequências de termos
- Estatísticas do corpus

**Decisão**: Optamos por JSON devido à facilidade de debug e portabilidade, mantendo boa performance.

---

## Estatísticas do Corpus BBC

- **Total de documentos**: 2.225
- **Categorias**: 5 (business, entertainment, politics, sport, tech)
- **Termos únicos**: ~29.000
- **Total de termos**: ~1.000.000

---

## Tecnologias Utilizadas

- **Python 3.9+**: Linguagem de programação
- **Flask**: Framework web
- **JSON**: Formato de persistência do índice
- **HTML/CSS**: Interface do usuário
