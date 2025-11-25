# Classificação de Risco de Evasão Acadêmica — TCC (Resumo Didático)

Autores: Lucas Dias da Silva e Leonardo Barreto Campos

Instituição: Coordenação de Sistemas de Informação — IFBA, Vitória da Conquista

---

Visão geral
---------
Este repositório apresenta um sistema híbrido para predição de risco de evasão no Grau Técnico (Vitória da Conquista). O sistema integra um modelo de Machine Learning (XGBoost multiclasse), regras de negócio institucionais e dados de satisfação discente (se disponíveis) para classificar a situação final da matrícula e priorizar intervenções via um dashboard em Power BI.

Objetivo
--------
- Estimar situações finais de matrícula (ex.: MT, LFI, LFR, LAC, NC, NF) a partir de 18 variáveis (12 acadêmico-administrativas + 6 de satisfação).
- Maximizar Recall-macro e F1-macro nas classes minoritárias (casos de risco) para priorizar ações pedagógicas.

Como o sistema funciona (resumo do pipeline)
------------------------------------------
1. ETL e padronização: limpeza, mapeamento de variáveis e codificação para um esquema de 18 colunas.
2. Treinamento: XGBoost multiclasse com validação cruzada 5-fold e pesos por classe; geração de artefatos (modelo, encoders, relatórios).
3. Produção (em lote): aplicação das transformações, inferência com o modelo ML, posterior aplicação de regras de negócio em cascata para ajustar/confirmar predições.
4. Exportação: CSV final com Predicao_ML, Predicao_Final, top-k, probabilidades e indicadores auxiliares para consumo no Power BI.
5. Explicabilidade: geração opcional de valores SHAP para justificar predições individuais.

Principais diferenças entre versões
---------------------------------
- v1.0 — ML puro (12 variáveis quantitativas). Baseline: XGBoost e comparativos com Random Forest e Regressão Logística.
- v1.5 — Híbrido (ML + Regras) sobre as mesmas 12 variáveis; regras permitem capturar eventos institucionais explícitos.
- v2.0 — Híbrido expandido (18 variáveis): inclui 6 variáveis de satisfação simuladas; mostrou aumento substancial de sensibilidade (Recall/F1-macro), porém depende de coleta real para validação definitiva.

Resultados resumidos
--------------------
- Base de treino: n ≈ 4.516 (período 2020–2025).
- Amostra operacional: n = 954 (último período analisado).
- v2.0 (ensaiada): F1-macro ≈ 0,221; Recall-macro ≈ 0,222; identifica 172 alunos em risco (≈18% da amostra operacional), representando ganho de sensibilidade ≈ +282% frente ao baseline v1.0.

Arquivos e localização (principais)
----------------------------------
- Pipeline e scripts de treino/produção: `SISTEMA_EVASAO_v2.0/SISTEMA_EVASAO_FINAL/codigo/treinar_modelo_final.py` e `SISTEMA_EVASAO_v2.0/SISTEMA_EVASAO_FINAL/codigo/sistema_predicao_evasao_final.py`.
- Modelos e artefatos serializados: `SISTEMA_EVASAO_v2.0/SISTEMA_EVASAO_FINAL/modelos/` (joblib/pkl).
- Scripts auxiliares e análises (TCC1): `TCC1-main/` — contém preprocessamento, scripts de previsão e arquivos de saída.
- Dados de exemplo e saídas: `SISTEMA_EVASAO_v2.0/SISTEMA_EVASAO_FINAL/dados/` e `SISTEMA_EVASAO_v2.0/SISTEMA_EVASAO_FINAL/output/`.
- Dashboard Power BI: arquivos gerados em CSV compatíveis com o `Dashboard/` (pasta de consumo do Power BI).

Como executar (exemplo mínimo — PowerShell)
-----------------------------------------
1) Criar/ativar ambiente Python e instalar dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r c:\Users\lucas\Downloads\TCC\SISTEMA_EVASAO_v2.0\SISTEMA_EVASAO_FINAL\requirements_final.txt
```

2) Treinar modelo (exemplo):

```powershell
python c:\Users\lucas\Downloads\TCC\SISTEMA_EVASAO_v2.0\SISTEMA_EVASAO_FINAL\codigo\treinar_modelo_final.py
```

3) Executar rotina de produção (inferência + regras):

```powershell
python c:\Users\lucas\Downloads\TCC\SISTEMA_EVASAO_v2.0\SISTEMA_EVASAO_FINAL\codigo\sistema_predicao_evasao_final.py \
  --input c:\Users\lucas\Downloads\TCC\SISTEMA_EVASAO_v2.0\SISTEMA_EVASAO_FINAL\dados\operacionais.csv \
  --output c:\Users\lucas\Downloads\TCC\SISTEMA_EVASAO_v2.0\SISTEMA_EVASAO_FINAL\output\predicoes_YYYYMM.csv
```

Observações:
- Ajuste caminhos conforme seu ambiente. Alguns scripts no TCC1-main (ex.: `predict_new_students_unified_v4.py`) são versões auxiliares; prefira os scripts em `SISTEMA_EVASAO_v2.0` para produção.
- Se preferir, rode os scripts com o Python do ambiente Conda em vez de venv.

Governança, LGPD e boas práticas
--------------------------------
- Dados pessoais devem ser tratados conforme LGPD: anonimização, minimização e controle de acesso aos artefatos.
- Versionamento: sempre gravar metadados (hash do modelo, data-corte, conjunto de treino, métricas) nos logs de produção.
- Retreinamento: periodicidade semestral ou gatilhos por drift/perda de desempenho (monitorar F1-macro e Recall-macro).

Integração com Power BI
-----------------------
- O CSV final gerado pela rotina de produção alimenta diretamente o relatório no Power BI. O painel exibe: Visão Geral, Lista de Prioridade, Análises por Curso/Turma e Tendências.
- No painel, inclua versão do modelo e nota sobre uso de dados simulados de satisfação (quando aplicável).

Limitações e recomendações
-------------------------
- As variáveis de satisfação, nesta entrega, são simuladas: recomenda-se implementar coleta real e validação temporal.
- Priorizar análises de calibração (curva de confiabilidade, Brier Score) e estudos de ablação para quantificar contribuição de cada grupo de variáveis.
- Testar métricas de equidade por curso/turno e definir limiares operacionais por unidade.

Próximos passos sugeridos
------------------------
1. Implementar coleta real das seis variáveis de satisfação e reenquadrar análise de sensibilidade.
2. Automatizar rotinas de ingestão (upload via interface web) e atualização do Power BI (opções de atualização automática).
3. Definir plano de governança com responsáveis por cada etapa (dados, ML, pedagogia).

