# Guia Rápido - Sistema Híbrido Expandido de Predição de Evasão

## ⚡ Início Rápido (5 minutos)

### 1. Instalação

```bash
# Clonar ou baixar o projeto
cd sistema-evasao

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac ou venv\Scripts\activate (Windows)

# Instalar dependências
pip install -r requirements_producao.txt
```

### 2. Preparar Dados

Seu arquivo CSV deve conter estas 18 colunas:

**Features Quantitativas (12):**
- Pend. Financ.
- Faltas Consecutivas
- Pend. Acad.
- Semestre
- Idade
- Sexo
- Turno
- Renda Familiar
- Distância Campus
- Tempo Deslocamento
- Dificuldade Disciplina
- Trabalha

**Features Qualitativas (6):**
- Satisfacao_Geral (1-5)
- Qualidade_Ensino (1-5)
- Motivacao_Continuar (1-5)
- Dificuldade_Aprendizado (1-5)
- Pretende_Desistir (0-2)
- Avaliacao_Professor (1-5)

### 3. Executar Predição

```python
from sistema_evasao_hibrido_expandido_producao import SistemaEvasaoHibridoExpandido
import pandas as pd

# Inicializar
sistema = SistemaEvasaoHibridoExpandido()

# Carregar modelo
sistema.carregar_modelo(
    'modelo_xgboost_expandido.joblib',
    'label_encoder_expandido.joblib'
)

# Carregar dados
dados = pd.read_csv('seus_dados.csv')

# Prever
resultados = sistema.prever(dados)

# Salvar
sistema.salvar_resultados(resultados, 'output/predicoes.csv')
```

### 4. Visualizar Resultados

```python
# Relatório
relatorio = sistema.gerar_relatorio(resultados)
print(f"Total de alunos: {relatorio['total_alunos']}")
print(f"Casos de risco: {relatorio['casos_risco']} ({relatorio['taxa_risco_percentual']})")

# Alunos em risco
alunos_risco = resultados[resultados['Eh_Risco']]
print(alunos_risco[['Matricula', 'Categoria_Risco']].head(10))
```

---

## 📊 Interpretação de Resultados

### Categorias de Risco

| Categoria | Sigla | Significado | Ação Recomendada |
|---|---|---|---|
| Matriculado | MT | Sem indicadores de risco | Monitoramento padrão |
| Limpeza Financeira | LFI | ≥2 parcelas em aberto | Contato financeiro |
| Limpeza de Frequência | LFR | Faltas + Pendências | Orientação acadêmica |
| Limpeza Acadêmica | LAC | Pendências acadêmicas | Reforço acadêmico |
| Nunca Compareceu | NC | ≥5 faltas consecutivas | Contato urgente |
| Não Formados | NF | Curso completo + pendências | Acompanhamento |

### Exemplo de Saída

```
Total de alunos: 954
Casos de risco: 172 (18.0%)

Distribuição:
  - Matriculado: 782
  - Limpeza Acadêmica: 78
  - Limpeza Financeira: 8
  - Nunca Compareceu: 9
  - Não Formados: 5
  - Outros: 72
```

---

## 🔍 Casos de Uso Comuns

### Caso 1: Identificar Alunos em Alto Risco

```python
# Alunos que precisam intervenção imediata
alunos_criticos = resultados[
    resultados['Predicao_Final'].isin(['LFI', 'NC', 'LFR'])
]
print(f"Alunos em situação crítica: {len(alunos_criticos)}")
alunos_criticos.to_csv('alunos_criticos.csv')
```

### Caso 2: Monitorar Mudanças de Predição

```python
# Casos onde regras modificaram predição ML
mudancas = resultados[
    resultados['Predicao_ML'] != resultados['Predicao_Final']
]
print(f"Predições modificadas por regras: {len(mudancas)}")
```

### Caso 3: Análise por Categoria

```python
# Alunos com Limpeza Acadêmica
lac = resultados[resultados['Predicao_Final'] == 'LAC']
print(f"Alunos com pendências acadêmicas: {len(lac)}")
print(lac[['Matricula', 'Pend. Acad.', 'Motivacao_Continuar']])
```

### Caso 4: Correlação com Satisfação

```python
# Alunos em risco com baixa satisfação
baixa_satisfacao = resultados[
    (resultados['Eh_Risco']) & 
    (resultados['Satisfacao_Geral'] <= 2)
]
print(f"Alunos em risco com baixa satisfação: {len(baixa_satisfacao)}")
```

---

## ⚙️ Configuração Avançada

### Desabilitar Regras de Negócio

```python
# Usar apenas predição ML (sem regras)
resultados_ml = sistema.prever(dados, usar_regras=False)
```

### Comparar ML vs Híbrido

```python
# Predição com e sem regras
resultado_ml = sistema.prever(dados, usar_regras=False)
resultado_hibrido = sistema.prever(dados, usar_regras=True)

# Comparar
comparacao = pd.DataFrame({
    'Matricula': dados['Matricula'],
    'ML': resultado_ml['Predicao_Final'],
    'Hibrido': resultado_hibrido['Predicao_Final']
})

mudancas = comparacao[comparacao['ML'] != comparacao['Hibrido']]
print(f"Mudanças de predição: {len(mudancas)}")
```

---

## 📈 Monitoramento Contínuo

### Agendamento Automático (Linux/Mac)

```bash
# Adicionar ao crontab (crontab -e)
# Executar predição diariamente às 8h
0 8 * * * cd /caminho/projeto && python -c "
from sistema_evasao_hibrido_expandido_producao import SistemaEvasaoHibridoExpandido
import pandas as pd
from datetime import datetime

sistema = SistemaEvasaoHibridoExpandido()
sistema.carregar_modelo('modelo_xgboost_expandido.joblib', 'label_encoder_expandido.joblib')
dados = pd.read_csv('alunos_ativos.csv')
resultados = sistema.prever(dados)
sistema.salvar_resultados(resultados, f'output/predicoes_{datetime.now().strftime(\"%Y%m%d\")}.csv')
"
```

### Agendamento Automático (Windows)

```powershell
# Criar arquivo run_predicoes.ps1
$sistema = New-Object -ComObject System.Diagnostics.ProcessStartInfo
$sistema.FileName = "python"
$sistema.Arguments = "sistema_evasao_hibrido_expandido_producao.py"
$sistema.WorkingDirectory = "C:\caminho\projeto"
Start-Process $sistema

# Usar Windows Task Scheduler para agendar
```

---

## 🐛 Problemas Comuns

### Erro: "Modelo não foi carregado"

```python
# ❌ Errado
resultados = sistema.prever(dados)

# ✅ Correto
sistema.carregar_modelo('modelo.joblib', 'label_encoder.joblib')
resultados = sistema.prever(dados)
```

### Erro: "Features faltando"

```python
# Verificar colunas disponíveis
print("Colunas no CSV:", dados.columns.tolist())

# Comparar com esperadas
print("Colunas esperadas:", sistema.TODAS_FEATURES)

# Renomear se necessário
dados = dados.rename(columns={'PendFinanceira': 'Pend. Financ.'})
```

### Erro: "Valores faltantes"

```python
# O sistema trata automaticamente, mas você pode verificar:
print(dados.isnull().sum())

# Ou preencher manualmente:
dados = dados.fillna(dados.mean(numeric_only=True))
```

---

## 📞 Suporte

Para problemas:

1. Verifique os logs: `cat sistema_predicao.log`
2. Valide os dados: `python -c "import pandas as pd; print(pd.read_csv('dados.csv').info())"`
3. Teste com dados de exemplo
4. Consulte a documentação completa: `DOCUMENTACAO_SISTEMA_PRODUCAO.md`

---

## 🚀 Próximos Passos

1. **Validar com dados reais:** Testar com dados históricos
2. **Ajustar regras:** Customizar critérios conforme instituição
3. **Integrar com AcadWeb:** Conectar com sistema acadêmico
4. **Monitorar performance:** Acompanhar acurácia ao longo do tempo
5. **Retreinar modelo:** Periodicamente com novos dados

---

**Versão:** 2.0  
**Última atualização:** 2025-10-31  
**Status:** Pronto para Produção ✅
