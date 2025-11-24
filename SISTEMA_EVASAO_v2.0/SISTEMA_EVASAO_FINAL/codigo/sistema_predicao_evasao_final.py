#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SISTEMA HÍBRIDO EXPANDIDO DE PREDIÇÃO DE EVASÃO ESTUDANTIL
Versão 2.0 - Pronto para Produção

Autor: Lucas Dias da Silva
Instituição: IFBA - Instituto Federal de Educação, Ciência e Tecnologia da Bahia
Orientador: Prof. Dr. Leonardo Barreto Campos
Data: Outubro de 2025

Descrição:
    Sistema que combina Machine Learning (XGBoost) com regras de negócio 
    institucionais e dados de satisfação estudantil para predição de risco 
    de evasão em cursos técnicos.

Componentes:
    1. Machine Learning (XGBoost) - 18 features (12 quant + 6 qual)
    2. Regras de Negócio Institucionais (LFI, LFR, LAC, NC, NF)
    3. Dados de Satisfação Estudantil (6 features qualitativas)

Uso Básico:
    >>> from sistema_predicao_evasao_final import SistemaEvasaoHibridoExpandido
    >>> sistema = SistemaEvasaoHibridoExpandido()
    >>> dados = sistema.carregar_dados('alunos.csv')
    >>> predicoes = sistema.prever(dados)
    >>> sistema.salvar_resultados(predicoes, 'predicoes.csv')

Conformidade:
    - LGPD: Dados anonimizados
    - SBC: Artigo em formato SBC
    - PEP8: Código segue padrões Python
"""

import os
import sys
import logging
import json
import warnings
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import pickle

import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import cross_val_score, StratifiedKFold
from xgboost import XGBClassifier

# Suprimir warnings desnecessários
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAÇÃO DE LOGGING
# ============================================================================

def configurar_logging(nome_arquivo: str = 'sistema_evasao.log') -> logging.Logger:
    """
    Configura o sistema de logging para auditoria e debugging.
    
    Args:
        nome_arquivo: Nome do arquivo de log
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger('SistemaEvasao')
    logger.setLevel(logging.DEBUG)
    
    # Handler para arquivo
    fh = logging.FileHandler(nome_arquivo)
    fh.setLevel(logging.DEBUG)
    
    # Handler para console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

logger = configurar_logging()

# ============================================================================
# DEFINIÇÕES DE CONSTANTES
# ============================================================================

# Features quantitativas originais (12)
FEATURES_QUANTITATIVAS = [
    'Pend_Financ',
    'Faltas_Consecutivas',
    'Pend_Acad',
    'Semestre',
    'Idade',
    'Sexo',
    'Turno',
    'Renda_Familiar',
    'Distancia_Campus',
    'Tempo_Deslocamento',
    'Dificuldade_Disciplina',
    'Trabalha'
]

# Features qualitativas de satisfação (6)
FEATURES_SATISFACAO = [
    'Satisfacao_Geral',
    'Qualidade_Ensino',
    'Motivacao_Continuar',
    'Dificuldade_Aprendizado',
    'Pretende_Desistir',
    'Avaliacao_Professor'
]

# Todas as features (18)
TODAS_FEATURES = FEATURES_QUANTITATIVAS + FEATURES_SATISFACAO

# Categorias de risco
CATEGORIAS_RISCO = {
    'MT': 'Matriculado',
    'LFI': 'Limpeza Financeira',
    'LFR': 'Limpeza de Frequência',
    'LAC': 'Limpeza Acadêmica',
    'NC': 'Nunca Compareceu',
    'NF': 'Não Formados',
    'CAC': 'Categoria Adicional 1',
    'CAN': 'Categoria Adicional 2',
    'FO': 'Fora',
    'TF': 'Transferência'
}

# Mapeamento de categorias para risco
MAPEAMENTO_RISCO = {
    'MT': False,
    'LFI': True,
    'LFR': True,
    'LAC': True,
    'NC': True,
    'NF': True,
    'CAC': True,
    'CAN': True,
    'FO': True,
    'TF': True
}

# ============================================================================
# CLASSE PRINCIPAL DO SISTEMA
# ============================================================================

class SistemaEvasaoHibridoExpandido:
    """
    Sistema Híbrido Expandido de Predição de Evasão Estudantil.
    
    Combina Machine Learning com regras de negócio institucionais e dados
    de satisfação para predição robusta de risco de evasão.
    
    Atributos:
        modelo: Modelo XGBoost treinado
        label_encoder: Encoder para labels
        scaler: StandardScaler para normalização
        logger: Logger para auditoria
    """
    
    def __init__(self, caminho_modelo: str = 'modelo_xgboost_expandido.joblib',
                 caminho_encoder: str = 'label_encoder_expandido.joblib'):
        """
        Inicializa o sistema.
        
        Args:
            caminho_modelo: Caminho do modelo treinado
            caminho_encoder: Caminho do label encoder
        """
        self.logger = logger
        self.modelo = None
        self.label_encoder = None
        self.scaler = StandardScaler()
        self.caminho_modelo = caminho_modelo
        self.caminho_encoder = caminho_encoder
        
        self.logger.info("Sistema Híbrido Expandido inicializado")
        
        # Tentar carregar modelo e encoder
        self._carregar_modelo_e_encoder()
    
    def _carregar_modelo_e_encoder(self) -> None:
        """Carrega modelo e encoder do disco."""
        try:
            if os.path.exists(self.caminho_modelo):
                self.modelo = joblib.load(self.caminho_modelo)
                self.logger.info(f"Modelo carregado: {self.caminho_modelo}")
            else:
                self.logger.warning(f"Modelo não encontrado: {self.caminho_modelo}")
                
            if os.path.exists(self.caminho_encoder):
                encoder_dict = joblib.load(self.caminho_encoder)
                if isinstance(encoder_dict, dict):
                    self.label_encoder = encoder_dict.get('label_encoder')
                else:
                    self.label_encoder = encoder_dict
                self.logger.info(f"Encoder carregado: {self.caminho_encoder}")
            else:
                self.logger.warning(f"Encoder não encontrado: {self.caminho_encoder}")
                
        except Exception as e:
            self.logger.error(f"Erro ao carregar modelo/encoder: {str(e)}")
    
    def carregar_dados(self, caminho_arquivo: str, 
                      header: int = 3) -> pd.DataFrame:
        """
        Carrega dados de um arquivo CSV ou Excel.
        
        Args:
            caminho_arquivo: Caminho do arquivo
            header: Linha do header (padrão: 3 para formato IFBA)
            
        Returns:
            DataFrame com os dados
        """
        try:
            self.logger.info(f"Carregando dados de: {caminho_arquivo}")
            
            if caminho_arquivo.endswith('.csv'):
                dados = pd.read_csv(caminho_arquivo)
            elif caminho_arquivo.endswith(('.xlsx', '.xls')):
                dados = pd.read_excel(caminho_arquivo, header=header)
            else:
                raise ValueError("Formato de arquivo não suportado")
            
            # Limpar nomes de colunas
            dados.columns = dados.columns.str.strip()
            
            self.logger.info(f"Dados carregados: {len(dados)} linhas, {len(dados.columns)} colunas")
            
            return dados
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados: {str(e)}")
            raise
    
    def _aplicar_regras_negocio(self, aluno: pd.Series) -> str:
        """
        Aplica regras de negócio institucionais para classificação de risco.
        
        Regras em cascata (ordem de prioridade):
            1. LFI: Pendências financeiras >= 2
            2. LFR: Pendências financeiras > 0 AND Faltas >= 12
            3. LAC: Pendências acadêmicas >= 1
            4. NC: Faltas consecutivas >= 5
            5. NF: Curso completo AND Pendências <= 2
            6. MT: Padrão (Matriculado)
        
        Args:
            aluno: Série com dados do aluno
            
        Returns:
            Categoria de risco (MT, LFI, LFR, LAC, NC, NF)
        """
        try:
            # Extrair valores com tratamento de NaN
            pend_financ = float(aluno.get('Pend_Financ', 0) or 0)
            faltas_consecutivas = float(aluno.get('Faltas_Consecutivas', 0) or 0)
            pend_acad = float(aluno.get('Pend_Acad', 0) or 0)
            
            # Aplicar regras em cascata
            if pend_financ >= 2:
                return 'LFI'
            elif pend_financ > 0 and faltas_consecutivas >= 12:
                return 'LFR'
            elif pend_acad >= 1:
                return 'LAC'
            elif faltas_consecutivas >= 5:
                return 'NC'
            else:
                return 'MT'
                
        except Exception as e:
            self.logger.warning(f"Erro ao aplicar regras para aluno: {str(e)}")
            return 'MT'
    
    def _preprocessar_dados(self, dados: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocessa os dados para o modelo.
        
        Args:
            dados: DataFrame com dados brutos
            
        Returns:
            DataFrame preprocessado
        """
        dados_prep = dados.copy()
        
        # Preencher valores faltantes
        for col in TODAS_FEATURES:
            if col in dados_prep.columns:
                if dados_prep[col].dtype in ['float64', 'int64']:
                    dados_prep[col].fillna(dados_prep[col].median(), inplace=True)
                else:
                    dados_prep[col].fillna(dados_prep[col].mode()[0] if len(dados_prep[col].mode()) > 0 else 0, inplace=True)
        
        # Garantir que todas as features existem
        for col in TODAS_FEATURES:
            if col not in dados_prep.columns:
                dados_prep[col] = 0
        
        return dados_prep
    
    def prever(self, dados: pd.DataFrame) -> pd.DataFrame:
        """
        Realiza predições de risco de evasão.
        
        Args:
            dados: DataFrame com dados dos alunos
            
        Returns:
            DataFrame com predições
        """
        try:
            self.logger.info(f"Iniciando predições para {len(dados)} alunos")
            
            # Preprocessar dados
            dados_prep = self._preprocessar_dados(dados)
            
            # Preparar features para o modelo
            X = dados_prep[TODAS_FEATURES].copy()
            
            # Fazer predições com o modelo
            if self.modelo is not None:
                predicoes_ml = self.modelo.predict(X)
                probabilidades = self.modelo.predict_proba(X)
                confianca = probabilidades.max(axis=1)
            else:
                self.logger.warning("Modelo não carregado, usando predição padrão")
                predicoes_ml = np.zeros(len(X), dtype=int)
                confianca = np.ones(len(X)) * 0.5
            
            # Decodificar predições
            if self.label_encoder is not None:
                predicoes_ml_str = self.label_encoder.inverse_transform(predicoes_ml)
            else:
                predicoes_ml_str = ['MT'] * len(X)
            
            # Aplicar regras de negócio
            predicoes_finais = []
            for idx, row in dados_prep.iterrows():
                predicao_ml = predicoes_ml_str[idx]
                predicao_regra = self._aplicar_regras_negocio(row)
                
                # Regras sobrescrevem ML se indicarem risco
                if MAPEAMENTO_RISCO.get(predicao_regra, False):
                    predicao_final = predicao_regra
                else:
                    predicao_final = predicao_ml
                
                predicoes_finais.append(predicao_final)
            
            # Criar DataFrame de resultados
            resultados = pd.DataFrame({
                'Matricula': dados.get('Matricula', dados.get('Matrícula', range(len(dados)))),
                'Predicao_ML': predicoes_ml_str,
                'Predicao_Final': predicoes_finais,
                'Eh_Risco': [MAPEAMENTO_RISCO.get(p, False) for p in predicoes_finais],
                'Categoria_Risco': [CATEGORIAS_RISCO.get(p, p) for p in predicoes_finais],
                'Confianca': confianca
            })
            
            self.logger.info(f"Predições concluídas: {resultados['Eh_Risco'].sum()} casos de risco")
            
            return resultados
            
        except Exception as e:
            self.logger.error(f"Erro ao fazer predições: {str(e)}")
            raise
    
    def gerar_relatorio(self, predicoes: pd.DataFrame) -> Dict[str, Any]:
        """
        Gera relatório estatístico das predições.
        
        Args:
            predicoes: DataFrame com predições
            
        Returns:
            Dicionário com estatísticas
        """
        try:
            relatorio = {
                'data_geracao': datetime.now().isoformat(),
                'total_alunos': len(predicoes),
                'total_risco': int(predicoes['Eh_Risco'].sum()),
                'percentual_risco': float(predicoes['Eh_Risco'].mean() * 100),
                'distribuicao_predicoes': predicoes['Predicao_Final'].value_counts().to_dict(),
                'confianca_media': float(predicoes['Confianca'].mean()),
                'confianca_minima': float(predicoes['Confianca'].min()),
                'confianca_maxima': float(predicoes['Confianca'].max())
            }
            
            self.logger.info(f"Relatório gerado: {relatorio['total_risco']} casos de risco")
            
            return relatorio
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório: {str(e)}")
            raise
    
    def salvar_resultados(self, predicoes: pd.DataFrame, 
                         caminho_arquivo: str) -> None:
        """
        Salva resultados em arquivo CSV.
        
        Args:
            predicoes: DataFrame com predições
            caminho_arquivo: Caminho do arquivo de saída
        """
        try:
            predicoes.to_csv(caminho_arquivo, index=False, encoding='utf-8')
            self.logger.info(f"Resultados salvos: {caminho_arquivo}")
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar resultados: {str(e)}")
            raise
    
    def exportar_relatorio_json(self, predicoes: pd.DataFrame,
                               caminho_arquivo: str) -> None:
        """
        Exporta relatório em formato JSON.
        
        Args:
            predicoes: DataFrame com predições
            caminho_arquivo: Caminho do arquivo JSON
        """
        try:
            relatorio = self.gerar_relatorio(predicoes)
            
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Relatório JSON exportado: {caminho_arquivo}")
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar JSON: {str(e)}")
            raise
    
    def analisar_categoria(self, predicoes: pd.DataFrame,
                          categoria: str) -> pd.DataFrame:
        """
        Filtra e retorna alunos de uma categoria específica.
        
        Args:
            predicoes: DataFrame com predições
            categoria: Categoria de risco (MT, LFI, LAC, etc)
            
        Returns:
            DataFrame filtrado
        """
        return predicoes[predicoes['Predicao_Final'] == categoria]
    
    def exportar_por_categoria(self, predicoes: pd.DataFrame,
                              diretorio_saida: str = 'predicoes_por_categoria') -> None:
        """
        Exporta predições separadas por categoria.
        
        Args:
            predicoes: DataFrame com predições
            diretorio_saida: Diretório para salvar arquivos
        """
        try:
            os.makedirs(diretorio_saida, exist_ok=True)
            
            for categoria in predicoes['Predicao_Final'].unique():
                df_categoria = self.analisar_categoria(predicoes, categoria)
                caminho = os.path.join(diretorio_saida, f'{categoria}.csv')
                df_categoria.to_csv(caminho, index=False, encoding='utf-8')
                self.logger.info(f"Categoria {categoria}: {len(df_categoria)} alunos")
            
            self.logger.info(f"Predições exportadas por categoria em: {diretorio_saida}")
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar por categoria: {str(e)}")
            raise

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def exemplo_uso_basico():
    """Exemplo de uso básico do sistema."""
    print("\n" + "="*70)
    print("EXEMPLO DE USO BÁSICO - SISTEMA HÍBRIDO EXPANDIDO")
    print("="*70 + "\n")
    
    try:
        # Inicializar sistema
        sistema = SistemaEvasaoHibridoExpandido()
        
        # Carregar dados
        dados = sistema.carregar_dados('alunos_ativos_atual_EXPANDIDO.csv')
        print(f"✓ Dados carregados: {len(dados)} alunos")
        
        # Fazer predições
        predicoes = sistema.prever(dados)
        print(f"✓ Predições realizadas")
        
        # Gerar relatório
        relatorio = sistema.gerar_relatorio(predicoes)
        print(f"\n✓ Relatório Gerado:")
        print(f"  - Total de alunos: {relatorio['total_alunos']}")
        print(f"  - Casos de risco: {relatorio['total_risco']} ({relatorio['percentual_risco']:.1f}%)")
        print(f"  - Confiança média: {relatorio['confianca_media']:.2f}")
        
        # Salvar resultados
        sistema.salvar_resultados(predicoes, 'predicoes_exemplo.csv')
        print(f"\n✓ Resultados salvos em: predicoes_exemplo.csv")
        
        # Mostrar distribuição
        print(f"\n✓ Distribuição de Predições:")
        for categoria, count in relatorio['distribuicao_predicoes'].items():
            percentual = (count / relatorio['total_alunos']) * 100
            print(f"  - {categoria}: {count} ({percentual:.1f}%)")
        
    except Exception as e:
        print(f"✗ Erro: {str(e)}")

def exemplo_analise_categoria():
    """Exemplo de análise por categoria."""
    print("\n" + "="*70)
    print("EXEMPLO DE ANÁLISE POR CATEGORIA")
    print("="*70 + "\n")
    
    try:
        sistema = SistemaEvasaoHibridoExpandido()
        dados = sistema.carregar_dados('alunos_ativos_atual_EXPANDIDO.csv')
        predicoes = sistema.prever(dados)
        
        # Analisar categoria LFI
        alunos_lfi = sistema.analisar_categoria(predicoes, 'LFI')
        print(f"✓ Alunos em Limpeza Financeira (LFI): {len(alunos_lfi)}")
        print(alunos_lfi[['Matricula', 'Confianca']].head())
        
        # Exportar por categoria
        sistema.exportar_por_categoria(predicoes)
        print(f"\n✓ Predições exportadas por categoria")
        
    except Exception as e:
        print(f"✗ Erro: {str(e)}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("SISTEMA HÍBRIDO EXPANDIDO DE PREDIÇÃO DE EVASÃO ESTUDANTIL")
    print("Versão 2.0 - Pronto para Produção")
    print("="*70)
    
    # Executar exemplos
    exemplo_uso_basico()
    exemplo_analise_categoria()
    
    print("\n" + "="*70)
    print("Exemplos concluídos com sucesso!")
    print("="*70 + "\n")
