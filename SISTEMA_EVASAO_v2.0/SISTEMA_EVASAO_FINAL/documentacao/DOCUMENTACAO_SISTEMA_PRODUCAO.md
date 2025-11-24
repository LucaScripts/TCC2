# Documentação Técnica - Sistema Híbrido Expandido de Predição de Evasão Estudantil

## Versão 2.0 (Produção)

---

## 1. Visão Geral do Sistema

O Sistema Híbrido Expandido é uma solução integrada para predição precoce de risco de evasão estudantil que combina três componentes principais:

1. **Machine Learning (XGBoost):** Modelo treinado com 18 features (12 quantitativas + 6 qualitativas)
2. **Regras de Negócio Institucionais:** Classificações baseadas em critérios administrativos
3. **Dados de Satisfação Estudantil:** Features qualitativas que capturam percepção e motivação

### Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    DADOS DE ENTRADA                         │
│  (954 alunos com 18 features: 12 quant + 6 qualitativas)   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────┐
        │   PREPROCESSAMENTO DE DADOS      │
        │  - Normalização                  │
        │  - Tratamento de faltantes       │
        │  - Validação de features         │
        └──────────────────┬───────────────┘
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
        ┌─────────────────┐   ┌──────────────────┐
        │  ML (XGBoost)   │   │  REGRAS NEGÓCIO  │
        │  18 Features    │   │  (LFI, LFR, etc) │
        │  Predição ML    │   │  Critérios Admin │
        └────────┬────────┘   └────────┬─────────┘
                 │                     │
                 └──────────┬──────────┘
                            ▼
                  ┌──────────────────────┐
                  │  CLASSIFICAÇÃO FINAL │
                  │  (Regras sobrescr ML)│
                  └──────────┬───────────┘
                             ▼
                  ┌──────────────────────┐
                  │  RELATÓRIO FINAL     │
                  │  - Predições         │
                  │  - Categorias Risco  │
                  │  - Estatísticas      │
                  └──────────────────────┘
```

---

## 2. Features do Sistema

### 2.1 Features Quantitativas (12)

| # | Feature | Escala | Tipo | Descrição |
|---|---------|--------|------|-----------|
| 1 | Pend. Financ. | 0-N | Contagem | Número de parcelas em aberto |
| 2 | Faltas Consecutivas | 0-N | Contagem | Máximo de faltas consecutivas |
| 3 | Pend. Acad. | 0-N | Contagem | Número de disciplinas com pendência |
| 4 | Semestre | 1-N | Ordinal | Semestre atual do aluno |
| 5 | Idade | 18-70 | Contínua | Idade em anos |
| 6 | Sexo | 0-1 | Binária | 0=Feminino, 1=Masculino |
| 7 | Turno | 0-2 | Categórica | 0=Matutino, 1=Vespertino, 2=Noturno |
| 8 | Renda Familiar | 1-5 | Ordinal | Faixa de renda (1=Baixa, 5=Alta) |
| 9 | Distância Campus | 0-100 | Contínua | Distância em km |
| 10 | Tempo Deslocamento | 0-180 | Contínua | Tempo em minutos |
| 11 | Dificuldade Disciplina | 1-5 | Ordinal | Média de dificuldade |
| 12 | Trabalha | 0-1 | Binária | 0=Não, 1=Sim |

### 2.2 Features Qualitativas de Satisfação (6)

| # | Feature | Escala | Correlação | Descrição |
|---|---------|--------|-----------|-----------|
| 1 | Satisfacao_Geral | 1-5 | Inversa | Avaliação geral da experiência |
| 2 | Qualidade_Ensino | 1-5 | Inversa | Percepção de qualidade das aulas |
| 3 | Motivacao_Continuar | 1-5 | Inversa | Nível de motivação |
| 4 | Dificuldade_Aprendizado | 1-5 | Direta | Percepção de dificuldade |
| 5 | Pretende_Desistir | 0-2 | Direta | 0=Não, 1=Talvez, 2=Sim |
| 6 | Avaliacao_Professor | 1-5 | Inversa | Percepção sobre docente |

**Nota:** Correlação Inversa = menor valor = maior risco; Correlação Direta = maior valor = maior risco

---

## 3. Regras de Negócio Institucionais

As regras são aplicadas em cascata (ordem de prioridade):

### Regra 1: Limpeza Financeira (LFI)
- **Critério:** ≥2 parcelas em aberto
- **Ação:** Contato financeiro, plano de pagamento
- **Prioridade:** Máxima

### Regra 2: Limpeza de Frequência (LFR)
- **Critério:** Pendências financeiras + ≥12 faltas consecutivas
- **Ação:** Contato urgente, orientação acadêmica
- **Prioridade:** Alta

### Regra 3: Limpeza Acadêmica (LAC)
- **Critério:** ≥1 disciplina com pendência (PR, PV, PF)
- **Ação:** Orientação acadêmica, reforço
- **Prioridade:** Alta

### Regra 4: Nunca Compareceu (NC)
- **Critério:** ≥5 faltas consecutivas na primeira disciplina
- **Ação:** Contato urgente, verificação de situação
- **Prioridade:** Máxima

### Regra 5: Não Formados (NF)
- **Critério:** Completou curso + ≤2 parcelas pendentes
- **Ação:** Acompanhamento para conclusão
- **Prioridade:** Média

### Classificação Padrão: Matriculado (MT)
- **Critério:** Nenhuma regra aplicável
- **Ação:** Monitoramento padrão
- **Prioridade:** Baixa

---

## 4. Instalação e Configuração

### 4.1 Requisitos

```bash
Python 3.8+
pandas>=1.3.0
numpy>=1.20.0
scikit-learn>=1.0.0
xgboost>=1.5.0
joblib>=1.0.0
```

### 4.2 Instalação

```bash
# Clonar repositório
git clone <url-repositorio>
cd sistema-evasao

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 4.3 Arquivos Necessários

```
projeto/
├── sistema_evasao_hibrido_expandido_producao.py  # Código principal
├── modelo_xgboost_expandido.joblib               # Modelo treinado
├── label_encoder_expandido.joblib                # Label encoder
├── alunos_ativos_atual_EXPANDIDO.csv             # Dados de entrada
└── output/
    ├── predicoes_evasao_final.csv                # Resultados
    └── relatorio_predicoes.json                  # Relatório
```

---

## 5. Uso do Sistema

### 5.1 Uso Básico

```python
from sistema_evasao_hibrido_expandido_producao import SistemaEvasaoHibridoExpandido
import pandas as pd

# Inicializar sistema
sistema = SistemaEvasaoHibridoExpandido()

# Carregar modelo
sistema.carregar_modelo(
    'modelo_xgboost_expandido.joblib',
    'label_encoder_expandido.joblib'
)

# Carregar dados
dados = pd.read_csv('alunos_ativos_atual_EXPANDIDO.csv')

# Realizar predição
resultados = sistema.prever(dados, usar_regras=True)

# Gerar relatório
relatorio = sistema.gerar_relatorio(resultados)

# Salvar resultados
sistema.salvar_resultados(resultados, 'output/predicoes.csv')
sistema.exportar_relatorio_json(relatorio, 'output/relatorio.json')
```

### 5.2 Uso Avançado

```python
# Predição sem regras (apenas ML)
resultados_ml = sistema.prever(dados, usar_regras=False)

# Acessar apenas alunos em risco
alunos_risco = resultados[resultados['Eh_Risco']]
print(f"Total de alunos em risco: {len(alunos_risco)}")

# Filtrar por categoria específica
alunos_lfi = resultados[resultados['Predicao_Final'] == 'LFI']
print(f"Alunos com Limpeza Financeira: {len(alunos_lfi)}")

# Comparar predição ML vs Final
diferenças = resultados[resultados['Predicao_ML'] != resultados['Predicao_Final']]
print(f"Casos onde regras modificaram predição: {len(diferenças)}")
```

---

## 6. Estrutura de Saída

### 6.1 DataFrame de Resultados

O DataFrame retornado por `prever()` contém:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| Matricula | str | ID do aluno |
| Pend. Financ. | float | Features quantitativas originais |
| ... | ... | ... |
| Satisfacao_Geral | float | Features qualitativas de satisfação |
| ... | ... | ... |
| Predicao_ML | str | Predição do modelo ML puro |
| Predicao_Final | str | Predição final (com regras) |
| Eh_Risco | bool | True se é caso de risco |
| Categoria_Risco | str | Descrição da categoria |

### 6.2 Relatório JSON

```json
{
  "data_geracao": "2025-10-31T14:30:00",
  "total_alunos": 954,
  "casos_risco": 172,
  "taxa_risco_percentual": "18.0%",
  "alunos_matriculados": 782,
  "distribuicao_categorias": {
    "Matriculado": 782,
    "Limpeza Acadêmica": 78,
    "Limpeza Financeira": 8,
    "Nunca Compareceu": 9,
    "Não Formados": 5,
    "Categoria Adicional 1": 48,
    "Categoria Adicional 2": 48,
    "Fora": 4,
    "Transferência": 3
  }
}
```

---

## 7. Métricas de Desempenho

### 7.1 Desempenho do Modelo

| Métrica | Valor | Interpretação |
|---------|-------|---|
| Acurácia | 0.7201 | 72% de predições corretas |
| Precisão Média | 0.2209 | 22% de precisão em casos de risco |
| Recall Médio | 0.2222 | 22% de recall (detecção de positivos) |
| F1-Score | 0.2216 | Média harmônica de precisão e recall |
| F1-Score (CV 5-fold) | 0.2210 | Validação cruzada estável |

### 7.2 Impacto das Melhorias

| Componente | Casos Detectados | Taxa | Melhoria |
|---|---|---|---|
| ML Original (12F) | 45 | 4.7% | - |
| Híbrido Original (12F+R) | 117 | 12.3% | +160% |
| Híbrido Expandido (18F+R) | 172 | 18.0% | +47% (vs Híbrido Original) |
| | | | **+282%** (vs ML Original) |

---

## 8. Troubleshooting

### Problema: "Modelo não foi carregado"

**Solução:** Certifique-se de chamar `carregar_modelo()` antes de `prever()`:

```python
sistema.carregar_modelo('modelo.joblib', 'label_encoder.joblib')
```

### Problema: "Features faltando"

**Solução:** Verifique se o CSV contém todas as 18 features com nomes exatos:

```python
# Verificar features disponíveis
print(dados.columns.tolist())

# Deve conter todas estas:
print(SistemaEvasaoHibridoExpandido.TODAS_FEATURES)
```

### Problema: "Erro ao realizar predição"

**Solução:** Verifique se os dados foram preprocessados corretamente:

```python
# Verificar tipos de dados
print(dados.dtypes)

# Verificar valores faltantes
print(dados.isnull().sum())

# Verificar escala de valores
print(dados.describe())
```

---

## 9. Boas Práticas

### 9.1 Validação de Dados

```python
# Sempre validar dados antes de predição
if not sistema._validar_features(dados):
    print("Dados inválidos!")
    return

# Verificar distribuição de dados
print(dados[sistema.TODAS_FEATURES].describe())
```

### 9.2 Monitoramento

```python
# Registrar predições para auditoria
resultados.to_csv(f'predicoes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')

# Monitorar mudanças em predições
print(f"Mudanças de predição: {(resultados['Predicao_ML'] != resultados['Predicao_Final']).sum()}")
```

### 9.3 Atualização de Modelo

```python
# Periodicamente retreinar modelo com novos dados
# Recomendação: A cada semestre ou quando taxa de erro aumentar >5%

from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

# Carregar dados históricos
dados_historicos = pd.read_csv('historico_completo.csv')

# Retreinar
X = dados_historicos[sistema.TODAS_FEATURES]
y = dados_historicos['Resultado_Real']

modelo_novo = XGBClassifier(max_depth=6, learning_rate=0.1, n_estimators=100)
modelo_novo.fit(X, y)

# Salvar novo modelo
joblib.dump(modelo_novo, 'modelo_xgboost_expandido_v2.joblib')
```

---

## 10. Integração com Sistemas Existentes

### 10.1 Integração com AcadWeb

```python
# Exemplo de integração com API do AcadWeb
import requests

# Buscar dados de alunos
response = requests.get('https://acadweb.instituicao.edu.br/api/alunos')
dados_json = response.json()

# Converter para DataFrame
dados = pd.DataFrame(dados_json)

# Realizar predição
resultados = sistema.prever(dados)

# Enviar alertas para sistema
for idx, row in resultados[resultados['Eh_Risco']].iterrows():
    requests.post(
        'https://acadweb.instituicao.edu.br/api/alertas',
        json={
            'matricula': row['Matricula'],
            'categoria': row['Categoria_Risco'],
            'timestamp': datetime.now().isoformat()
        }
    )
```

### 10.2 Agendamento Automático

```bash
# Crontab (Linux/Mac) - Executar predição diariamente às 8h
0 8 * * * cd /caminho/projeto && python sistema_evasao_hibrido_expandido_producao.py

# Windows Task Scheduler
# Criar tarefa agendada que execute: python sistema_evasao_hibrido_expandido_producao.py
```

---

## 11. Referências e Documentação

- **XGBoost:** https://xgboost.readthedocs.io/
- **Scikit-learn:** https://scikit-learn.org/
- **Pandas:** https://pandas.pydata.org/
- **Joblib:** https://joblib.readthedocs.io/

---

## 12. Suporte e Contato

Para dúvidas ou problemas:

1. Consulte a seção Troubleshooting (Seção 8)
2. Verifique os logs do sistema (arquivo `.log`)
3. Valide os dados de entrada (Seção 9.1)
4. Entre em contato com a equipe de desenvolvimento

---

**Versão:** 2.0  
**Data:** 2025-10-31  
**Status:** Produção  
**Última Atualização:** 2025-10-31
