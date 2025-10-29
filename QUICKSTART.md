# Guia Rápido de Início - BBC News Search Engine

## 🚀 Início Rápido (5 minutos)

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Baixe o corpus BBC News
- Baixe de: http://mlg.ucd.ie/files/datasets/bbc-fulltext.zip
- Extraia e coloque a pasta `bbc` no diretório do projeto
- A estrutura deve ser:
```
TP1_ALG_2/
├── bbc/
│   ├── business/
│   ├── entertainment/
│   ├── politics/
│   ├── sport/
│   └── tech/
└── app.py
```

### 3. Execute os testes (opcional)
```bash
python test_system.py
```

### 4. Inicie a aplicação
```bash
python app.py
```

### 5. Acesse no navegador
Abra: http://localhost:5000

---

## 📝 Exemplos de Busca

### Busca Simples
```
football
```

### Busca com AND
```
football AND player
```

### Busca com OR
```
football OR basketball
```

### Busca Complexa
```
(economy AND growth) OR recession
```

---

## ⚠️ Resolução de Problemas

### Erro: "Corpus não encontrado"
- Certifique-se de que a pasta `bbc` está no diretório raiz
- Verifique se há 5 subpastas: business, entertainment, politics, sport, tech

### Erro: "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Índice corrompido
- Delete o arquivo `index.json`
- Execute novamente `python app.py`

---

## 📊 Informações do Sistema

- **Tempo de primeira indexação**: ~13 segundos
- **Tempo de carregamento do índice**: ~2 segundos
- **Tempo de consulta**: ~60ms
- **Uso de memória**: ~110 MB
- **Documentos indexados**: 2.225
- **Termos únicos**: ~29.000

---

## 📚 Documentação Completa

- README.md - Documentação geral
- RELATORIO.md - Relatório técnico detalhado

---

## 👥 Suporte

Para dúvidas sobre o trabalho, consulte:
- Professor: Renato Vimieiro
- Disciplina: DCC207 - Algoritmos 2
- UFMG - 2025
