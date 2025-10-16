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
            if (word == searchWord) and not searchNode.children:
                return searchNode.documents  # Palavra encontrada

    def insert(self, word: str, document: str) -> bool:
        searchNode = self.root
        searchWord = ""

        if self.root.content == "": # Árvore vazia
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
                    break
            else:
                # Inserir nova palavra
                newNode = CompactTrieNode()
                if word == searchWord:
                    newNode.content = TERMINAL
                else:
                    newNode.content = word[len(searchWord):]
                    
                newNode.documents.add(document)
                searchNode.children.add(newNode)
                return True
            if (word == searchWord) and not searchNode.children:
                if document not in searchNode.documents:
                    searchNode.documents.add(document)
                    return True  # Documento adicionado
                return False # Já está na trie