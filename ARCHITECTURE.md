# Arquitetura do Sistema - BBC News Search Engine

```
┌─────────────────────────────────────────────────────────────────┐
│                         FLASK APPLICATION                        │
│                            (app.py)                              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
    ┌─────────────┐ ┌──────────────┐ ┌──────────────┐
    │   Routes    │ │  Templates   │ │     APIs     │
    │             │ │              │ │              │
    │ / (home)    │ │ base.html    │ │ /api/search  │
    │ /search     │ │ index.html   │ │ /api/stats   │
    │ /document   │ │ results.html │ └──────────────┘
    │             │ │ document.html│
    └──────┬──────┘ └──────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────────┐
│                      QUERY PROCESSOR                              │
│                    (query_processor.py)                           │
│                                                                   │
│  • Parse consultas booleanas                                      │
│  • Algoritmo Shunting Yard                                        │
│  • Avaliação RPN                                                  │
│  • Cálculo de z-scores                                            │
│  • Geração de snippets                                            │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                      INVERTED INDEX                               │
│                    (inverted_index.py)                            │
│                                                                   │
│  • Indexação de documentos                                        │
│  • Tokenização                                                    │
│  • Estatísticas do corpus                                         │
│  • Persistência em JSON                                           │
│  • Carregamento do índice                                         │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                      COMPACT TRIE                                 │
│                    (compact_trie.py)                              │
│                                                                   │
│  • Estrutura de dados principal                                   │
│  • Inserção com divisão de nós                                    │
│  • Busca exata                                                    │
│  • Busca por prefixo                                              │
│  • Serialização/deserialização                                    │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   index.json  │
                    │   (Disk)      │
                    └───────────────┘
```

## Fluxo de Dados

### 1. Inicialização

```
┌─────────────┐
│ app.py      │
│ startup     │
└──────┬──────┘
       │
       ├─── Arquivo index.json existe?
       │    │
       │    ├── SIM ──▶ Carregar índice do disco
       │    │           (inverted_index.load_index)
       │    │
       │    └── NÃO ──▶ Criar novo índice
       │                │
       │                ├─ Ler documentos do corpus BBC
       │                ├─ Tokenizar cada documento
       │                ├─ Inserir termos na Trie
       │                └─ Salvar índice em disco
       │
       └─── Inicializar QueryProcessor
```

### 2. Processamento de Consulta

```
┌──────────────────┐
│ User Query       │
│ "(economy AND    │
│  growth) OR      │
│  recession"      │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ STEP 1: Tokenização                     │
│ ['(', 'economy', 'AND', 'growth',       │
│  ')', 'OR', 'recession']                │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ STEP 2: Conversão para RPN              │
│ (Shunting Yard Algorithm)               │
│ ['economy', 'growth', 'AND',            │
│  'recession', 'OR']                     │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ STEP 3: Avaliação da RPN                │
│ - economy → {doc1, doc5, doc7, ...}     │
│ - growth → {doc1, doc3, doc9, ...}      │
│ - AND → {doc1, ...}                     │
│ - recession → {doc2, doc4, ...}         │
│ - OR → {doc1, doc2, doc4, ...}          │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ STEP 4: Cálculo de Relevância           │
│ Para cada documento:                    │
│   - Calcular z-score para cada termo    │
│   - Média dos z-scores                  │
│   - Ordenar por score (decrescente)     │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ STEP 5: Geração de Snippets             │
│ Para cada resultado:                    │
│   - Encontrar termo mais relevante      │
│   - Extrair 80 chars antes/depois       │
│   - Destacar termo com <mark>           │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ STEP 6: Paginação                       │
│ - Dividir em páginas de 10              │
│ - Retornar página solicitada            │
└────────┬────────────────────────────────┘
         │
         ▼
┌──────────────────┐
│ Results Page     │
│ (HTML)           │
└──────────────────┘
```

### 3. Estrutura da Trie Compacta

```
Exemplo: Inserção de "test", "testing", "tester", "team"

Trie Tradicional:                Trie Compacta:
    root                             root
     |                                |
     t                               "te"
     |                            /       \
     e                          "st"     "am"
     |                          / |  \     |
   s   a                      ø "ing" "er" ø
   |   |                        |     |
   t   m                        ø     ø
   |   |
   ø   ø           ø = fim de palavra
  /|\
ing er

Nós: 17                          Nós: 7
Redução: ~60%
```

### 4. Cálculo de Z-Score

```
Documento: "The economy is growing. Economy shows growth."
Termo: "economy"

┌─────────────────────────────────────────────────┐
│ Frequência no documento: 2                      │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ Frequência média no corpus:                     │
│ (Total de "economy" no corpus) / (Total docs)   │
│ = 450 / 2225 = 0.202                           │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ Calcular variância:                             │
│ Σ(freq_doc - média)² / total_docs              │
│ = 0.412                                         │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ Desvio padrão: √variância = 0.642               │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ Z-score = (2 - 0.202) / 0.642 = 2.80           │
│ (Alto z-score = alta relevância)                │
└─────────────────────────────────────────────────┘
```

## Estrutura de Dados em Memória

```
InvertedIndex
├── trie: CompactTrie
│   └── root: TrieNode
│       ├── prefix: ""
│       ├── children: {
│       │   'a': TrieNode("about", docs={1,5,7}),
│       │   'b': TrieNode("b", children={
│       │       'u': TrieNode("usiness", docs={2,8}),
│       │       'a': TrieNode("all", docs={3,9})
│       │   }),
│       │   ...
│       │}
│       ├── documents: set()
│       └── is_end_of_word: False
│
├── documents: {
│   "business/001.txt": {
│       "title": "Economy grows",
│       "content": "The economy...",
│       "category": "business",
│       "path": "/path/to/file"
│   },
│   ...
│}
│
├── term_frequencies: {
│   "business/001.txt": {
│       "economy": 5,
│       "growth": 3,
│       ...
│   },
│   ...
│}
│
├── doc_lengths: {
│   "business/001.txt": 450,
│   ...
│}
│
├── corpus_term_freq: {
│   "economy": 450,
│   "growth": 320,
│   ...
│}
│
└── total_docs: 2225
```

## Formato JSON de Persistência

```json
{
  "trie": {
    "root": {
      "prefix": "",
      "children": {
        "a": {
          "prefix": "about",
          "children": {},
          "documents": [1, 5, 7],
          "is_end_of_word": true
        },
        ...
      },
      "documents": [],
      "is_end_of_word": false
    }
  },
  "documents": {
    "business/001.txt": {
      "title": "Economy grows",
      "content": "Full text...",
      "category": "business",
      "path": "/path/to/file"
    }
  },
  "term_frequencies": {...},
  "doc_lengths": {...},
  "corpus_term_freq": {...},
  "total_docs": 2225
}
```

## Interface do Usuário - Fluxo

```
┌────────────────────────────────────────┐
│         PÁGINA INICIAL                 │
│                                        │
│  [Buscar: _______________] [🔍 Buscar] │
│                                        │
│  Como usar:                            │
│  • Busca simples                       │
│  • AND / OR / ()                       │
│                                        │
│  Estatísticas:                         │
│  ┌──────┐ ┌──────┐ ┌──────┐           │
│  │ 2225 │ │29158 │ │ 1.0M │           │
│  │ Docs │ │Terms │ │Total │           │
│  └──────┘ └──────┘ └──────┘           │
└────────────────────────────────────────┘
                 │
                 │ User types: "economy AND growth"
                 ▼
┌────────────────────────────────────────┐
│      PÁGINA DE RESULTADOS              │
│                                        │
│  [Buscar: economy AND growth] [🔍]     │
│                                        │
│  87 resultados (Página 1 de 9)         │
│                                        │
│  ┌──────────────────────────────────┐ │
│  │ [business] UK Economy Report      │ │
│  │ ...shows strong economy and       │ │
│  │ consistent growth in the...       │ │
│  │ Relevância: 3.45                  │ │
│  └──────────────────────────────────┘ │
│                                        │
│  ┌──────────────────────────────────┐ │
│  │ [business] Growth Forecast        │ │
│  │ ...predict economic growth...     │ │
│  │ Relevância: 2.98                  │ │
│  └──────────────────────────────────┘ │
│                                        │
│  [1] 2 3 4 5 ... 9 [Próxima]          │
└────────────────────────────────────────┘
                 │
                 │ User clicks result
                 ▼
┌────────────────────────────────────────┐
│      DOCUMENTO COMPLETO                │
│                                        │
│  ← Voltar                              │
│                                        │
│  [business]                            │
│                                        │
│  UK Economy Report                     │
│                                        │
│  ID: business/001.txt                  │
│                                        │
│  The economy showed strong growth      │
│  in the third quarter, with GDP        │
│  increasing by 2.3%...                 │
│  [Full content displayed]              │
└────────────────────────────────────────┘
```

---

Este diagrama mostra como todos os componentes se conectam e trabalham juntos!
