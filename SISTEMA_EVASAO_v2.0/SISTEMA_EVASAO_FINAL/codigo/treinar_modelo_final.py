#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SCRIPT DE TREINAMENTO DO MODELO FINAL
Sistema Híbrido Expandido de Predição de Evasão Estudantil

Treina o modelo XGBoost com 18 features (12 quantitativas + 6 qualitativas)
e salva o modelo e encoder para uso em produção.

Uso:
    python3 treinar_modelo_final.py
"""

import os
import sys
import logging
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
from xgboost import XGBClassifier

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAÇÃO DE LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONSTANTES
# ============================================================================

FEATURES_QUANTITATIVAS = [
    'Pend_Financ', 'Faltas_Consecutivas', 'Pend_Acad', 'Semestre', 'Idade',
    'Sexo', 'Turno', 'Renda_Familiar', 'Distancia_Campus',
    'Tempo_Deslocamento', 'Dificuldade_Disciplina', 'Trabalha'
]

FEATURES_SATISFACAO = [
    'Satisfacao_Geral', 'Qualidade_Ensino', 'Motivacao_Continuar',
    'Dificuldade_Aprendizado', 'Pretende_Desistir', 'Avaliacao_Professor'
]

TODAS_FEATURES = FEATURES_QUANTITATIVAS + FEATURES_SATISFACAO

# ============================================================================
# FUNÇÕES DE TREINAMENTO
# ============================================================================

def carregar_dados(caminho_arquivo: str) -> pd.DataFrame:
    """Carrega dados de treinamento."""
    logger.info(f"Carregando dados de: {caminho_arquivo}")
    
    if caminho_arquivo.endswith('.csv'):
        dados = pd.read_csv(caminho_arquivo)
    else:
        dados = pd.read_excel(caminho_arquivo, header=3)
    
    dados.columns = dados.columns.str.strip()
    logger.info(f"Dados carregados: {len(dados)} registros, {len(dados.columns)} colunas")
    
    return dados

def preprocessar_dados(dados: pd.DataFrame) -> pd.DataFrame:
    """Preprocessa os dados."""
    logger.info("Preprocessando dados...")
    
    dados_prep = dados.copy()
    
    # Preencher valores faltantes
    for col in TODAS_FEATURES:
        if col in dados_prep.columns:
            if dados_prep[col].dtype in ['float64', 'int64']:
                dados_prep[col].fillna(dados_prep[col].median(), inplace=True)
            else:
                dados_prep[col].fillna(0, inplace=True)
    
    # Garantir que todas as features existem
    for col in TODAS_FEATURES:
        if col not in dados_prep.columns:
            dados_prep[col] = 0
    
    logger.info("Preprocessamento concluído")
    return dados_prep

def treinar_modelo(X_treino: np.ndarray, y_treino: np.ndarray) -> XGBClassifier:
    """Treina o modelo XGBoost."""
    logger.info("Treinando modelo XGBoost...")
    
    modelo = XGBClassifier(
        max_depth=6,
        learning_rate=0.1,
        n_estimators=100,
        objective='multi:softprob',
        num_class=len(np.unique(y_treino)),
        random_state=42,
        eval_metric='mlogloss',
        verbosity=0
    )
    
    modelo.fit(X_treino, y_treino)
    logger.info("Modelo treinado com sucesso")
    
    return modelo

def avaliar_modelo(modelo: XGBClassifier, X_teste: np.ndarray,
                   y_teste: np.ndarray, le: LabelEncoder) -> Dict:
    """Avalia o modelo."""
    logger.info("Avaliando modelo...")
    
    # Predições
    y_pred = modelo.predict(X_teste)
    
    # Métricas
    acuracia = accuracy_score(y_teste, y_pred)
    precisao = precision_score(y_teste, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_teste, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_teste, y_pred, average='weighted', zero_division=0)
    
    # Validação cruzada
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    f1_cv = cross_val_score(modelo, X_teste, y_teste, cv=cv, scoring='f1_weighted')
    
    metricas = {
        'acuracia': acuracia,
        'precisao': precisao,
        'recall': recall,
        'f1_score': f1,
        'f1_score_cv_media': f1_cv.mean(),
        'f1_score_cv_std': f1_cv.std()
    }
    
    logger.info(f"Acurácia: {acuracia:.4f}")
    logger.info(f"Precisão: {precisao:.4f}")
    logger.info(f"Recall: {recall:.4f}")
    logger.info(f"F1-Score: {f1:.4f}")
    logger.info(f"F1-Score CV (5-fold): {f1_cv.mean():.4f} ± {f1_cv.std():.4f}")
    
    return metricas

def salvar_modelo(modelo: XGBClassifier, le: LabelEncoder,
                  caminho_modelo: str = 'modelo_xgboost_expandido.joblib',
                  caminho_encoder: str = 'label_encoder_expandido.joblib') -> None:
    """Salva modelo e encoder."""
    logger.info("Salvando modelo e encoder...")
    
    # Salvar modelo
    joblib.dump(modelo, caminho_modelo)
    logger.info(f"Modelo salvo: {caminho_modelo}")
    
    # Salvar encoder
    encoder_dict = {
        'label_encoder': le,
        'classes': le.classes_,
        'data_treinamento': datetime.now().isoformat()
    }
    joblib.dump(encoder_dict, caminho_encoder)
    logger.info(f"Encoder salvo: {caminho_encoder}")

def gerar_relatorio(metricas: Dict, caminho_arquivo: str = 'relatorio_treinamento.txt') -> None:
    """Gera relatório de treinamento."""
    logger.info("Gerando relatório...")
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("RELATÓRIO DE TREINAMENTO DO MODELO\n")
        f.write("Sistema Híbrido Expandido de Predição de Evasão Estudantil\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("MÉTRICAS DE DESEMPENHO:\n")
        f.write("-"*70 + "\n")
        f.write(f"Acurácia:              {metricas['acuracia']:.4f}\n")
        f.write(f"Precisão:              {metricas['precisao']:.4f}\n")
        f.write(f"Recall:                {metricas['recall']:.4f}\n")
        f.write(f"F1-Score:              {metricas['f1_score']:.4f}\n")
        f.write(f"F1-Score CV (5-fold):  {metricas['f1_score_cv_media']:.4f} ± {metricas['f1_score_cv_std']:.4f}\n")
        
        f.write("\n" + "="*70 + "\n")
    
    logger.info(f"Relatório salvo: {caminho_arquivo}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Função principal."""
    print("\n" + "="*70)
    print("TREINAMENTO DO MODELO - SISTEMA HÍBRIDO EXPANDIDO")
    print("="*70 + "\n")
    
    try:
        # 1. Carregar dados
        logger.info("Etapa 1: Carregando dados...")
        dados = carregar_dados('Planilhabasedados_EXPANDIDO.csv')
        
        # 2. Preprocessar dados
        logger.info("Etapa 2: Preprocessando dados...")
        dados_prep = preprocessar_dados(dados)
        
        # 3. Preparar features e target
        logger.info("Etapa 3: Preparando features e target...")
        X = dados_prep[TODAS_FEATURES].values
        y = dados_prep['Situacao'].values if 'Situacao' in dados_prep.columns else dados_prep.iloc[:, -1].values
        
        # 4. Codificar labels
        logger.info("Etapa 4: Codificando labels...")
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        
        logger.info(f"Classes encontradas: {le.classes_}")
        logger.info(f"Distribuição de classes:")
        unique, counts = np.unique(y_encoded, return_counts=True)
        for cls, count in zip(le.classes_, counts):
            logger.info(f"  - {cls}: {count} ({count/len(y)*100:.1f}%)")
        
        # 5. Dividir dados
        logger.info("Etapa 5: Dividindo dados (70% treino, 30% teste)...")
        X_treino, X_teste, y_treino, y_teste = train_test_split(
            X, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
        )
        
        logger.info(f"Treino: {len(X_treino)} amostras")
        logger.info(f"Teste: {len(X_teste)} amostras")
        
        # 6. Normalizar dados
        logger.info("Etapa 6: Normalizando dados...")
        scaler = StandardScaler()
        X_treino_scaled = scaler.fit_transform(X_treino)
        X_teste_scaled = scaler.transform(X_teste)
        
        # 7. Treinar modelo
        logger.info("Etapa 7: Treinando modelo...")
        modelo = treinar_modelo(X_treino_scaled, y_treino)
        
        # 8. Avaliar modelo
        logger.info("Etapa 8: Avaliando modelo...")
        metricas = avaliar_modelo(modelo, X_teste_scaled, y_teste, le)
        
        # 9. Salvar modelo
        logger.info("Etapa 9: Salvando modelo...")
        salvar_modelo(modelo, le)
        
        # 10. Gerar relatório
        logger.info("Etapa 10: Gerando relatório...")
        gerar_relatorio(metricas)
        
        print("\n" + "="*70)
        print("✓ TREINAMENTO CONCLUÍDO COM SUCESSO!")
        print("="*70)
        print(f"\nArquivos gerados:")
        print(f"  - modelo_xgboost_expandido.joblib")
        print(f"  - label_encoder_expandido.joblib")
        print(f"  - relatorio_treinamento.txt")
        print("\nMétricas finais:")
        print(f"  - Acurácia: {metricas['acuracia']:.4f}")
        print(f"  - F1-Score: {metricas['f1_score']:.4f}")
        print(f"  - F1-Score CV: {metricas['f1_score_cv_media']:.4f}")
        print("="*70 + "\n")
        
    except Exception as e:
        logger.error(f"Erro durante treinamento: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
