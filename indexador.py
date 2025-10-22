import os
from compact_trie import CompactTrie
from processador_texto import limpar_texto
from carregar_documentos import DocumentLoader

PASTA_BBC = "bbc"
ARQUIVO_INDICE = "indice.json"

class IndexBuilder:
    def __init__(self, pasta_raiz):
        self.pasta_raiz = pasta_raiz
        self.trie = CompactTrie()

    def criar_indice(self):
    
    
    
      loader = DocumentLoader(PASTA_BBC)
      for nome_arquivo, texto_original, categoria in loader.stream_documentos():
        
          texto_limpo = limpar_texto(texto_original)
          palavras = texto_limpo.split() #descarta automaticamente os espacos em branco
        
          # Cria ID unico para o documento baseado na categoria e nome do arquivo
          doc_id_unico = f"{categoria}/{nome_arquivo}"
        
          for palavra in palavras:
             self.trie.insert(palavra, doc_id_unico)
            
      return self.trie

    def salvar_indice(self, filename=ARQUIVO_INDICE):
       success = self.trie.save_to_json(filename)
            
       return success

    def carregar_indice(self, filename=ARQUIVO_INDICE):
       loaded_trie = CompactTrie.load_from_json(filename)
       if loaded_trie:
           self.trie = loaded_trie
           return True
       return False






# TESTES
if __name__ == "__main__":
    
    # prints
    
    builder = IndexBuilder(PASTA_BBC)

    # carregar ou criar com print
    print(f"Tentando carregar índice de '{ARQUIVO_INDICE}'")
    if not builder.carregar_indice(ARQUIVO_INDICE):
        
        # Se não existir, constrói e salva
        print("Índice não encontrado. Construindo um novo")
        builder.criar_indice()
        
        print(f"Salvando índice em '{ARQUIVO_INDICE}'")
        if builder.salvar_indice(ARQUIVO_INDICE):
            print("Índice salvo com sucesso!") 
        else:
            print("ERRO ao salvar índice!")
    else:
        print("Índice carregado com sucesso")

    # Teste final de busca
    print("\n Teste de Busca")
    
    # Uma palavra que deve existir
    termo_teste = "government"
    resultados = builder.trie.search(termo_teste) 
    if resultados:
         print(f" Resultados para '{termo_teste}': {len(resultados)} encontrados.")
         print(f" Exemplos: {list(resultados)[:5]}")
    else:
         print(f"Nenhum resultado para '{termo_teste}'.")
    
    # testando a retirada dos numeros uma palavra que NAO deve existir numero
    termo_teste_num = "19"
    resultados_num = builder.trie.search(termo_teste_num)
    if not resultados_num:
        print(f"Resultados para '{termo_teste_num}': nenhum encontrado (Certo!)")
    else:
        print(f"Erro! Termo '{termo_teste_num}' encontrado Deveria ter sido removido.")

    print("fim de teste")



