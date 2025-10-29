"""
Módulo de Índice Invertido
Utiliza a Trie Compacta para armazenar o índice invertido dos documentos.
"""

import os
import re
import json
from compact_trie import CompactTrie


class InvertedIndex:
    def __init__(self):
        self.trie = CompactTrie()
        self.documents = {}  # {doc_id: {'title': str, 'content': str, 'category': str, 'path': str}}
        self.term_frequencies = {}  # {doc_id: {term: frequency}}
        self.doc_lengths = {}  # {doc_id: número de termos}
        self.corpus_term_freq = {}  # {term: frequência total no corpus}
        self.total_docs = 0
    
    def index_documents(self, corpus_path):
        print("Iniciando indexação dos documentos...")
        
        # Itera por todas as categorias (pastas)
        for category in os.listdir(corpus_path):
            category_path = os.path.join(corpus_path, category)
            
            if not os.path.isdir(category_path):
                continue
            
            print(f"Processando categoria: {category}")
            
            # Itera por todos os documentos da categoria
            for filename in os.listdir(category_path):
                if not filename.endswith('.txt'):
                    continue
                
                doc_path = os.path.join(category_path, filename)
                doc_id = f"{category}/{filename}"
                
                # Lê o documento
                with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Primeira linha é o título
                lines = content.split('\n', 1)
                title = lines[0].strip() if lines else ""
                content = lines[1] if len(lines) > 1 else ""
                
                # Armazena informações do documento
                self.documents[doc_id] = {
                    'title': title,
                    'content': content,
                    'category': category,
                    'path': doc_path
                }
                
                # Processa e indexa os termos
                terms = self._tokenize(content)
                self._index_document_terms(doc_id, terms)
                
                self.total_docs += 1
        
        print(f"Indexação concluída! Total de documentos: {self.total_docs}")
        print(f"Total de termos únicos: {len(self.corpus_term_freq)}")
    
    def _tokenize(self, text):
        # Remove pontuação e converte para minúsculas
        text = text.lower()
        # Mantém apenas letras e números
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens
    
    def _index_document_terms(self, doc_id, terms):
        # Conta a frequência dos termos
        term_freq = {}
        for term in terms:
            term_freq[term] = term_freq.get(term, 0) + 1
        
        self.term_frequencies[doc_id] = term_freq
        self.doc_lengths[doc_id] = len(terms)
        
        # Insere cada termo único na Trie
        for term in term_freq.keys():
            self.trie.insert(term, doc_id)
            self.corpus_term_freq[term] = self.corpus_term_freq.get(term, 0) + term_freq[term]
    
    def search_term(self, term):
        return self.trie.search(term)
    
    def get_term_frequency(self, doc_id, term):
        term = term.lower()
        if doc_id in self.term_frequencies:
            return self.term_frequencies[doc_id].get(term, 0)
        return 0
    
    def get_document(self, doc_id):
        return self.documents.get(doc_id)
    
    def save_index(self, index_path):
        print(f"Salvando índice em {index_path}...")
        
        # Serializa a estrutura completa
        index_data = {
            'trie': self.trie.to_dict(),
            'documents': self.documents,
            'term_frequencies': self.term_frequencies,
            'doc_lengths': self.doc_lengths,
            'corpus_term_freq': self.corpus_term_freq,
            'total_docs': self.total_docs
        }
        
        # Salva em formato JSON
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
        
        print("Índice salvo com sucesso!")
    
    def load_index(self, index_path):
        if not os.path.exists(index_path):
            return False
        
        print(f"Carregando índice de {index_path}...")
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            # Reconstrói a Trie
            self.trie = CompactTrie.from_dict(index_data['trie'])
            self.documents = index_data['documents']
            self.term_frequencies = index_data['term_frequencies']
            self.doc_lengths = index_data['doc_lengths']
            self.corpus_term_freq = index_data['corpus_term_freq']
            self.total_docs = index_data['total_docs']
            
            print(f"Índice carregado com sucesso! Total de documentos: {self.total_docs}")
            return True
        
        except Exception as e:
            print(f"Erro ao carregar índice: {e}")
            return False
    
    def get_statistics(self):
        return {
            'total_documents': self.total_docs,
            'unique_terms': len(self.corpus_term_freq),
            'total_terms': sum(self.corpus_term_freq.values()),
            'avg_doc_length': sum(self.doc_lengths.values()) / self.total_docs if self.total_docs > 0 else 0
        }
