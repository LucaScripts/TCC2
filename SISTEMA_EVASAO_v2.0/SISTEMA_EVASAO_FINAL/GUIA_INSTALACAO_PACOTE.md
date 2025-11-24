# 📦 Guia de Instalação e Uso do Pacote Completo

**Sistema Híbrido Expandido de Predição de Evasão Estudantil**  
**Versão:** 2.0  
**Data:** Outubro de 2025

---

## 🚀 Início Rápido (5 minutos)

### 1️⃣ Descompactar o Arquivo

**Windows:**
```
Clique com botão direito em SISTEMA_EVASAO_FINAL.zip
Selecione "Extrair Tudo..."
```

**Linux/Mac:**
```bash
unzip SISTEMA_EVASAO_FINAL.zip
# ou
tar -xzf SISTEMA_EVASAO_FINAL.tar.gz
```

### 2️⃣ Instalar Dependências

```bash
cd SISTEMA_EVASAO_FINAL
pip3 install -r requirements_final.txt
```

### 3️⃣ Executar o Sistema

```bash
cd codigo
python3 sistema_predicao_evasao_final.py
```

### 4️⃣ Ver Resultados

```bash
# Abrir arquivo gerado
cat predicoes_exemplo.csv
```

---

## 📁 Estrutura do Pacote

```
SISTEMA_EVASAO_FINAL/
│
├── 📄 README.md                          # Leia primeiro!
├── 📄 INSTALACAO_RAPIDA.md              # Instalação em 3 passos
├── 📄 ESTRUTURA.txt                      # Estrutura do projeto
├── 📄 VERSAO.txt                         # Informações de versão
├── 📄 config.ini                         # Configurações
├── 📄 requirements_final.txt              # Dependências Python
│
├── 📁 codigo/                            # Código Python
│   ├── sistema_predicao_evasao_final.py  # Sistema principal ⭐
│   └── treinar_modelo_final.py           # Script de treinamento
│
├── 📁 dados/                             # Dados de entrada
│   ├── Planilhabasedados_EXPANDIDO.csv   # Dados treino (expandido)
│   ├── alunos_ativos_atual_EXPANDIDO.csv # Dados predição (expandido)
│   ├── Planilhabasedados.xlsx            # Dados treino (original)
│   └── alunos_ativos_atual.xlsx          # Dados predição (original)
│
├── 📁 modelos/                           # Modelos treinados
│   ├── modelo_xgboost_expandido.joblib   # Modelo XGBoost ⭐
│   └── label_encoder_expandido.joblib    # Encoder de labels
│
├── 📁 documentacao/                      # Documentação completa
│   ├── ARTIGO_FINAL_ENRIQUECIDO.md       # Artigo acadêmico (25-30 pgs)
│   ├── RESUMO_EXECUTIVO_TCC2.md          # Resumo executivo
│   ├── GUIA_COMPLETO_USO_SISTEMA.md      # Guia detalhado
│   ├── DOCUMENTACAO_SISTEMA_PRODUCAO.md  # Documentação técnica
│   ├── GUIA_RAPIDO_PRODUCAO.md           # Guia rápido (5 min)
│   ├── CHECKLIST_DEFESA_TCC2.md          # Checklist defesa
│   └── README_FINAL.md                   # README detalhado
│
├── 📁 exemplos/                          # Exemplos de uso
│   └── exemplo_uso_basico.py             # Exemplo funcional
│
└── 📁 logs/                              # Arquivos de log
    └── (gerados automaticamente)
```

---

## 💻 Requisitos do Sistema

### Mínimo
- **Python:** 3.8 ou superior
- **Espaço:** 500 MB
- **RAM:** 2 GB
- **Processador:** Qualquer

### Recomendado
- **Python:** 3.10+
- **Espaço:** 1 GB
- **RAM:** 4 GB
- **Processador:** Multi-core

---

## 📋 Passo a Passo Detalhado

### Passo 1: Descompactar

**Windows (PowerShell):**
```powershell
Expand-Archive -Path SISTEMA_EVASAO_FINAL.zip -DestinationPath .
cd SISTEMA_EVASAO_FINAL
```

**Linux/Mac:**
```bash
unzip SISTEMA_EVASAO_FINAL.zip
cd SISTEMA_EVASAO_FINAL
```

### Passo 2: Verificar Python

```bash
python3 --version
# Deve retornar: Python 3.8.0 ou superior
```

### Passo 3: Criar Ambiente Virtual (Recomendado)

```bash
# Criar ambiente
python3 -m venv venv

# Ativar ambiente
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Passo 4: Instalar Dependências

```bash
pip3 install --upgrade pip
pip3 install -r requirements_final.txt
```

### Passo 5: Verificar Instalação

```bash
python3 -c "import pandas, xgboost, sklearn; print('✓ Dependências OK')"
```

### Passo 6: Executar o Sistema

```bash
cd codigo
python3 sistema_predicao_evasao_final.py
```

### Passo 7: Ver Resultados

```bash
# Resultados gerados:
# - predicoes_exemplo.csv
# - sistema_evasao.log

cat predicoes_exemplo.csv
```

---

## 🎯 Casos de Uso

### Caso 1: Usar Modelo Pré-treinado

```python
from sistema_predicao_evasao_final import SistemaEvasaoHibridoExpandido

sistema = SistemaEvasaoHibridoExpandido()
dados = sistema.carregar_dados('dados/alunos_ativos_atual_EXPANDIDO.csv')
predicoes = sistema.prever(dados)
sistema.salvar_resultados(predicoes, 'predicoes.csv')
```

### Caso 2: Treinar Novo Modelo

```bash
cd codigo
python3 treinar_modelo_final.py
```

Isso criará:
- `../modelos/modelo_xgboost_expandido.joblib`
- `../modelos/label_encoder_expandido.joblib`
- `relatorio_treinamento.txt`

### Caso 3: Analisar por Categoria

```python
sistema = SistemaEvasaoHibridoExpandido()
dados = sistema.carregar_dados('dados/alunos_ativos_atual_EXPANDIDO.csv')
predicoes = sistema.prever(dados)

# Filtrar alunos em risco específico
alunos_lfi = sistema.analisar_categoria(predicoes, 'LFI')
alunos_lac = sistema.analisar_categoria(predicoes, 'LAC')

# Exportar por categoria
sistema.exportar_por_categoria(predicoes, 'predicoes_por_categoria')
```

---

## 🔧 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'xgboost'"

**Solução:**
```bash
pip3 install -r requirements_final.txt
```

### Erro: "FileNotFoundError: modelo_xgboost_expandido.joblib"

**Solução:**
```bash
cd codigo
python3 treinar_modelo_final.py
```

### Erro: "No such file or directory: 'dados/alunos_ativos_atual_EXPANDIDO.csv'"

**Solução:**
```bash
# Verificar se está no diretório correto
pwd
# Deve estar em: SISTEMA_EVASAO_FINAL/

# Verificar se arquivo existe
ls dados/
```

### Erro de Encoding (UnicodeDecodeError)

**Solução:**
```python
# No código, especificar encoding
dados = pd.read_csv('arquivo.csv', encoding='latin-1')
```

### Erro de Memória (MemoryError)

**Solução:**
```bash
# Aumentar memória disponível ou processar dados em chunks
# Consulte: documentacao/GUIA_COMPLETO_USO_SISTEMA.md
```

---

## 📊 Validação da Instalação

Execute este script para validar:

```bash
cd codigo
python3 -c "
from sistema_predicao_evasao_final import SistemaEvasaoHibridoExpandido
import os

sistema = SistemaEvasaoHibridoExpandido()

# Verificar arquivos
print('Verificando arquivos...')
assert os.path.exists('../modelos/modelo_xgboost_expandido.joblib'), 'Modelo não encontrado'
assert os.path.exists('../modelos/label_encoder_expandido.joblib'), 'Encoder não encontrado'
print('✓ Modelos OK')

# Verificar dados
assert os.path.exists('../dados/alunos_ativos_atual_EXPANDIDO.csv'), 'Dados não encontrados'
print('✓ Dados OK')

# Testar carregamento
dados = sistema.carregar_dados('../dados/alunos_ativos_atual_EXPANDIDO.csv')
print(f'✓ Dados carregados: {len(dados)} registros')

# Testar predição
predicoes = sistema.prever(dados)
print(f'✓ Predições OK: {len(predicoes)} resultados')

print('\n✅ INSTALAÇÃO VALIDADA COM SUCESSO!')
"
```

---

## 🚀 Próximos Passos

1. ✅ Leia `README.md` para visão geral
2. ✅ Execute `exemplo_uso_basico.py` para ver funcionando
3. ✅ Consulte `documentacao/GUIA_COMPLETO_USO_SISTEMA.md` para uso avançado
4. ✅ Leia `documentacao/ARTIGO_FINAL_ENRIQUECIDO.md` para fundamentação teórica
5. ✅ Use `CHECKLIST_DEFESA_TCC2.md` para preparar sua defesa

---

## 📞 Suporte

### Documentação
- `README.md` - Visão geral
- `INSTALACAO_RAPIDA.md` - Instalação rápida
- `documentacao/GUIA_COMPLETO_USO_SISTEMA.md` - Guia detalhado
- `documentacao/ARTIGO_FINAL_ENRIQUECIDO.md` - Fundamentação teórica

### Código
- Todos os arquivos Python têm comentários explicativos
- Docstrings em todas as funções
- Exemplos de uso inclusos

### Logs
- Verificar `logs/sistema_evasao.log` para detalhes de erros
- Logs são criados automaticamente

---

## ✅ Checklist de Instalação

- [ ] Descompactou o arquivo
- [ ] Instalou Python 3.8+
- [ ] Instalou dependências (`pip3 install -r requirements_final.txt`)
- [ ] Verificou que modelo existe em `modelos/`
- [ ] Executou `python3 sistema_predicao_evasao_final.py`
- [ ] Viu arquivo `predicoes_exemplo.csv` gerado
- [ ] Leu `README.md`
- [ ] Consultou documentação conforme necessário

---

## 🎓 Pronto para Usar!

Seu sistema está 100% pronto para:
- ✅ Executar predições
- ✅ Analisar dados
- ✅ Gerar relatórios
- ✅ Integrar com AcadWeb
- ✅ Agendar execução automática

**Boa sorte com seu TCC2! 🚀**

---

**Versão:** 2.0  
**Data:** Outubro de 2025  
**Status:** ✅ Pronto para Produção
