# RefMerger: Ferramenta de Processamento de Referências Bibliográficas

**RefMerger** é uma ferramenta Python robusta e gratuita para pesquisadores, bibliotecários e acadêmicos que trabalham com grandes volumes de referências bibliográficas. Ela automatiza o processo tedioso de mesclar referências de múltiplas fontes e remover duplicatas, economizando horas de trabalho manual.

## Descrição Detalhada

Em projetos de pesquisa, é comum coletar referências de diversas fontes como PubMed, Web of Science, Scopus ou bases de dados locais. Cada fonte exporta em formatos diferentes (.bib, .xml, .csv, .json), e ao juntá-los, surgem duplicatas inevitáveis. RefMerger resolve isso convertendo tudo para o formato RIS (padrão para gestores de referências como Zotero, Mendeley e EndNote), mesclando os arquivos e aplicando deduplicação inteligente.

### Principais Benefícios:
- **Suporte Multi-Formato**: Converte automaticamente .bib (BibTeX), .xml (PubMed), .csv, .json e .ris
- **Deduplicação Avançada**: Usa algoritmos de similaridade para detectar duplicatas mesmo com variações de título ou formatação
- **Flexibilidade**: Modos configuráveis de deduplicação para diferentes necessidades
- **Robusto**: Trata encodings variados e erros de arquivo graciosamente
- **Gratuito e Open-Source**: Código Python puro, sem dependências pesadas

## Funcionalidades

- **Conversão de Formatos**: Suporta .ris, .bib, .xml, .csv, .json
- **Junção de Arquivos**: Combina múltiplos arquivos em um único RIS
- **Deduplicação Robusta**: Remove duplicatas com prioridade DOI > PMID > Título+Ano+Autor > Hash
- **Modos de Deduplicação**:
  - `estrito`: Apenas DOI
  - `balanceado`: DOI + Título/Ano/Autor
  - `agressivo`: Inclui similaridade de títulos (90%+)
- **Exportação**: Para CSV ou JSON (opcional)
- **Detecção de Encoding**: UTF-8, Latin-1, Windows-1252

## Funcionalidades

- **Conversão de Formatos**: Suporta .ris, .bib, .xml, .csv, .json
- **Junção de Arquivos**: Combina múltiplos arquivos em um único RIS
- **Deduplicação Robusta**: Remove duplicatas com prioridade DOI > PMID > Título+Ano+Autor > Hash
- **Modos de Deduplicação**:
  - `estrito`: Apenas DOI
  - `balanceado`: DOI + Título/Ano/Autor
  - `agressivo`: Inclui similaridade de títulos (90%+)
- **Exportação**: Para CSV ou JSON (opcional)
- **Detecção de Encoding**: UTF-8, Latin-1, Windows-1252

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/fdossi/refmerger.git
   cd refmerger
   ```

2. **Instale dependências** (opcional, apenas para .bib):
   ```bash
   pip install bibtexparser
   ```

3. **Execute o script**:
   ```bash
   python refmerger.py
   ```

## Como Usar

1. Coloque todos os arquivos (.ris, .bib, .xml, .csv, .json) na mesma pasta.
2. Edite as variáveis no final do script:
   - `pasta_dos_arquivos`: Caminho da pasta
   - `modo_deduplicacao`: 'estrito', 'balanceado' ou 'agressivo'
   - `formato_exportar`: None (RIS), 'csv' ou 'json'
3. Execute o script Python.

### Exemplo de Uso:
```python
# Configurações no final do refmerger.py
pasta_dos_arquivos = r"C:\Meus\Arquivos\Referencias"
modo_deduplicacao = 'balanceado'
formato_exportar = None  # Saída em RIS
```

Saída esperada:
```
Sucesso! 25 arquivos foram juntados em 'todas_referencias_juntas.ris'.
707 referência(s) duplicada(s) removida(s). Total final: 268 referência(s) única(s).
```

## Dependências

- Python 3.x
- bibtexparser (para .bib): `pip install bibtexparser`
- Bibliotecas padrão: os, glob, re, json, csv, xml.etree, unicodedata, hashlib, difflib

## Exemplo de Saída

```
Sucesso! 25 arquivos foram juntados em 'todas_referencias_juntas.ris'.
707 referência(s) duplicada(s) removida(s). Total final: 268 referência(s) única(s).
```

## Formatos Suportados

### .bib (BibTeX)
Campos: title, author, year, doi, journal

### .xml (PubMed)
Estrutura esperada: ArticleTitle, Author/LastName, Year, DOI

### .csv
Colunas: title, authors (separados por ;), year, doi

### .json
Estrutura: [{"title": "...", "authors": [...], "year": "...", "doi": "..."}]

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.

## Autor

Desenvolvido por [Seu Nome] - fdossi
   - Exemplos de uso em pesquisas (se aplicável)

3. **Acknowledgements** (opcional)
   - Contribuições que não justificam coautoria
   - Financiamento (agências e números de grant)

4. **References**
   - Gerado automaticamente do arquivo .bib

## Diretrizes de Formatação

### Texto
- **Tamanho**: 250-1000 palavras (excluindo referências)
- **Tom**: Acessível a pesquisadores de diversas áreas
- **Evite**: Listas com bullet points (use prosa)
- **Evite**: Documentação de API (isso vai na documentação do software)

### Citações
- Use sintaxe Markdown: `[@referencia1]` ou `[@ref1; @ref2]`
- No arquivo .bib, use nomes COMPLETOS de revistas/conferências
- Inclua DOI sempre que possível

### Matemática
- Inline: `$f(x) = e^{\pi/x}$`
- Display: `$$\Delta U = Q - W$$`
- Ou use LaTeX direto:
  ```
  \begin{equation}\label{eq:nome}
  \hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
  \end{equation}
  ```

### Código
Use blocos de código Markdown:
```python
import edslab
resultado = edslab.processar(dados)
```

## Testando Localmente

### Com Docker
```bash
docker run --rm \
  --volume $PWD:/data \
  --user $(id -u):$(id -g) \
  --env JOURNAL=joss \
  openjournals/inara
```

Isso gera `paper.pdf` no diretório atual.

### Com GitHub Actions
Adicione este workflow ao seu repositório em `.github/workflows/draft-pdf.yml`:

```yaml
name: Draft PDF

on:
  push:
    branches: [main]
  pull_request:

jobs:
  paper:
    runs-on: ubuntu-latest
    name: Paper Draft
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Build PDF
        uses: openjournals/openjournals-draft-action@master
        with:
          journal: joss
          paper-path: paper.md
      - name: Upload
        uses: actions/upload-artifact@v3
        with:
          name: paper
          path: paper.pdf
```

## Preparando para Submissão

1. **Complete todos os campos** marcados com `[...]` no `paper.md`
2. **Adicione referências** ao `paper.bib` e cite-as no texto
3. **Revise o tamanho**: deve ter 250-1000 palavras
4. **Teste localmente**: gere o PDF e verifique a formatação
5. **Coloque no repositório**: junto com o código do software
6. **Crie um release** com tag de versão (ex: v1.0.0)
7. **Archive no Zenodo** e obtenha um DOI

## Processo de Submissão JOSS

1. Acesse https://joss.theoj.org/
2. Clique em "Submit"
3. Preencha o formulário com:
   - URL do repositório
   - Versão do software
   - Editor sugerido (opcional)
4. Aguarde pre-review do editor
5. Responda a comentários dos revisores
6. Faça alterações solicitadas
7. Após aceite, publique release final e atualize DOI

## Recursos Adicionais

- **Documentação JOSS**: https://joss.readthedocs.io/
- **Exemplo de artigo**: https://joss.readthedocs.io/en/latest/example_paper.html
- **Diretrizes para revisores**: https://joss.readthedocs.io/en/latest/reviewer_guidelines.html
- **Critérios de revisão**: https://joss.readthedocs.io/en/latest/review_criteria.html

## Checklist Pré-Submissão

- [ ] Software tem licença OSI-approved
- [ ] Código está em repositório Git público
- [ ] Documentação clara está disponível
- [ ] Testes automatizados implementados
- [ ] README.md descreve instalação e uso básico
- [ ] Arquivo paper.md completo (250-1000 palavras)
- [ ] Arquivo paper.bib com todas as referências
- [ ] Metadados YAML preenchidos corretamente
- [ ] PDF gerado localmente sem erros
- [ ] ORCID dos autores verificado
- [ ] Afiliações corretas
- [ ] DOI ou link do software disponível

## Dicas Finais

1. **Seja conciso**: JOSS valoriza brevidade e clareza
2. **Foco no valor**: Explique POR QUE seu software é útil
3. **Público amplo**: Escreva para pesquisadores de outras áreas
4. **Cite bem**: Referencie trabalhos relacionados adequadamente
5. **Documente bem**: A documentação do software é tão importante quanto o artigo
6. **Testes**: Cobertura de testes é critério de revisão
7. **Comunidade**: Responda aos revisores de forma colaborativa

## Suporte

- **Issues no GitHub JOSS**: https://github.com/openjournals/joss/issues
- **Email**: admin@theoj.org (apenas para questões confidenciais)
- **Discussões**: https://github.com/openjournals/joss/discussions

---

**Nota**: Este modelo está atualizado conforme as diretrizes do JOSS em janeiro de 2025. Sempre consulte a documentação oficial para informações mais recentes.
