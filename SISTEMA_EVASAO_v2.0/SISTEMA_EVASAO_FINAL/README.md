# Sistema Híbrido Expandido de Predição de Evasão Estudantil

**Versão:** 2.0  
**Status:** Pronto para Produção  
**Autor:** Lucas Dias da Silva  
**Instituição:** IFBA  
**Data:** Outubro de 2025

## 🚀 Início Rápido (3 passos)

### 1. Instalar Dependências
```bash
pip3 install -r requirements_final.txt
```

### 2. Executar o Sistema
```bash
cd codigo
python3 sistema_predicao_evasao_final.py
```

### 3. Ver Resultados
```bash
# Resultados salvos em:
# - predicoes_exemplo.csv
# - sistema_evasao.log
```

## 📚 Documentação

- **INSTALACAO_RAPIDA.md** - Instalação em 3 passos
- **documentacao/GUIA_COMPLETO_USO_SISTEMA.md** - Guia detalhado
- **documentacao/ARTIGO_FINAL_ENRIQUECIDO.md** - Fundamentação teórica
- **documentacao/README_FINAL.md** - Documentação completa

## 📊 O que o Sistema Faz

Prediz risco de evasão estudantil combinando:
- ✅ Machine Learning (XGBoost) com 18 features
- ✅ Regras de Negócio Institucionais
- ✅ Dados de Satisfação Estudantil

**Resultado:** Detecta 172 casos de risco (18% dos alunos)

## 📁 Estrutura

```
codigo/              - Código Python
dados/               - Dados de entrada (CSV/Excel)
modelos/             - Modelos treinados (JOBLIB)
documentacao/        - Documentação completa
exemplos/            - Exemplos de uso
logs/                - Arquivos de log
```

## 🔧 Requisitos

- Python 3.8+
- pip3
- ~500MB de espaço em disco

## 📞 Suporte

Consulte a documentação em `documentacao/`

---

**Pronto para usar! 🚀**
