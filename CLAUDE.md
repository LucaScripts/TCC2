# CLAUDE.md

Este arquivo fornece orientações ao Claude Code (claude.ai/code) ao trabalhar com o código neste repositório.

## Visão Geral do Projeto

Projeto de pesquisa acadêmica (TCC - Trabalho de Conclusão de Curso) do IFBA implementando um **Sistema Híbrido de Predição de Risco de Evasão Acadêmica** em cursos técnicos. O sistema combina ML com XGBoost, regras de negócio e dados de satisfação dos alunos. Existem três versões iterativas que mostram a evolução do sistema.

## Comandos

### V2.0 (Versão de Produção Atual)
Diretório de trabalho: `SISTEMA_EVASAO_v2.0/SISTEMA_EVASAO_FINAL/`

```bash
# Instalar dependências
pip install -r requirements_final.txt

# Treinar modelo do zero
python codigo/treinar_modelo_final.py

# Executar sistema de predição
python codigo/sistema_predicao_evasao_final.py

# Executar exemplo de uso
python exemplos/exemplo_uso_basico.py
```

### V1.5 (Híbrido com Interface Web)
Diretório de trabalho: `SISTEMA_EVASAO_v1.5/SISTEMA_PREDI--O_EVASAO-TCC2-main/SISTEMA_PREDIÇÃO_EVASAO/`

```bash
# Executar testes automatizados
python test_sistema.py

# Executar sistema principal (modo verboso)
python principal.py --verboso

# Executar com arquivo de entrada específico
python principal.py data/raw/alunos_ativos_atual.xlsx

# Iniciar interface web
python interface_web.py
```

### Ferramentas de desenvolvimento (aplicáveis a todas as versões)
```bash
black .          # formatação de código
flake8 .         # linting
pytest           # executar testes
```

## Arquitetura

### Três Sistemas Versionados

| Versão | Localização | Funcionalidades | Casos de Risco Detectados |
|--------|-------------|-----------------|--------------------------|
| v1.0 | `SISTEMA_EVASAO_v1.0/` | Baseline apenas ML (RF, LR, XGBoost) | 45 (4,7%) |
| v1.5 | `SISTEMA_EVASAO_v1.5/` | Híbrido + arquitetura modular + UI web | 117 (12,3%) |
| v2.0 | `SISTEMA_EVASAO_v2.0/` | Híbrido + 6 features de satisfação | 172 (18,0%) |

### Componentes Principais da V2.0 (`codigo/`)

**`sistema_predicao_evasao_final.py`** — Classe principal `SistemaEvasaoHibridoExpandido` (570 linhas):
- Carrega dados de entrada (CSV/Excel), pré-processa, aplica inferência ML e sobrepõe regras de negócio
- Gera relatório CSV pronto para Power BI ou sistema institucional AcadWeb

**`treinar_modelo_final.py`** — Pipeline de treinamento (283 linhas):
- Validação cruzada StratifiedKFold com 5 folds
- Serializa modelo e encoders via joblib
- Reporta acurácia (0,7201) e F1 (0,2216)

### Pipeline de Predição

```
Dados de Entrada (CSV/Excel, 18 features)
    ↓ Pré-processamento (imputação por mediana, StandardScaler)
    ↓
    ├─→ ML XGBoost (classificador de 10 classes)
    │       12 features quantitativas + 6 features de satisfação
    │
    └─→ Motor de Regras de Negócio (prioridade em cascata)
            LFI → LFR → LAC → NC → NF → MT
    ↓
Resultados Mesclados (predições ML sobrepõem classificações por regras)
    ↓
Exportação CSV (compatível com Power BI / AcadWeb)
```

### Ordem de Prioridade das Regras de Negócio (V2.0/V1.5)

As regras são aplicadas em cascata — a primeira regra que corresponder vence:
1. **LFI** (Limpeza Financeira): ≥2 pendências financeiras
2. **LFR** (Limpeza de Frequência): ≥12 faltas consecutivas
3. **LAC** (Limpeza Acadêmica): ≥1 pendência acadêmica
4. **NC** (Nunca Compareceu): ≥5 faltas
5. **NF** (Não Formados): curso concluído + ≤2 pendências
6. **MT** (Matriculado): padrão

### Arquitetura Modular da V1.5 (`codigo_fonte/`)

Mais estruturada que a V2.0, organizada em:
- `configuracao/` — gerenciamento de configurações
- `modelos/` — wrappers de modelos ML
- `nucleo/` — orquestração central das predições
- `regras_negocio/` — implementações das regras de negócio
- `utilitarios/` — utilitários de logging e dados

### Configuração (`config.ini` — apenas V2.0)

Armazena metadados do sistema, parâmetros do modelo, métricas de desempenho e estatísticas de detecção. Não é usado em tempo de execução para a lógica de predição — serve principalmente para documentação e versionamento.

### Classes Alvo (10 situações de matrícula)

`MT`, `LFI`, `LFR`, `LAC`, `NC`, `NF`, `CAC`, `CAN`, `FO`, `TF`

### Dados

- Treinamento: `dados/Planilhabasedados_EXPANDIDO.csv` (~4.516 registros, 2020–2025)
- Entrada operacional: Excel ou CSV com 18 colunas obrigatórias
- As 6 features de satisfação (motivação, intenção de desistir, avaliação do professor, etc.) são atualmente simuladas no dataset — a integração com pesquisa real é uma melhoria pendente
