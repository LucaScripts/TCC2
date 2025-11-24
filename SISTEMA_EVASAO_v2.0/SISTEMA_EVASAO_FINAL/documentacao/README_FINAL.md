# Sistema Híbrido Expandido de Predição de Evasão Estudantil

**Versão:** 2.0  
**Status:** Pronto para Produção  
**Autor:** Lucas Dias da Silva  
**Instituição:** IFBA - Instituto Federal de Educação, Ciência e Tecnologia da Bahia  
**Orientador:** Prof. Dr. Leonardo Barreto Campos  
**Data:** Outubro de 2025

---

## 📋 Descrição

Sistema que combina **Machine Learning (XGBoost)** com **regras de negócio institucionais** e **dados de satisfação estudantil** para predição robusta de risco de evasão em cursos técnicos.

### Componentes

1. **Machine Learning (XGBoost)**
   - Modelo treinado com 18 features (12 quantitativas + 6 qualitativas)
   - F1-Score: 0.2210 (validação cruzada)
   - Recall: 0.2222 (3.5x melhor que baseline)

2. **Regras de Negócio Institucionais**
   - LFI (Limpeza Financeira): Pendências financeiras ≥ 2
   - LFR (Limpeza de Frequência): Pendências + Faltas ≥ 12
   - LAC (Limpeza Acadêmica): Pendências acadêmicas ≥ 1
   - NC (Nunca Compareceu): Faltas ≥ 5
   - NF (Não Formados): Curso completo + pendências ≤ 2

3. **Dados de Satisfação Estudantil**
   - Satisfação Geral (1-5)
   - Qualidade do Ensino (1-5)
   - Motivação para Continuar (1-5)
   - Dificuldade de Aprendizado (1-5)
   - Pretende Desistir (0-2)
   - Avaliação do Professor (1-5)

---

## 🚀 Início Rápido

### 1. Instalação

```bash
# Clonar ou copiar os arquivos
cd /caminho/do/projeto

# Instalar dependências
pip3 install -r requirements_final.txt
```

### 2. Uso Básico

```python
from sistema_predicao_evasao_final import SistemaEvasaoHibridoExpandido

# Inicializar sistema
sistema = SistemaEvasaoHibridoExpandido()

# Carregar dados
dados = sistema.carregar_dados('alunos_ativos_atual_EXPANDIDO.csv')

# Fazer predições
predicoes = sistema.prever(dados)

# Salvar resultados
sistema.salvar_resultados(predicoes, 'predicoes.csv')

# Gerar relatório
relatorio = sistema.gerar_relatorio(predicoes)
print(f"Total de alunos: {relatorio['total_alunos']}")
print(f"Casos de risco: {relatorio['total_risco']} ({relatorio['percentual_risco']:.1f}%)")
```

### 3. Executar Exemplos

```bash
python3 sistema_predicao_evasao_final.py
```

---

## 📁 Estrutura de Arquivos

```
projeto/
├── sistema_predicao_evasao_final.py      # Sistema principal
├── treinar_modelo_final.py                # Script de treinamento
├── requirements_final.txt                 # Dependências
├── modelo_xgboost_expandido.joblib       # Modelo treinado
├── label_encoder_expandido.joblib        # Encoder de labels
├── Planilhabasedados_EXPANDIDO.csv       # Dados de treinamento
├── alunos_ativos_atual_EXPANDIDO.csv     # Dados de predição
├── README_FINAL.md                        # Este arquivo
└── logs/
    └── sistema_evasao.log                 # Arquivo de log
```

---

## 📊 Resultados

### Detecção de Casos de Risco

| Sistema | Casos | % | Melhoria |
|---------|-------|---|----------|
| ML Original (12F) | 45 | 4.7% | - |
| Híbrido Original (12F+R) | 117 | 12.3% | +160% |
| **Híbrido Expandido (18F+R)** | **172** | **18.0%** | **+282%** |

### Métricas de Desempenho

| Métrica | Valor |
|---------|-------|
| Acurácia | 0.7201 |
| Precisão | 0.2209 |
| Recall | 0.2222 |
| F1-Score | 0.2216 |
| F1-Score CV (5-fold) | 0.2210 |

### Importância das Features

**Top 5:**
1. Faltas Consecutivas (18.2%)
2. Pendências Financeiras (15.0%)
3. **Motivação para Continuar (12.2%)**
4. Dificuldade Disciplina (10.8%)
5. **Avaliação Professor (8.9%)**

---

## 🔧 Uso Avançado

### Análise por Categoria

```python
# Filtrar alunos em risco específico
alunos_lfi = sistema.analisar_categoria(predicoes, 'LFI')
alunos_lac = sistema.analisar_categoria(predicoes, 'LAC')

# Exportar por categoria
sistema.exportar_por_categoria(predicoes, 'predicoes_por_categoria')
```

### Agendamento Automático

#### Linux/Mac (Crontab)

```bash
# Executar diariamente às 8h
0 8 * * * /usr/bin/python3 /caminho/do/projeto/executar_predicoes.py

# Executar toda segunda-feira às 9h
0 9 * * 1 /usr/bin/python3 /caminho/do/projeto/executar_predicoes.py
```

#### Windows (Task Scheduler)

1. Abra Task Scheduler
2. Clique em "Create Basic Task"
3. Nome: "Predição de Evasão"
4. Trigger: Diário às 8h
5. Action: Executar script Python

### Integração com AcadWeb

```python
import pandas as pd

# Carregar dados do AcadWeb
dados_acadweb = pd.read_csv('alunos_ativos_atual.csv')

# Processar e fazer predições
sistema = SistemaEvasaoHibridoExpandido()
predicoes = sistema.prever(dados_acadweb)

# Exportar para reimportar no AcadWeb
predicoes.to_csv('predicoes_acadweb.csv', index=False)
```

---

## 📚 Documentação Completa

- **ARTIGO_FINAL_ENRIQUECIDO.md** - Fundamentação teórica (25-30 páginas)
- **RESUMO_EXECUTIVO_TCC2.md** - Visão geral executiva (5-7 páginas)
- **GUIA_COMPLETO_USO_SISTEMA.md** - Guia de uso detalhado (15+ páginas)
- **DOCUMENTACAO_SISTEMA_PRODUCAO.md** - Documentação técnica
- **GUIA_RAPIDO_PRODUCAO.md** - Guia rápido (5 minutos)
- **CHECKLIST_DEFESA_TCC2.md** - Checklist para defesa

---

## 🔍 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'xgboost'"

```bash
pip3 install -r requirements_final.txt
```

### Erro: "FileNotFoundError: modelo_xgboost_expandido.joblib"

Treinar o modelo:

```bash
python3 treinar_modelo_final.py
```

### Erro de Encoding

```python
# Especificar encoding ao carregar
dados = pd.read_csv('arquivo.csv', encoding='latin-1')
```

---

## 📞 Suporte

- **Documentação:** Consulte os arquivos .md
- **Código:** Veja comentários no código-fonte
- **Orientador:** Prof. Dr. Leonardo Barreto Campos
- **Email:** [seu_email@ifba.edu.br]

---

## 📄 Licença

Este projeto é fornecido para fins educacionais e de pesquisa.

---

## 🎓 Citação

Se usar este trabalho em pesquisa, cite como:

```bibtex
@mastersthesis{silva2025,
  author = {Silva, Lucas Dias da},
  title = {Sistema Híbrido Expandido de Predição de Evasão Estudantil},
  school = {Instituto Federal de Educação, Ciência e Tecnologia da Bahia},
  year = {2025},
  advisor = {Campos, Leonardo Barreto}
}
```

---

## ✅ Checklist de Implementação

- [ ] Instalar dependências
- [ ] Treinar modelo (ou usar modelo pré-treinado)
- [ ] Testar com dados de exemplo
- [ ] Integrar com AcadWeb
- [ ] Agendar execução automática
- [ ] Configurar alertas
- [ ] Treinar equipe
- [ ] Monitorar resultados

---

## 🚀 Próximos Passos

1. **Coleta de Dados Reais de Satisfação** - Implementar survey com alunos
2. **Validação do Modelo** - Treinar com dados reais
3. **Monitoramento de Efetividade** - Acompanhar impacto das intervenções
4. **Refinamento de Regras** - Ajustar critérios conforme aprendizado
5. **Expansão para Outros Cursos** - Adaptar modelo para outros programas

---

**Versão:** 2.0  
**Data:** Outubro de 2025  
**Status:** ✅ Pronto para Produção

**Boa sorte com o sistema! 🚀**
