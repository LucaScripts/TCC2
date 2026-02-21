# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Academic research project (TCC - Trabalho de Conclusão de Curso) from IFBA implementing a **Hybrid System for Predicting Academic Dropout Risk** in technical courses. The system combines XGBoost ML with business rules and student satisfaction data. Three versioned iterations exist showing the system's evolution.

## Commands

### V2.0 (Current Production Version)
Working directory: `SISTEMA_EVASAO_v2.0/SISTEMA_EVASAO_FINAL/`

```bash
# Install dependencies
pip install -r requirements_final.txt

# Train model from scratch
python codigo/treinar_modelo_final.py

# Run prediction system
python codigo/sistema_predicao_evasao_final.py

# Run usage example
python exemplos/exemplo_uso_basico.py
```

### V1.5 (Hybrid with Web Interface)
Working directory: `SISTEMA_EVASAO_v1.5/SISTEMA_PREDI--O_EVASAO-TCC2-main/SISTEMA_PREDIÇÃO_EVASAO/`

```bash
# Run automated tests
python test_sistema.py

# Run main system (verbose mode)
python principal.py --verboso

# Run with specific input file
python principal.py data/raw/alunos_ativos_atual.xlsx

# Start web interface
python interface_web.py
```

### Development tools (applicable to all versions)
```bash
black .          # code formatting
flake8 .         # linting
pytest           # run tests
```

## Architecture

### Three Versioned Systems

| Version | Location | Features | At-Risk Cases Detected |
|---------|----------|----------|----------------------|
| v1.0 | `SISTEMA_EVASAO_v1.0/` | ML-only baseline (RF, LR, XGBoost) | 45 (4.7%) |
| v1.5 | `SISTEMA_EVASAO_v1.5/` | Hybrid + modular architecture + web UI | 117 (12.3%) |
| v2.0 | `SISTEMA_EVASAO_v2.0/` | Hybrid + 6 satisfaction features | 172 (18.0%) |

### V2.0 Core Components (`codigo/`)

**`sistema_predicao_evasao_final.py`** — Main class `SistemaEvasaoHibridoExpandido` (570 lines):
- Loads input data (CSV/Excel), preprocesses, applies ML inference, then overlays business rules
- Outputs CSV report ready for Power BI or AcadWeb institutional system

**`treinar_modelo_final.py`** — Training pipeline (283 lines):
- 5-fold StratifiedKFold cross-validation
- Serializes model and encoders via joblib
- Reports accuracy (0.7201) and F1 (0.2216)

### Prediction Pipeline

```
Input Data (CSV/Excel, 18 features)
    ↓ Preprocessing (median imputation, StandardScaler)
    ↓
    ├─→ XGBoost ML (10-class classifier)
    │       12 quantitative features + 6 satisfaction features
    │
    └─→ Business Rules Engine (cascading priority)
            LFI → LFR → LAC → NC → NF → MT
    ↓
Merged Results (ML predictions override rule classifications)
    ↓
CSV Export (Power BI / AcadWeb compatible)
```

### Business Rule Priority Order (V2.0/V1.5)

Rules are applied in this cascade — the first matching rule wins:
1. **LFI** (Limpeza Financeira): ≥2 financial pendencies
2. **LFR** (Limpeza de Frequência): ≥12 consecutive absences
3. **LAC** (Limpeza Acadêmica): ≥1 academic pendency
4. **NC** (Nunca Compareceu): ≥5 absences
5. **NF** (Não Formados): course completed + ≤2 pendencies
6. **MT** (Matriculado): default

### V1.5 Modular Architecture (`codigo_fonte/`)

More structured than V2.0, organized into:
- `configuracao/` — configuration management
- `modelos/` — ML model wrappers
- `nucleo/` — core prediction orchestration
- `regras_negocio/` — business rule implementations
- `utilitarios/` — logging and data utilities

### Configuration (`config.ini` — V2.0 only)

Stores system metadata, model parameters, performance metrics, and detection stats. Not used at runtime for prediction logic — primarily for documentation and versioning.

### Target Classes (10 enrollment statuses)

`MT`, `LFI`, `LFR`, `LAC`, `NC`, `NF`, `CAC`, `CAN`, `FO`, `TF`

### Data

- Training: `dados/Planilhabasedados_EXPANDIDO.csv` (~4,516 records, 2020–2025)
- Operational input: Excel or CSV with 18 required columns
- The 6 satisfaction features (motivation, intent to drop out, professor evaluation, etc.) are currently simulated in the dataset — real survey integration is a pending improvement
