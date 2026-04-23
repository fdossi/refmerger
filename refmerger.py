import os
import glob
import re
import json
import csv
import xml.etree.ElementTree as ET
import unicodedata
import hashlib
from difflib import SequenceMatcher
try:
    import bibtexparser
except ImportError:
    bibtexparser = None

def detectar_encoding(arquivo):
    """Tenta detectar encoding do arquivo."""
    encodings = ['utf-8', 'latin-1', 'windows-1252']
    for enc in encodings:
        try:
            with open(arquivo, 'r', encoding=enc) as f:
                f.read()
            return enc
        except UnicodeDecodeError:
            continue
    return 'utf-8'  # fallback

def normalizar_texto(texto):
    """Remove acentos, pontuação e normaliza espaços."""
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('ascii')
    texto = re.sub(r'[^\w\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip().lower()
    return texto

def normalizar_doi(doi):
    """Normaliza DOI: remove prefixos, lowercase, strip."""
    doi = doi.lower().strip()
    doi = re.sub(r'^https?://doi\.org/', '', doi)
    doi = re.sub(r'^doi:', '', doi)
    return doi

def converter_para_ris(arquivo_entrada, arquivo_saida_ris):
    """Converte arquivo para RIS baseado na extensão."""
    ext = os.path.splitext(arquivo_entrada)[1].lower()
    encoding = detectar_encoding(arquivo_entrada)

    try:
        if ext == '.ris':
            # Já é RIS, copia
            with open(arquivo_entrada, 'r', encoding=encoding) as f_in:
                conteudo = f_in.read()
            with open(arquivo_saida_ris, 'w', encoding='utf-8') as f_out:
                f_out.write(conteudo)
        elif ext == '.bib':
            if bibtexparser is None:
                print(f"bibtexparser não instalado, pulando {arquivo_entrada}")
                return
            with open(arquivo_entrada, 'r', encoding=encoding) as f:
                bib_database = bibtexparser.load(f)
            ris_blocos = []
            for entry in bib_database.entries:
                bloco = "TY  - JOUR\n"
                if 'title' in entry:
                    bloco += f"TI  - {entry['title']}\n"
                if 'author' in entry:
                    autores = entry['author'].split(' and ')
                    for autor in autores:
                        bloco += f"AU  - {autor}\n"
                if 'year' in entry:
                    bloco += f"PY  - {entry['year']}\n"
                if 'doi' in entry:
                    bloco += f"DO  - {entry['doi']}\n"
                if 'journal' in entry:
                    bloco += f"JO  - {entry['journal']}\n"
                bloco += "ER  -\n\n"
                ris_blocos.append(bloco)
            with open(arquivo_saida_ris, 'w', encoding='utf-8') as f_out:
                f_out.write(''.join(ris_blocos))
        elif ext == '.xml':
            tree = ET.parse(arquivo_entrada)
            root = tree.getroot()
            ris_blocos = []
            for artigo in root.findall('.//Article'):  # Assumindo PubMed XML
                bloco = "TY  - JOUR\n"
                titulo = artigo.find('ArticleTitle')
                if titulo is not None:
                    bloco += f"TI  - {titulo.text}\n"
                autores = artigo.findall('.//Author')
                for autor in autores:
                    nome = autor.find('LastName')
                    if nome is not None:
                        bloco += f"AU  - {nome.text}\n"
                ano = artigo.find('Journal//Year')
                if ano is not None:
                    bloco += f"PY  - {ano.text}\n"
                doi = artigo.find('ELocationID[@EIdType="doi"]')
                if doi is not None:
                    bloco += f"DO  - {doi.text}\n"
                bloco += "ER  -\n\n"
                ris_blocos.append(bloco)
            with open(arquivo_saida_ris, 'w', encoding='utf-8') as f_out:
                f_out.write(''.join(ris_blocos))
        elif ext == '.csv':
            ris_blocos = []
            with open(arquivo_entrada, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    bloco = "TY  - JOUR\n"
                    if 'title' in row:
                        bloco += f"TI  - {row['title']}\n"
                    if 'authors' in row:
                        autores = row['authors'].split(';')
                        for autor in autores:
                            bloco += f"AU  - {autor.strip()}\n"
                    if 'year' in row:
                        bloco += f"PY  - {row['year']}\n"
                    if 'doi' in row:
                        bloco += f"DO  - {row['doi']}\n"
                    bloco += "ER  -\n\n"
                    ris_blocos.append(bloco)
            with open(arquivo_saida_ris, 'w', encoding='utf-8') as f_out:
                f_out.write(''.join(ris_blocos))
        elif ext == '.json':
            with open(arquivo_entrada, 'r', encoding=encoding) as f:
                data = json.load(f)
            ris_blocos = []
            for item in data if isinstance(data, list) else [data]:
                bloco = "TY  - JOUR\n"
                if 'title' in item:
                    bloco += f"TI  - {item['title']}\n"
                if 'authors' in item:
                    autores = item['authors'] if isinstance(item['authors'], list) else [item['authors']]
                    for autor in autores:
                        bloco += f"AU  - {autor}\n"
                if 'year' in item:
                    bloco += f"PY  - {item['year']}\n"
                if 'doi' in item:
                    bloco += f"DO  - {item['doi']}\n"
                bloco += "ER  -\n\n"
                ris_blocos.append(bloco)
            with open(arquivo_saida_ris, 'w', encoding='utf-8') as f_out:
                f_out.write(''.join(ris_blocos))
        else:
            print(f"Formato não suportado: {ext}")
    except Exception as e:
        print(f"Erro ao converter {arquivo_entrada}: {e}")

def converter_arquivos_para_ris(diretorio_entrada, temp_dir):
    """Converte todos os arquivos suportados para RIS temporários."""
    os.makedirs(temp_dir, exist_ok=True)
    arquivos = glob.glob(os.path.join(diretorio_entrada, '*'))
    arquivos_ris = []
    for arquivo in arquivos:
        if os.path.isfile(arquivo):
            nome_base = os.path.splitext(os.path.basename(arquivo))[0]
            ris_temp = os.path.join(temp_dir, f"{nome_base}.ris")
            converter_para_ris(arquivo, ris_temp)
            if os.path.exists(ris_temp):
                arquivos_ris.append(ris_temp)
    return arquivos_ris

def juntar_arquivos_ris(arquivos_ris, arquivo_saida):
    """
    Junta arquivos RIS em um único arquivo.
    """
    if not arquivos_ris:
        print("Nenhum arquivo RIS encontrado.")
        return

    # Abre o arquivo de saída no modo de escrita ('w')
    try:
        with open(arquivo_saida, 'w', encoding='utf-8') as f_saida:
            for caminho_arquivo in arquivos_ris:
                try:
                    encoding = detectar_encoding(caminho_arquivo)
                    with open(caminho_arquivo, 'r', encoding=encoding) as f_entrada:
                        conteudo = f_entrada.read()
                        f_saida.write(conteudo)
                        if not conteudo.endswith('\n'):
                            f_saida.write('\n')
                except (IOError, UnicodeDecodeError) as e:
                    print(f"Erro ao ler o arquivo '{caminho_arquivo}': {e}")
                    continue
    except PermissionError as e:
        print(f"Erro: sem permissão para criar ou escrever no arquivo de saída '{arquivo_saida}': {e}")
        return
    except IOError as e:
        print(f"Erro ao criar ou escrever no arquivo de saída '{arquivo_saida}': {e}")
        return
                    
    print(f"Sucesso! {len(arquivos_ris)} arquivos foram juntados em '{arquivo_saida}'.")


def remover_duplicatas(arquivo_saida, modo='balanceado'):
    """
    Remove referências duplicadas do arquivo RIS com modos configuráveis.
    Modos: 'estrito' (DOI apenas), 'balanceado' (DOI + título/ano), 'agressivo' (inclui similaridade).
    """
    try:
        with open(arquivo_saida, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except (IOError, UnicodeDecodeError) as e:
        print(f"Erro ao ler o arquivo para deduplicação: {e}")
        return

    # Divide em blocos individuais de referência (cada um começa com TY  -)
    blocos = re.split(r'(?=^TY  -)', conteudo, flags=re.MULTILINE)
    blocos = [b.strip() for b in blocos if b.strip()]

    if not blocos:
        print("Nenhum bloco de referência encontrado para deduplicar.")
        return

    def extrair_campos(bloco):
        """Extrai campos do bloco RIS, suportando alternativos."""
        campos = {}
        linhas = bloco.split('\n')
        for linha in linhas:
            if '  - ' in linha:
                tag, valor = linha.split('  - ', 1)
                campos[tag.strip()] = valor.strip()
        return campos

    def gerar_chave(bloco, modo):
        campos = extrair_campos(bloco)
        # DOI normalizado
        doi = campos.get('DO', '')
        if doi:
            doi_norm = normalizar_doi(doi)
            if modo == 'estrito':
                return ('doi', doi_norm)
            else:
                return ('doi', doi_norm)

        # PMID
        pmid = campos.get('PMID', '')
        if pmid:
            return ('pmid', pmid.strip())

        # Título + ano + primeiro autor
        titulo = campos.get('TI', campos.get('T1', ''))
        ano = campos.get('PY', campos.get('Y1', ''))
        autores = campos.get('AU', '')
        if titulo and ano:
            titulo_norm = normalizar_texto(titulo)
            primeiro_autor = autores.split('\n')[0] if autores else ''
            chave_base = ('titulo_ano_autor', titulo_norm, ano, primeiro_autor)
            if modo == 'agressivo':
                # Verificar similaridade com títulos existentes
                for v in vistos:
                    if isinstance(v, tuple) and len(v) == 4 and v[0] == 'titulo_ano_autor':
                        sim = SequenceMatcher(None, titulo_norm, v[1]).ratio()
                        if sim > 0.9:  # 90% similar
                            return v  # Considerar duplicata
                return chave_base
            return chave_base

        # Hash do conteúdo
        hash_conteudo = hashlib.md5(bloco.encode('utf-8')).hexdigest()
        return ('hash', hash_conteudo)

    vistos = set()
    unicos = []
    duplicatas = 0

    for bloco in blocos:
        chave = gerar_chave(bloco, modo)

        if chave not in vistos:
            vistos.add(chave)
            unicos.append(bloco)
        else:
            duplicatas += 1

    try:
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(unicos) + '\n')
    except IOError as e:
        print(f"Erro ao escrever arquivo deduplicado: {e}")
        return

    print(f"{duplicatas} referência(s) duplicada(s) removida(s). Total final: {len(unicos)} referência(s) única(s).")

def exportar_para_formato(arquivo_ris, formato, arquivo_saida):
    """Exporta arquivo RIS para outro formato."""
    try:
        with open(arquivo_ris, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except (IOError, UnicodeDecodeError) as e:
        print(f"Erro ao ler arquivo RIS: {e}")
        return

    blocos = re.split(r'(?=^TY  -)', conteudo, flags=re.MULTILINE)
    blocos = [b.strip() for b in blocos if b.strip()]

    if formato == 'csv':
        with open(arquivo_saida, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Authors', 'Year', 'DOI'])
            for bloco in blocos:
                campos = extrair_campos(bloco)
                titulo = campos.get('TI', campos.get('T1', ''))
                autores = '; '.join([campos.get('AU', '')])
                ano = campos.get('PY', campos.get('Y1', ''))
                doi = campos.get('DO', '')
                writer.writerow([titulo, autores, ano, doi])
        print(f"Exportado para CSV: {arquivo_saida}")
    elif formato == 'json':
        data = []
        for bloco in blocos:
            campos = extrair_campos(bloco)
            item = {
                'title': campos.get('TI', campos.get('T1', '')),
                'authors': [campos.get('AU', '')],
                'year': campos.get('PY', campos.get('Y1', '')),
                'doi': campos.get('DO', '')
            }
            data.append(item)
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Exportado para JSON: {arquivo_saida}")
    else:
        print(f"Formato não suportado: {formato}")

# ==========================================
# COMO USAR:
# ==========================================
# 1. Coloque todos os seus arquivos (.ris, .bib, .xml, .csv, .json) na mesma pasta.
# 2. Mude o caminho abaixo para a pasta onde estão seus arquivos (pode ser '.' para a pasta atual).
pasta_dos_arquivos = r"C:\Users\fabio\Downloads\RIS_mnps" 

# 3. Escolha o nome do arquivo final que será gerado.
nome_do_arquivo_final = os.path.join(pasta_dos_arquivos, 'todas_referencias_juntas.ris')

# 4. Escolha o modo de deduplicação: 'estrito', 'balanceado', 'agressivo'
modo_deduplicacao = 'balanceado'

# 5. Opcional: exportar para outro formato ('csv', 'json') ou None para RIS
formato_exportar = None  # 'csv' ou 'json' ou None

# Executa as funções
temp_dir = os.path.join(pasta_dos_arquivos, 'temp_ris')
arquivos_ris = converter_arquivos_para_ris(pasta_dos_arquivos, temp_dir)
# Exclui o arquivo de saída se existir na lista
arquivos_ris = [f for f in arquivos_ris if not f.endswith(os.path.basename(nome_do_arquivo_final))]
juntar_arquivos_ris(arquivos_ris, nome_do_arquivo_final)
remover_duplicatas(nome_do_arquivo_final, modo_deduplicacao)

if formato_exportar:
    arquivo_exportado = nome_do_arquivo_final.replace('.ris', f'.{formato_exportar}')
    exportar_para_formato(nome_do_arquivo_final, formato_exportar, arquivo_exportado)

# Limpa temp
import shutil
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)