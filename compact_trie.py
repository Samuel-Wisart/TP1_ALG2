import json

TERMINAL = "$"

class CompactTrieNode:
    def __init__(self):
        self.content = ""
        self.children = set()  # Conjunto de nós filhos
        self.documents = set()  # Conjunto de nomes de documentos

class CompactTrie:
    def __init__(self):
        self.root = CompactTrieNode()

    def search(self, word: str) -> set[str]:
        searchNode = self.root
        searchWord = ""
        while True:
            for child in searchNode.children:
                childSulfix = child.content
                if child.content.endswith(TERMINAL):
                    childSulfix = child.content[:-1]
                if word.startswith(searchWord + childSulfix):
                    searchWord += childSulfix
                    searchNode = child
                    break
            else:
                return set()  # Palavra não encontrada
            # Se a palavra foi completamente consumida, retornar os documentos
            if word == searchWord:
                return searchNode.documents

    def insert(self, word: str, document: str) -> bool:
        searchNode = self.root
        searchWord = ""

        if not self.root.children:  # Árvore vazia
            newNode = CompactTrieNode()
            newNode.content = word
            newNode.documents.add(document)
            searchNode.children.add(newNode)
            return True

        while True:
            for child in searchNode.children:
                childSulfix = child.content
                if child.content.endswith(TERMINAL):
                    childSulfix = child.content[:-1]
                if word.startswith(searchWord + childSulfix):
                    searchWord += childSulfix
                    searchNode = child
                    # Se lermos a palavra completa no nó atual, atualizar documentos
                    if searchWord == word:
                        if document in searchNode.documents:
                            return False
                        searchNode.documents.add(document)
                        return True
                    break
            else:
                # Inserir nova palavra como filho
                newNode = CompactTrieNode()
                newNode.content = word[len(searchWord):]
                newNode.documents.add(document)
                searchNode.children.add(newNode)
                return True
        
    def save_to_json(self, filepath: str) -> bool:

        def _serialize(node):
            return {
                "content": node.content,
                "documents": sorted(list(node.documents)),
                "children": [_serialize(child) for child in node.children]
            }

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(_serialize(self.root), f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    @classmethod
    def load_from_json(cls, filepath: str):
        """Carrega uma CompactTrie a partir do JSON produzido por save_to_json.

        Retorna uma instância de CompactTrie ou None em caso de erro.
        """
        def _build(node_data):
            node = CompactTrieNode()
            node.content = node_data.get("content", "")
            node.documents = set(node_data.get("documents", []))
            for child_data in node_data.get("children", []):
                child = _build(child_data)
                node.children.add(child)
            return node

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            trie = cls()
            trie.root = _build(data)
            return trie
        except Exception:
            return None


def _test_compact_trie():
    """Teste simples para as três funções: insert, search e save_to_json."""
    import os

    trie = CompactTrie()
    # Inserir algumas palavras em documentos diferentes
    assert trie.insert("casa", "doc1") is True
    assert trie.insert("casar", "doc2") is True
    assert trie.insert("cabo", "doc3") is True
    # Inserir palavra já existente no mesmo documento
    assert trie.insert("casa", "doc1") is False
    # Inserir palavra já existente em documento diferente
    assert trie.insert("casa", "doc4") is True

    # Testar search
    docs_casa = trie.search("casa")
    assert isinstance(docs_casa, set)
    assert "doc1" in docs_casa
    assert "doc4" in docs_casa

    docs_casar = trie.search("casar")
    assert docs_casar == {"doc2"}

    docs_nao = trie.search("inexistente")
    assert docs_nao == set()

    # Testar save_to_json
    outpath = "compact_trie_test_output.json"
    ok = trie.save_to_json(outpath)
    assert ok is True
    assert os.path.exists(outpath)

    # Ler e validar json básico
    with open(outpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict)

    # Testar load_from_json
    loaded = CompactTrie.load_from_json(outpath)
    assert loaded is not None
    # As buscas na trie carregada devem corresponder
    docs_casa_loaded = loaded.search("casa")
    assert isinstance(docs_casa_loaded, set)
    assert "doc1" in docs_casa_loaded
    assert "doc4" in docs_casa_loaded

    # Limpar arquivo de teste
    try:
        os.remove(outpath)
    except Exception:
        pass

    print("All compact_trie tests passed")


if __name__ == "__main__":
    _test_compact_trie()

