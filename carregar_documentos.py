import os
import glob


class DocumentLoader:
    def __init__(self, pasta_raiz):
        self.pasta_raiz = pasta_raiz
        self.todos_documentos = None

    def stream_documentos(self):
       print(f"Iniciando o carregamento dos documentos da pasta: {self.pasta_raiz}")
       try:
            pastas_categorias = os.listdir(self.pasta_raiz)
       except FileNotFoundError:
            print(f"Erro: A pasta '{self.pasta_raiz}' não foi encontrada.")
            return 
      
       for pasta in pastas_categorias:
           caminho_da_pasta = os.path.join(self.pasta_raiz, pasta)

           if os.path.isdir(caminho_da_pasta):
               print(f"Lendo a pasta: {pasta}...")

               for nome_arquivo in os.listdir(caminho_da_pasta):
                   caminho_do_arquivo = os.path.join(caminho_da_pasta, nome_arquivo)
                   try:
                       with open(caminho_do_arquivo, 'r', encoding='utf-8') as f:
                            texto_original = f.read()
                       yield nome_arquivo, texto_original, pasta
                        
                   except Exception as e:
                             print(f"Erro ao ler o arquivo {nome_arquivo}: {e}") 
            
    def load_all_documents(self):
        if self.todos_documentos:
            return self.todos_documentos
        
        print(f"Carregando TODOS os documentos de '{self.pasta_raiz}' para a memória")
        self.todos_documentos = {}
        
        caminho_glob = os.path.join(self.pasta_raiz, "*", "*.txt")
        arquivos_txt = glob.glob(caminho_glob)
        
        for file_path in arquivos_txt:
            try:
                nome_arquivo = os.path.basename(file_path)
                categoria = os.path.basename(os.path.dirname(file_path))
                
                with open(file_path, 'r', encoding='latin-1') as file:
                    content = file.read()
                    
                self.todos_documentos[nome_arquivo] = {
                    'content': content,
                    'category': categoria
                }
            except Exception as e:
                print(f"Erro ao carregar arquivo {file_path}: {e}")
                
        print(f"Carregados {len(self.todos_documentos)} documentos na memória.")
        return self.todos_documentos

    
            

        


    