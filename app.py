"""
Aplicação Flask para Máquina de Busca
Algoritmos 2 - TP1
"""

from flask import Flask, render_template, request, jsonify
import os
from inverted_index import InvertedIndex
from query_processor import QueryProcessor

app = Flask(__name__)

# Variáveis globais
index = InvertedIndex()
query_processor = None

# Configurações
CORPUS_PATH = 'bbc'  # Pasta onde está o corpus BBC
INDEX_PATH = 'index.json'  # Arquivo onde o índice será salvo
RESULTS_PER_PAGE = 10


def initialize_index():
    """Inicializa ou carrega o índice invertido"""
    global query_processor
    
    # Tenta carregar o índice do disco
    if os.path.exists(INDEX_PATH):
        print("Índice encontrado, carregando...")
        if index.load_index(INDEX_PATH):
            print("Índice carregado com sucesso!")
        else:
            print("Erro ao carregar índice, criando novo...")
            create_new_index()
    else:
        # Cria um novo índice
        print("Índice não encontrado, criando novo...")
        create_new_index()
    
    # Inicializa o QueryProcessor
    query_processor = QueryProcessor(index)
    
    # Estatísticas
    stats = index.get_statistics()
    print("\n=== Estatísticas do Índice ===")
    print(f"Total de documentos: {stats['total_documents']}")
    print(f"Termos únicos: {stats['unique_terms']}")
    print(f"Total de termos: {stats['total_terms']}")
    print(f"Média de termos por documento: {stats['avg_doc_length']:.2f}")
    print("================================\n")


def create_new_index():
    """Cria um novo índice a partir do corpus"""
    if not os.path.exists(CORPUS_PATH):
        print(f"ERRO: Corpus não encontrado em '{CORPUS_PATH}'")
        print("Por favor, baixe o corpus BBC e extraia na pasta 'bbc'")
        return
    
    # Indexa os documentos
    index.index_documents(CORPUS_PATH)
    
    # Salva o índice em disco
    index.save_index(INDEX_PATH)


@app.route('/')
def home():
    """Página inicial"""
    stats = index.get_statistics()
    return render_template('index.html', stats=stats)


@app.route('/search')
def search():
    """Processa a busca e retorna resultados"""
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    
    if not query:
        return render_template('results.html', 
                             query='', 
                             results=[], 
                             total_results=0,
                             page=1,
                             total_pages=0)
    
    # Faz a consulta
    results = query_processor.process_query(query)
    
    # Extrai termos da consulta
    query_terms = query_processor._extract_terms(query)
    
    # Prepara os resultados com informações completas
    detailed_results = []
    for doc_id, score in results:
        doc = index.get_document(doc_id)
        if doc:
            snippet = query_processor.generate_snippet(doc_id, query_terms)
            detailed_results.append({
                'doc_id': doc_id,
                'title': doc['title'],
                'category': doc['category'],
                'snippet': snippet,
                'score': score
            })
    
    # Paginação
    total_results = len(detailed_results)
    total_pages = (total_results + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
    
    start_idx = (page - 1) * RESULTS_PER_PAGE
    end_idx = start_idx + RESULTS_PER_PAGE
    paginated_results = detailed_results[start_idx:end_idx]
    
    return render_template('results.html',
                         query=query,
                         results=paginated_results,
                         total_results=total_results,
                         page=page,
                         total_pages=total_pages)


@app.route('/document/<path:doc_id>')
def view_document(doc_id):
    """Exibe um documento completo"""
    doc = index.get_document(doc_id)
    
    if not doc:
        return "Documento não encontrado", 404
    
    return render_template('document.html', doc=doc, doc_id=doc_id)


@app.route('/api/search')
def api_search():
    """API endpoint para busca (retorna JSON)"""
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    
    if not query:
        return jsonify({
            'query': '',
            'results': [],
            'total_results': 0,
            'page': 1,
            'total_pages': 0
        })
    
    
    results = query_processor.process_query(query)
    query_terms = query_processor._extract_terms(query)
    
    
    detailed_results = []
    for doc_id, score in results:
        doc = index.get_document(doc_id)
        if doc:
            snippet = query_processor.generate_snippet(doc_id, query_terms)
            detailed_results.append({
                'doc_id': doc_id,
                'title': doc['title'],
                'category': doc['category'],
                'snippet': snippet,
                'score': score
            })
    
    total_results = len(detailed_results)
    total_pages = (total_results + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
    
    start_idx = (page - 1) * RESULTS_PER_PAGE
    end_idx = start_idx + RESULTS_PER_PAGE
    paginated_results = detailed_results[start_idx:end_idx]
    
    return jsonify({
        'query': query,
        'results': paginated_results,
        'total_results': total_results,
        'page': page,
        'total_pages': total_pages
    })


@app.route('/api/stats')
def api_stats():
    """API endpoint para estatísticas do índice"""
    stats = index.get_statistics()
    return jsonify(stats)


if __name__ == '__main__':
    print("=== Máquina de Busca BBC News ===")
    print("Inicializando...")
    
    # Inicializa o índice
    initialize_index()
    
    print("Iniciando servidor Flask...")
    print("Acesse: http://localhost:5000")
    print("================================\n")
    
    # Inicia o servidor
    app.run(debug=True, host='0.0.0.0', port=5000)
