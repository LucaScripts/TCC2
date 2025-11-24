# Guia Completo de Uso do Sistema Híbrido Expandido de Predição de Evasão

**Versão:** 2.0  
**Data:** Outubro de 2025  
**Status:** Pronto para Produção

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Uso Básico](#uso-básico)
4. [Uso Avançado](#uso-avançado)
5. [Integração com AcadWeb](#integração-com-acadweb)
6. [Agendamento Automático](#agendamento-automático)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## 🎯 Visão Geral

### O que é o Sistema?

O Sistema Híbrido Expandido de Predição de Evasão é uma solução que combina:

- **Machine Learning (XGBoost):** Modelo treinado com 18 features
- **Regras de Negócio:** Critérios institucionais de risco
- **Dados de Satisfação:** 6 features qualitativas de satisfação estudantil

### O que o Sistema Faz?

O sistema analisa dados de alunos e prediz o risco de evasão, classificando-os em categorias:

- **MT (Matriculado):** Sem indicadores de risco
- **LFI (Limpeza Financeira):** Pendências financeiras
- **LFR (Limpeza de Frequência):** Faltas + pendências
- **LAC (Limpeza Acadêmica):** Pendências acadêmicas
- **NC (Nunca Compareceu):** Nunca frequentou
- **NF (Não Formados):** Curso completo + pendências

### Quem Deve Usar?

- **Coordenadores de Curso:** Para monitorar alunos em risco
- **Equipe Pedagógica:** Para planejar intervenções
- **Gestão Acadêmica:** Para análise estratégica
- **Pesquisadores:** Para estudar padrões de evasão

---

## 💻 Instalação

### Pré-requisitos

```bash
# Python 3.8+
python3 --version

# Pip (gerenciador de pacotes)
pip3 --version
```

### Instalação de Dependências

```bash
# Clonar ou copiar os arquivos do projeto
cd /caminho/do/projeto

# Instalar dependências
pip3 install -r requirements_producao.txt
```

### Arquivo requirements_producao.txt

```
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
xgboost>=1.5.0
joblib>=1.1.0
openpyxl>=3.7.0
```

### Verificação de Instalação

```bash
# Testar importações
python3 -c "import pandas, numpy, sklearn, xgboost, joblib; print('✅ Todas as dependências instaladas')"
```

---

## 🚀 Uso Básico

### Exemplo 1: Predição Simples

```python
from sistema_evasao_hibrido_expandido_producao import SistemaEvasaoHibridoExpandido

# Inicializar sistema
sistema = SistemaEvasaoHibridoExpandido()

# Carregar dados
dados = sistema.carregar_dados('alunos_ativos_atual_EXPANDIDO.csv')

# Fazer predições
predicoes = sistema.prever(dados)

# Exibir resultados
print(predicoes)
```

**Saída esperada:**

```
Matricula  Predicao_ML  Predicao_Final  Categoria_Risco  Confianca
ENF180197  MT           MT               Matriculado      0.95
ENF180202  LAC          LAC              Limpeza Acadêmica 0.87
ENF180161  LFI          LFI              Limpeza Financeira 0.92
```

### Exemplo 2: Salvar Resultados

```python
# Fazer predições
predicoes = sistema.prever(dados)

# Salvar em CSV
sistema.salvar_resultados(predicoes, 'predicoes_outubro_2025.csv')

# Salvar em JSON
sistema.exportar_relatorio_json(predicoes, 'relatorio_outubro_2025.json')
```

### Exemplo 3: Gerar Relatório

```python
# Gerar relatório estatístico
relatorio = sistema.gerar_relatorio(predicoes)

# Exibir relatório
print(relatorio)
```

**Saída esperada:**

```
RELATÓRIO DE PREDIÇÃO DE EVASÃO
================================
Data: 2025-10-31 14:30:00
Total de alunos: 954

DISTRIBUIÇÃO DE PREDIÇÕES:
  Matriculado (MT): 782 (82.0%)
  Limpeza Acadêmica (LAC): 78 (8.2%)
  Limpeza Financeira (LFI): 8 (0.8%)
  Nunca Compareceu (NC): 9 (0.9%)
  Não Formados (NF): 5 (0.5%)
  Outros: 72 (7.5%)

CASOS DE RISCO: 172 (18.0%)

AÇÕES RECOMENDADAS:
  - Contato financeiro: 8 alunos
  - Acompanhamento acadêmico: 78 alunos
  - Contato urgente: 9 alunos
  - Monitoramento intensivo: 72 alunos
```

---

## 🔧 Uso Avançado

### Exemplo 4: Análise por Categoria

```python
# Filtrar alunos por categoria de risco
alunos_lfi = predicoes[predicoes['Categoria_Risco'] == 'Limpeza Financeira']
alunos_lac = predicoes[predicoes['Categoria_Risco'] == 'Limpeza Acadêmica']
alunos_nc = predicoes[predicoes['Categoria_Risco'] == 'Nunca Compareceu']

# Exibir alunos em cada categoria
print(f"Alunos em Limpeza Financeira: {len(alunos_lfi)}")
print(f"Alunos em Limpeza Acadêmica: {len(alunos_lac)}")
print(f"Alunos que Nunca Compareceram: {len(alunos_nc)}")

# Exportar por categoria
alunos_lfi.to_csv('alunos_limpeza_financeira.csv', index=False)
alunos_lac.to_csv('alunos_limpeza_academica.csv', index=False)
alunos_nc.to_csv('alunos_nunca_compareceram.csv', index=False)
```

### Exemplo 5: Análise de Confiança

```python
# Alunos com alta confiança (>0.9)
alta_confianca = predicoes[predicoes['Confianca'] > 0.9]

# Alunos com média confiança (0.7-0.9)
media_confianca = predicoes[(predicoes['Confianca'] >= 0.7) & (predicoes['Confianca'] <= 0.9)]

# Alunos com baixa confiança (<0.7)
baixa_confianca = predicoes[predicoes['Confianca'] < 0.7]

print(f"Alta confiança: {len(alta_confianca)} ({len(alta_confianca)/len(predicoes)*100:.1f}%)")
print(f"Média confiança: {len(media_confianca)} ({len(media_confianca)/len(predicoes)*100:.1f}%)")
print(f"Baixa confiança: {len(baixa_confianca)} ({len(baixa_confianca)/len(predicoes)*100:.1f}%)")
```

### Exemplo 6: Monitoramento Contínuo

```python
import pandas as pd
from datetime import datetime

# Carregar histórico de predições
historico = pd.read_csv('historico_predicoes.csv')

# Adicionar novas predições
nova_data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
predicoes['data_predicao'] = nova_data

# Concatenar com histórico
historico = pd.concat([historico, predicoes], ignore_index=True)

# Salvar histórico atualizado
historico.to_csv('historico_predicoes.csv', index=False)

# Análise de tendência
print("Evolução do número de casos de risco:")
print(historico.groupby('data_predicao')['Eh_Risco'].sum())
```

---

## 🔗 Integração com AcadWeb

### Passo 1: Exportar Dados do AcadWeb

```bash
# No AcadWeb:
# 1. Acesse: Relatórios → Alunos Ativos
# 2. Selecione: Apenas Ativos
# 3. Exporte como: CSV ou Excel
# 4. Salve como: alunos_ativos_atual.csv
```

### Passo 2: Processar Dados

```python
import pandas as pd

# Carregar dados do AcadWeb
dados_acadweb = pd.read_csv('alunos_ativos_atual.csv', encoding='latin-1')

# Renomear colunas para padrão do sistema
mapeamento = {
    'Matrícula': 'Matricula',
    'Pendências Financeiras': 'Pend_Financ',
    'Faltas Consecutivas': 'Faltas_Consecutivas',
    'Pendências Acadêmicas': 'Pend_Acad',
    # ... adicionar outros mapeamentos
}

dados_processados = dados_acadweb.rename(columns=mapeamento)

# Salvar dados processados
dados_processados.to_csv('alunos_processados.csv', index=False)
```

### Passo 3: Fazer Predições

```python
from sistema_evasao_hibrido_expandido_producao import SistemaEvasaoHibridoExpandido

# Inicializar sistema
sistema = SistemaEvasaoHibridoExpandido()

# Carregar dados processados
dados = sistema.carregar_dados('alunos_processados.csv')

# Fazer predições
predicoes = sistema.prever(dados)

# Salvar resultados
sistema.salvar_resultados(predicoes, 'predicoes_acadweb.csv')
```

### Passo 4: Importar de Volta no AcadWeb

```bash
# No AcadWeb:
# 1. Acesse: Configurações → Importar Dados
# 2. Selecione: predicoes_acadweb.csv
# 3. Mapeie colunas corretamente
# 4. Importe dados
# 5. Verifique resultados
```

### API REST (Opcional)

Para integração mais robusta, você pode criar uma API REST:

```python
from flask import Flask, request, jsonify
from sistema_evasao_hibrido_expandido_producao import SistemaEvasaoHibridoExpandido

app = Flask(__name__)
sistema = SistemaEvasaoHibridoExpandido()

@app.route('/api/prever', methods=['POST'])
def prever():
    """Endpoint para fazer predições"""
    dados = request.json
    predicoes = sistema.prever(dados)
    return jsonify(predicoes.to_dict())

@app.route('/api/relatorio', methods=['GET'])
def relatorio():
    """Endpoint para gerar relatório"""
    dados = sistema.carregar_dados('alunos_ativos_atual_EXPANDIDO.csv')
    predicoes = sistema.prever(dados)
    relatorio = sistema.gerar_relatorio(predicoes)
    return jsonify(relatorio)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

---

## ⏰ Agendamento Automático

### Linux/Mac: Usando Crontab

```bash
# Abrir editor de crontab
crontab -e

# Adicionar agendamento (executar todo dia às 8h)
0 8 * * * /usr/bin/python3 /caminho/do/projeto/executar_predicoes.py

# Adicionar agendamento (executar toda segunda-feira às 9h)
0 9 * * 1 /usr/bin/python3 /caminho/do/projeto/executar_predicoes.py

# Adicionar agendamento (executar todo dia 1º do mês às 10h)
0 10 1 * * /usr/bin/python3 /caminho/do/projeto/executar_predicoes.py
```

### Windows: Usando Task Scheduler

```batch
# Criar arquivo executar_predicoes.bat
@echo off
cd C:\caminho\do\projeto
python3 executar_predicoes.py
pause
```

Depois, no Task Scheduler:

```
1. Abra Task Scheduler
2. Clique em "Create Basic Task"
3. Nome: "Predição de Evasão"
4. Trigger: Diário às 8h
5. Action: Executar executar_predicoes.bat
6. Clique em OK
```

### Script de Execução Automática

```python
# executar_predicoes.py
import os
import sys
import logging
from datetime import datetime
from sistema_evasao_hibrido_expandido_producao import SistemaEvasaoHibridoExpandido

# Configurar logging
logging.basicConfig(
    filename='predicoes.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def executar_predicoes():
    """Executa predições e salva resultados"""
    try:
        logging.info("Iniciando predições...")
        
        # Inicializar sistema
        sistema = SistemaEvasaoHibridoExpandido()
        
        # Carregar dados
        dados = sistema.carregar_dados('alunos_ativos_atual_EXPANDIDO.csv')
        logging.info(f"Dados carregados: {len(dados)} alunos")
        
        # Fazer predições
        predicoes = sistema.prever(dados)
        logging.info(f"Predições realizadas: {len(predicoes)} alunos")
        
        # Gerar relatório
        relatorio = sistema.gerar_relatorio(predicoes)
        logging.info("Relatório gerado")
        
        # Salvar resultados
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sistema.salvar_resultados(predicoes, f'predicoes_{timestamp}.csv')
        sistema.exportar_relatorio_json(predicoes, f'relatorio_{timestamp}.json')
        
        logging.info(f"Resultados salvos: predicoes_{timestamp}.csv")
        logging.info("Predições concluídas com sucesso!")
        
    except Exception as e:
        logging.error(f"Erro ao executar predições: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    executar_predicoes()
```

---

## 🔧 Troubleshooting

### Problema 1: Erro "ModuleNotFoundError"

**Sintoma:** `ModuleNotFoundError: No module named 'xgboost'`

**Solução:**

```bash
# Instalar dependências novamente
pip3 install -r requirements_producao.txt

# Ou instalar especificamente
pip3 install xgboost scikit-learn pandas numpy
```

### Problema 2: Erro "FileNotFoundError"

**Sintoma:** `FileNotFoundError: [Errno 2] No such file or directory: 'modelo_xgboost_expandido.joblib'`

**Solução:**

```bash
# Verificar se o arquivo existe
ls -la modelo_xgboost_expandido.joblib

# Se não existir, treinar o modelo novamente
python3 treinar_modelo_expandido.py
```

### Problema 3: Erro de Encoding

**Sintoma:** `UnicodeDecodeError: 'utf-8' codec can't decode byte...`

**Solução:**

```python
# Especificar encoding ao carregar dados
dados = pd.read_csv('arquivo.csv', encoding='latin-1')
# ou
dados = pd.read_csv('arquivo.csv', encoding='iso-8859-1')
```

### Problema 4: Memória Insuficiente

**Sintoma:** `MemoryError` ao processar grande volume de dados

**Solução:**

```python
# Processar dados em chunks
chunk_size = 100
for chunk in pd.read_csv('arquivo.csv', chunksize=chunk_size):
    predicoes = sistema.prever(chunk)
    sistema.salvar_resultados(predicoes, 'predicoes.csv', append=True)
```

### Problema 5: Modelo Desatualizado

**Sintoma:** Predições não correspondem aos dados atuais

**Solução:**

```bash
# Retreinar o modelo com dados novos
python3 treinar_modelo_expandido.py

# Verificar data do modelo
ls -l modelo_xgboost_expandido.joblib
```

---

## ❓ FAQ

### P: Com que frequência devo executar as predições?

**R:** Recomenda-se executar:
- **Diariamente:** Para monitoramento contínuo
- **Semanalmente:** Para relatórios gerenciais
- **Mensalmente:** Para análise estratégica
- **Semestralmente:** Para retreinamento do modelo

### P: Como interpretar a "Confiança"?

**R:** A confiança (0-1) indica o grau de certeza da predição:
- **> 0.9:** Muito confiável, agir imediatamente
- **0.7-0.9:** Confiável, monitorar
- **< 0.7:** Baixa confiança, revisar manualmente

### P: O que fazer com alunos em risco?

**R:** Ações recomendadas por categoria:
- **LFI:** Contato financeiro, plano de pagamento
- **LFR:** Orientação acadêmica, revisão de frequência
- **LAC:** Acompanhamento acadêmico, tutoria
- **NC:** Contato urgente, verificação de situação
- **Outros:** Monitoramento intensivo, apoio psicopedagógico

### P: Como garantir privacidade (LGPD)?

**R:** Medidas implementadas:
- Dados anonimizados (sem nomes, apenas matrícula)
- Armazenamento seguro (acesso restrito)
- Backup criptografado
- Logs de acesso
- Retenção limitada de dados

### P: Posso usar o modelo para outros cursos?

**R:** Sim, mas com cuidado:
- Modelo foi treinado com Grau Técnico
- Pode funcionar para cursos similares
- Recomenda-se retreinar com dados específicos
- Validar resultados antes de usar em produção

### P: Como retreinar o modelo?

**R:** Processo de retreinamento:

```bash
# 1. Coletar novos dados
# 2. Executar script de treinamento
python3 treinar_modelo_expandido.py

# 3. Validar novo modelo
python3 validar_modelo.py

# 4. Substituir modelo antigo
mv modelo_xgboost_expandido.joblib modelo_xgboost_expandido_backup.joblib
mv modelo_novo.joblib modelo_xgboost_expandido.joblib

# 5. Testar com dados reais
python3 teste_sistema.py
```

### P: Onde encontro suporte?

**R:** Canais de suporte:
- **Documentação:** Consulte DOCUMENTACAO_SISTEMA_PRODUCAO.md
- **Código:** Veja comentários no código-fonte
- **Orientador:** Prof. Dr. Leonardo Barreto Campos
- **Pesquisa:** Consulte ARTIGO_FINAL_ENRIQUECIDO.md

---

## 📞 Contato e Suporte

Para dúvidas ou problemas:

- **Email:** [seu_email@ifba.edu.br]
- **Telefone:** [seu_telefone]
- **Horário:** Segunda a sexta, 9h-17h
- **GitHub:** [link_do_repositorio]

---

## 📚 Referências

- ARTIGO_FINAL_ENRIQUECIDO.md - Fundamentação teórica completa
- DOCUMENTACAO_SISTEMA_PRODUCAO.md - Documentação técnica
- GUIA_RAPIDO_PRODUCAO.md - Guia rápido (5 minutos)
- Código-fonte comentado - Exemplos práticos

---

**Versão:** 2.0  
**Data:** Outubro de 2025  
**Status:** Pronto para Produção

**Boa sorte com o sistema! 🚀**
