"""
Módulo de Recuperação de Informação
Processa consultas booleanas e retorna resultados ordenados por relevância.
Algoritmos 2 - TP1
"""

import re
import math
from inverted_index import InvertedIndex


class QueryProcessor:
    """
    Processa consultas booleanas e retorna documentos relevantes.
    
    Suporta operadores AND, OR e parênteses para controle de precedência.
    """
    
    def __init__(self, inverted_index):
        """
        Inicializa o processador de consultas.
        
        Args:
            inverted_index (InvertedIndex): Índice invertido
        """
        self.index = inverted_index
    
    def process_query(self, query_string):
        """
        Processa uma consulta booleana e retorna documentos relevantes.
        
        Args:
            query_string (str): String de consulta
            
        Returns:
            list: Lista de tuplas (doc_id, relevance_score)
        """
        # Parse da consulta
        doc_ids = self._evaluate_query(query_string)
        
        if not doc_ids:
            return []
        
        # Calcula relevância para cada documento
        query_terms = self._extract_terms(query_string)
        scored_docs = []
        
        for doc_id in doc_ids:
            score = self._calculate_relevance(doc_id, query_terms)
            scored_docs.append((doc_id, score))
        
        # Ordena por relevância (decrescente)
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        return scored_docs
    
    def _evaluate_query(self, query_string):
        """
        Avalia a expressão booleana da consulta.
        
        Args:
            query_string (str): String de consulta
            
        Returns:
            set: Conjunto de IDs de documentos
        """
        # Tokeniza a consulta
        tokens = self._tokenize_query(query_string)
        
        # Avalia a expressão usando pilhas
        return self._evaluate_tokens(tokens)
    
    def _tokenize_query(self, query_string):
        """
        Tokeniza a consulta em termos e operadores.
        
        Args:
            query_string (str): String de consulta
            
        Returns:
            list: Lista de tokens
        """
        # Pattern para capturar termos, operadores AND/OR e parênteses
        pattern = r'\(|\)|AND|OR|[a-zA-Z0-9]+'
        tokens = re.findall(pattern, query_string)
        return tokens
    
    def _evaluate_tokens(self, tokens):
        """
        Avalia os tokens usando o algoritmo Shunting Yard modificado.
        
        Args:
            tokens (list): Lista de tokens
            
        Returns:
            set: Conjunto de IDs de documentos
        """
        if not tokens:
            return set()
        
        # Converte para notação polonesa reversa (RPN)
        rpn = self._to_rpn(tokens)
        
        # Avalia a RPN
        return self._evaluate_rpn(rpn)
    
    def _to_rpn(self, tokens):
        """
        Converte tokens para notação polonesa reversa (Shunting Yard).
        
        Args:
            tokens (list): Lista de tokens
            
        Returns:
            list: Tokens em RPN
        """
        output = []
        operator_stack = []
        
        # Precedência dos operadores
        precedence = {'OR': 1, 'AND': 2}
        
        for token in tokens:
            if token in ['AND', 'OR']:
                # É um operador
                while (operator_stack and 
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in precedence and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            
            elif token == '(':
                operator_stack.append(token)
            
            elif token == ')':
                # Pop até encontrar '('
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if operator_stack:
                    operator_stack.pop()  # Remove o '('
            
            else:
                # É um termo
                output.append(token)
        
        # Pop dos operadores restantes
        while operator_stack:
            output.append(operator_stack.pop())
        
        return output
    
    def _evaluate_rpn(self, rpn):
        """
        Avalia uma expressão em RPN.
        
        Args:
            rpn (list): Expressão em notação polonesa reversa
            
        Returns:
            set: Conjunto de IDs de documentos
        """
        stack = []
        
        for token in rpn:
            if token == 'AND':
                # Operação AND (interseção)
                if len(stack) >= 2:
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(left & right)
                elif len(stack) == 1:
                    # Se só há um operando, mantém ele
                    pass
            
            elif token == 'OR':
                # Operação OR (união)
                if len(stack) >= 2:
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(left | right)
                elif len(stack) == 1:
                    # Se só há um operando, mantém ele
                    pass
            
            else:
                # É um termo, busca no índice
                docs = self.index.search_term(token.lower())
                stack.append(docs)
        
        # Retorna o resultado final
        if stack:
            return stack[0]
        return set()
    
    def _extract_terms(self, query_string):
        """
        Extrai apenas os termos da consulta (sem operadores).
        
        Args:
            query_string (str): String de consulta
            
        Returns:
            list: Lista de termos
        """
        tokens = self._tokenize_query(query_string)
        terms = [t.lower() for t in tokens if t not in ['AND', 'OR', '(', ')']]
        return terms
    
    def _calculate_relevance(self, doc_id, query_terms):
        """
        Calcula a relevância de um documento para os termos da consulta.
        Usa a média dos z-scores dos termos.
        
        Args:
            doc_id: Identificador do documento
            query_terms (list): Lista de termos da consulta
            
        Returns:
            float: Score de relevância
        """
        z_scores = []
        
        for term in query_terms:
            z_score = self._calculate_z_score(doc_id, term)
            z_scores.append(z_score)
        
        # Média dos z-scores
        if z_scores:
            return sum(z_scores) / len(z_scores)
        return 0.0
    
    def _calculate_z_score(self, doc_id, term):
        """
        Calcula o z-score de um termo em um documento.
        
        Z-score = (frequência no doc - média no corpus) / desvio padrão
        
        Args:
            doc_id: Identificador do documento
            term (str): Termo
            
        Returns:
            float: Z-score
        """
        # Frequência do termo no documento
        term_freq_doc = self.index.get_term_frequency(doc_id, term)
        
        if term_freq_doc == 0:
            return 0.0
        
        # Frequência total do termo no corpus
        total_term_freq = self.index.corpus_term_freq.get(term.lower(), 0)
        
        if total_term_freq == 0:
            return 0.0
        
        # Média de frequência do termo no corpus
        mean_freq = total_term_freq / self.index.total_docs
        
        # Calcula desvio padrão
        variance = 0
        for doc in self.index.documents.keys():
            freq = self.index.get_term_frequency(doc, term)
            variance += (freq - mean_freq) ** 2
        
        variance /= self.index.total_docs
        std_dev = math.sqrt(variance)
        
        # Z-score
        if std_dev == 0:
            return 0.0
        
        z_score = (term_freq_doc - mean_freq) / std_dev
        return z_score
    
    def generate_snippet(self, doc_id, query_terms, context_size=80):
        """
        Gera um snippet do documento destacando os termos da consulta.
        
        Args:
            doc_id: Identificador do documento
            query_terms (list): Lista de termos da consulta
            context_size (int): Tamanho do contexto (caracteres antes e depois)
            
        Returns:
            str: Snippet com o termo destacado
        """
        doc = self.index.get_document(doc_id)
        if not doc:
            return ""
        
        content = doc['content']
        
        # Encontra o termo mais relevante no documento
        best_term = None
        best_score = -float('inf')
        
        for term in query_terms:
            score = self._calculate_z_score(doc_id, term)
            if score > best_score:
                best_score = score
                best_term = term
        
        if not best_term:
            # Se não houver termo relevante, retorna início do documento
            return content[:context_size * 2] + "..."
        
        # Encontra a primeira ocorrência do termo mais relevante
        content_lower = content.lower()
        term_pos = content_lower.find(best_term.lower())
        
        if term_pos == -1:
            # Termo não encontrado, retorna início do documento
            return content[:context_size * 2] + "..."
        
        # Calcula posições do snippet
        start = max(0, term_pos - context_size)
        end = min(len(content), term_pos + len(best_term) + context_size)
        
        # Extrai snippet
        snippet = content[start:end]
        
        # Adiciona reticências se necessário
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        
        # Destaca o termo no snippet (usando marcação HTML)
        # Usa expressão regular para encontrar o termo (case-insensitive)
        pattern = re.compile(re.escape(best_term), re.IGNORECASE)
        snippet = pattern.sub(lambda m: f"<mark>{m.group()}</mark>", snippet, count=1)
        
        return snippet
