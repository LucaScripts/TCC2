# Guia de Integração: Dados Reais de Satisfação Estudantil

## Situação Atual

As 6 features de satisfação utilizadas pelo modelo são **atualmente simuladas** no dataset de treinamento (`Planilhabasedados_EXPANDIDO.csv`). Isso significa que os valores foram gerados artificialmente e não refletem respostas reais de alunos. Essa é uma limitação conhecida do sistema que impacta diretamente a qualidade das predições para esse subconjunto de features.

**Features afetadas:**

| Coluna | Descrição | Escala atual (simulada) |
|--------|-----------|------------------------|
| `Satisfacao_Geral` | Satisfação geral com o curso | 1 a 5 |
| `Qualidade_Ensino` | Avaliação da qualidade do ensino | 1 a 5 |
| `Motivacao_Continuar` | Motivação para continuar no curso | 1 a 5 |
| `Dificuldade_Aprendizado` | Nível de dificuldade de aprendizado | 1 a 5 |
| `Pretende_Desistir` | Intenção de desistir do curso | 0 (não) ou 1 (sim) |
| `Avaliacao_Professor` | Avaliação do desempenho dos professores | 1 a 5 |

---

## Como Integrar Dados Reais

### Passo 1 — Criar o instrumento de pesquisa

Elabore um questionário com as 6 perguntas correspondentes. Sugestão de formulação:

1. **Satisfacao_Geral**: *"De 1 a 5, como você avalia sua satisfação geral com o curso?"*
2. **Qualidade_Ensino**: *"De 1 a 5, como você avalia a qualidade do ensino recebido?"*
3. **Motivacao_Continuar**: *"De 1 a 5, qual o seu nível de motivação para continuar no curso?"*
4. **Dificuldade_Aprendizado**: *"De 1 a 5, qual o seu nível de dificuldade no aprendizado das disciplinas?"*
5. **Pretende_Desistir**: *"Você pretende desistir do curso? (0 = Não / 1 = Sim)"*
6. **Avaliacao_Professor**: *"De 1 a 5, como você avalia o desempenho dos seus professores?"*

Ferramentas sugeridas: Google Forms, Microsoft Forms, ou formulário interno do IFBA.

### Passo 2 — Exportar e formatar os dados coletados

O resultado da pesquisa deve ser exportado como CSV ou Excel com as colunas nomeadas **exatamente** como na tabela acima. Exemplo:

```
Matricula,Satisfacao_Geral,Qualidade_Ensino,Motivacao_Continuar,Dificuldade_Aprendizado,Pretende_Desistir,Avaliacao_Professor
20241001,4,3,5,2,0,4
20241002,2,2,1,4,1,2
```

### Passo 3 — Fazer o merge com os dados institucionais

O arquivo de entrada do sistema contém as 12 features quantitativas (vindas do AcadWeb/sistema institucional). As 6 features de satisfação devem ser unidas a esse arquivo pelo número de matrícula antes de executar as predições.

```python
import pandas as pd

# Dados institucionais (do AcadWeb ou exportação administrativa)
dados_institucionais = pd.read_excel('alunos_ativos_atual.xlsx', header=3)

# Dados da pesquisa de satisfação
dados_satisfacao = pd.read_csv('pesquisa_satisfacao.csv')

# Merge pela matrícula
dados_completos = dados_institucionais.merge(
    dados_satisfacao,
    on='Matricula',
    how='left'  # mantém alunos que não responderam (features serão 0)
)

# Salvar arquivo combinado para usar no sistema
dados_completos.to_csv('alunos_com_satisfacao.csv', index=False)
```

### Passo 4 — Executar o sistema normalmente

```bash
python codigo/sistema_predicao_evasao_final.py
```

O sistema já trata alunos sem dados de satisfação (features preenchidas com 0) através do método `_preprocessar_dados`. Um aviso será exibido no log caso as colunas de satisfação estejam ausentes.

---

## Retreinar o Modelo com Dados Reais

Após coletar dados reais de satisfação, é fundamental retreinar o modelo para que ele aprenda os padrões reais, em vez dos simulados.

1. Adicione as colunas de satisfação ao arquivo `dados/Planilhabasedados_EXPANDIDO.csv`
2. Execute o treinamento:

```bash
python codigo/treinar_modelo_final.py
```

3. O novo modelo (`modelo_xgboost_expandido.joblib`) substituirá o anterior automaticamente.

> **Expectativa**: com dados reais de satisfação, especialmente a feature `Pretende_Desistir`, espera-se uma melhora significativa no F1-Score atual (0,2216), pois essa feature tem alto poder preditivo direto sobre evasão.

---

## Periodicidade Recomendada

| Período | Ação |
|---------|------|
| Início de semestre | Aplicar pesquisa de satisfação a todos os alunos ativos |
| Mensalmente | Executar predições com dados atualizados |
| Ao final de cada ano letivo | Retreinar o modelo com novos dados rotulados |

---

## Referências

- Features definidas em: [`codigo/sistema_predicao_evasao_final.py`](../codigo/sistema_predicao_evasao_final.py) — constante `FEATURES_SATISFACAO`
- Documentação técnica completa: [`DOCUMENTACAO_SISTEMA_PRODUCAO.md`](DOCUMENTACAO_SISTEMA_PRODUCAO.md)
