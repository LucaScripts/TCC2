# Instalação Rápida - Sistema Híbrido Expandido

## 1. Instalar Dependências

```bash
pip3 install -r requirements_final.txt
```

## 2. Treinar o Modelo (Opcional)

Se você não tiver o modelo pré-treinado:

```bash
cd codigo
python3 treinar_modelo_final.py
```

Isso criará:
- `../modelos/modelo_xgboost_expandido.joblib`
- `../modelos/label_encoder_expandido.joblib`

## 3. Usar o Sistema

```bash
cd codigo
python3 sistema_predicao_evasao_final.py
```

Isso executará os exemplos e gerará:
- `predicoes_exemplo.csv` - Predições
- `sistema_evasao.log` - Log de execução

## 4. Próximos Passos

Consulte a documentação em `documentacao/GUIA_COMPLETO_USO_SISTEMA.md`

---

**Pronto para usar! 🚀**
