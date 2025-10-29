"""
Script de Teste para a Trie Compacta e Índice Invertido
Algoritmos 2 - TP1
"""

from compact_trie import CompactTrie, TrieNode
from inverted_index import InvertedIndex
from query_processor import QueryProcessor


def test_compact_trie():
    """Testa funcionalidades básicas da Trie Compacta"""
    print("=== Testando Trie Compacta ===\n")
    
    trie = CompactTrie()
    
    # Teste 1: Inserção básica
    print("Teste 1: Inserção e busca básica")
    trie.insert("test", "doc1")
    trie.insert("testing", "doc2")
    trie.insert("tester", "doc3")
    
    result = trie.search("test")
    print(f"Busca por 'test': {result}")
    assert "doc1" in result, "Erro: doc1 deveria estar nos resultados"
    print("✓ Passou\n")
    
    # Teste 2: Busca por prefixo
    print("Teste 2: Busca por prefixo")
    result = trie.starts_with("test")
    print(f"Documentos com prefixo 'test': {result}")
    assert len(result) == 3, "Erro: deveria encontrar 3 documentos"
    print("✓ Passou\n")
    
    # Teste 3: Divisão de nós
    print("Teste 3: Divisão de nós")
    trie2 = CompactTrie()
    trie2.insert("testing", "doc1")
    trie2.insert("test", "doc2")
    
    result1 = trie2.search("test")
    result2 = trie2.search("testing")
    print(f"Busca por 'test': {result1}")
    print(f"Busca por 'testing': {result2}")
    assert "doc2" in result1 and len(result1) == 1
    assert "doc1" in result2 and len(result2) == 1
    print("✓ Passou\n")
    
    # Teste 4: Serialização
    print("Teste 4: Serialização e deserialização")
    trie_dict = trie.to_dict()
    trie_restored = CompactTrie.from_dict(trie_dict)
    
    result_original = trie.search("testing")
    result_restored = trie_restored.search("testing")
    print(f"Original: {result_original}")
    print(f"Restaurado: {result_restored}")
    assert result_original == result_restored
    print("✓ Passou\n")
    
    print("=== Todos os testes da Trie passaram! ===\n")


def test_query_processor():
    """Testa o processamento de consultas booleanas"""
    print("=== Testando Processamento de Consultas ===\n")
    
    # Cria um índice de teste
    index = InvertedIndex()
    
    # Simula alguns documentos
    index.documents = {
        "doc1": {"title": "Doc 1", "content": "economy growth", "category": "business", "path": ""},
        "doc2": {"title": "Doc 2", "content": "economy recession", "category": "business", "path": ""},
        "doc3": {"title": "Doc 3", "content": "growth market", "category": "business", "path": ""},
    }
    
    # Indexa manualmente
    index.trie.insert("economy", "doc1")
    index.trie.insert("growth", "doc1")
    index.trie.insert("economy", "doc2")
    index.trie.insert("recession", "doc2")
    index.trie.insert("growth", "doc3")
    index.trie.insert("market", "doc3")
    
    index.term_frequencies = {
        "doc1": {"economy": 1, "growth": 1},
        "doc2": {"economy": 1, "recession": 1},
        "doc3": {"growth": 1, "market": 1},
    }
    index.doc_lengths = {"doc1": 2, "doc2": 2, "doc3": 2}
    index.corpus_term_freq = {"economy": 2, "growth": 2, "recession": 1, "market": 1}
    index.total_docs = 3
    
    processor = QueryProcessor(index)
    
    # Teste 1: Busca simples
    print("Teste 1: Busca simples")
    results = processor.process_query("economy")
    print(f"Consulta 'economy': {[r[0] for r in results]}")
    assert len(results) == 2, "Deveria encontrar 2 documentos"
    print("✓ Passou\n")
    
    # Teste 2: AND
    print("Teste 2: Operador AND")
    results = processor.process_query("economy AND growth")
    print(f"Consulta 'economy AND growth': {[r[0] for r in results]}")
    assert len(results) == 1 and results[0][0] == "doc1"
    print("✓ Passou\n")
    
    # Teste 3: OR
    print("Teste 3: Operador OR")
    results = processor.process_query("economy OR market")
    print(f"Consulta 'economy OR market': {[r[0] for r in results]}")
    assert len(results) == 3, "Deveria encontrar 3 documentos"
    print("✓ Passou\n")
    
    # Teste 4: Parênteses
    print("Teste 4: Consulta com parênteses")
    results = processor.process_query("(economy AND growth) OR market")
    print(f"Consulta '(economy AND growth) OR market': {[r[0] for r in results]}")
    assert len(results) == 2, "Deveria encontrar 2 documentos"
    print("✓ Passou\n")
    
    print("=== Todos os testes de consulta passaram! ===\n")


def main():
    """Executa todos os testes"""
    print("\n" + "="*50)
    print("TESTES DO SISTEMA DE BUSCA BBC NEWS")
    print("="*50 + "\n")
    
    try:
        test_compact_trie()
        test_query_processor()
        
        print("\n" + "="*50)
        print("✓✓✓ TODOS OS TESTES PASSARAM! ✓✓✓")
        print("="*50 + "\n")
        
    except AssertionError as e:
        print(f"\n✗ ERRO NO TESTE: {e}\n")
        return 1
    except Exception as e:
        print(f"\n✗ ERRO INESPERADO: {e}\n")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
