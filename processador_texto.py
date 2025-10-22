import string

def limpar_texto(texto):
    #converte para minusculas  
    texto = texto.lower()
    
    #remove pontuação e numeros*
    caracteres_para_remover = string.punctuation + string.digits
    tabela_pontuacao_numeros = str.maketrans('', '', caracteres_para_remover)
    
    texto = texto.translate(tabela_pontuacao_numeros)
    
    # remove espaços extras
    # texto = ' '.join(texto.split())
    
    return texto
