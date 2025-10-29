"""Trie compacta (Patricia Trie) para índice invertido."""

class TrieNode:
    """Nó da trie compacta."""

    def __init__(self, prefix=""):
        self.prefix = prefix
        self.children = {}
        self.documents = set()
        self.is_end_of_word = False

    def to_dict(self):
        """Serializa o nó para dicionário."""
        return {
            'prefix': self.prefix,
            'children': {k: v.to_dict() for k, v in self.children.items()},
            'documents': list(self.documents),
            'is_end_of_word': self.is_end_of_word
        }

    @staticmethod
    def from_dict(data):
        """Deserializa um nó a partir de dicionário."""
        node = TrieNode(data['prefix'])
        node.documents = set(data['documents'])
        node.is_end_of_word = data['is_end_of_word']
        node.children = {k: TrieNode.from_dict(v) for k, v in data['children'].items()}
        return node


class CompactTrie:
    """Trie compacta (Patricia Trie) usada pelo índice invertido."""
    
    def __init__(self):
        self.root = TrieNode("")
        self.total_words = 0
    
    def insert(self, word, doc_id):
        """Insere uma palavra associada a um documento."""
        if not word:
            return
        
        word = word.lower()
        self._insert_recursive(self.root, word, doc_id, 0)
    
    def _insert_recursive(self, node, word, doc_id, depth):
        """Auxiliar recursiva para inserção."""
        if depth == len(word):
            node.is_end_of_word = True
            node.documents.add(doc_id)
            return
        
        char = word[depth]
        
        if char not in node.children:
            remaining = word[depth:]
            new_node = TrieNode(remaining)
            new_node.is_end_of_word = True
            new_node.documents.add(doc_id)
            node.children[char] = new_node
            return
        
        child = node.children[char]
        prefix = child.prefix
        
    # Encontra o maior prefixo comum entre a palavra e o prefixo do nó
        common_length = 0
        max_compare = min(len(prefix), len(word) - depth)
        
        while common_length < max_compare and prefix[common_length] == word[depth + common_length]:
            common_length += 1
        
        # Caso 1: Prefixo do nó é completamente consumido
        if common_length == len(prefix):
            self._insert_recursive(child, word, doc_id, depth + common_length)
            return
        
    # Caso 2: dividir nó criando intermediário com prefixo comum
        common_prefix = prefix[:common_length]
        new_node = TrieNode(common_prefix)
        
    # Atualiza filho existente
        child.prefix = prefix[common_length:]
        first_char_old = child.prefix[0]
        new_node.children[first_char_old] = child
        
        # Cria novo nó para o resto da palavra sendo inserida
        if depth + common_length < len(word):
            remaining = word[depth + common_length:]
            new_child = TrieNode(remaining)
            new_child.is_end_of_word = True
            new_child.documents.add(doc_id)
            new_node.children[remaining[0]] = new_child
        else:
            # A palavra termina no nó intermediário
            new_node.is_end_of_word = True
            new_node.documents.add(doc_id)
        
        # Substitui o filho antigo pelo novo nó intermediário
        node.children[char] = new_node
    
    def search(self, word):
        """Busca uma palavra e retorna conjunto de documentos."""
        if not word:
            return set()
        
        word = word.lower()
        node = self._find_node(word)
        
        if node and node.is_end_of_word:
            return node.documents.copy()
        return set()
    
    def _find_node(self, word):
        """Encontra o nó correspondente a uma palavra."""
        node = self.root
        depth = 0
        
        while depth < len(word):
            char = word[depth]
            
            if char not in node.children:
                return None
            
            child = node.children[char]
            prefix = child.prefix
            
            # Verifica se o prefixo corresponde à palavra
            max_compare = min(len(prefix), len(word) - depth)
            
            for i in range(max_compare):
                if prefix[i] != word[depth + i]:
                    return None
            
            depth += len(prefix)
            node = child
        
        return node
    
    def starts_with(self, prefix):
        """Retorna documentos que contêm palavras com o prefixo fornecido."""
        if not prefix:
            return set()
        
        prefix = prefix.lower()
        node = self._find_node(prefix)
        
        if not node:
            return set()
        
        # Coleta todos os documentos da subárvore
        return self._collect_all_documents(node)
    
    def _collect_all_documents(self, node):
        """Coleta todos os documentos de uma subárvore."""
        docs = set()
        
        if node.is_end_of_word:
            docs.update(node.documents)
        
        for child in node.children.values():
            docs.update(self._collect_all_documents(child))
        
        return docs
    
    def get_all_words(self):
        """Retorna todas as palavras armazenadas na trie."""
        words = []
        self._collect_words(self.root, "", words)
        return words
    
    def _collect_words(self, node, current_word, words):
        """Coleta todas as palavras recursivamente."""
        current_word += node.prefix
        
        if node.is_end_of_word:
            words.append((current_word, node.documents.copy()))
        
        for child in node.children.values():
            self._collect_words(child, current_word, words)
    
    def to_dict(self):
        """Serializa a trie para um dicionário."""
        return {
            'root': self.root.to_dict(),
            'total_words': self.total_words
        }
    
    @staticmethod
    def from_dict(data):
        """Deserializa uma trie a partir de dicionário."""
        trie = CompactTrie()
        trie.root = TrieNode.from_dict(data['root'])
        trie.total_words = data['total_words']
        return trie
    
    def __len__(self):
        """Retorna o número de palavras únicas na trie."""
        return len(self.get_all_words())
    
    def __contains__(self, word):
        """Verifica se uma palavra existe na trie."""
        return len(self.search(word)) > 0
