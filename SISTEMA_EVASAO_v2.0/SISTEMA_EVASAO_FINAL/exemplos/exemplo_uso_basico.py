#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exemplo de Uso Básico do Sistema Híbrido Expandido
"""

import sys
import os

# Adicionar caminho do código
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'codigo'))

from sistema_predicao_evasao_final import SistemaEvasaoHibridoExpandido

def main():
    print("\n" + "="*70)
    print("EXEMPLO DE USO BÁSICO - SISTEMA HÍBRIDO EXPANDIDO")
    print("="*70 + "\n")
    
    try:
        # 1. Inicializar sistema
        print("1. Inicializando sistema...")
        sistema = SistemaEvasaoHibridoExpandido()
        print("   ✓ Sistema inicializado\n")
        
        # 2. Carregar dados
        print("2. Carregando dados...")
        caminho_dados = os.path.join(os.path.dirname(__file__), '..', 'dados', 'alunos_ativos_atual_EXPANDIDO.csv')
        dados = sistema.carregar_dados(caminho_dados)
        print(f"   ✓ Dados carregados: {len(dados)} alunos\n")
        
        # 3. Fazer predições
        print("3. Fazendo predições...")
        predicoes = sistema.prever(dados)
        print(f"   ✓ Predições realizadas\n")
        
        # 4. Gerar relatório
        print("4. Gerando relatório...")
        relatorio = sistema.gerar_relatorio(predicoes)
        print(f"   ✓ Relatório gerado\n")
        
        # 5. Exibir resultados
        print("="*70)
        print("RESULTADOS")
        print("="*70)
        print(f"Total de alunos: {relatorio['total_alunos']}")
        print(f"Casos de risco: {relatorio['total_risco']} ({relatorio['percentual_risco']:.1f}%)")
        print(f"Confiança média: {relatorio['confianca_media']:.2f}")
        print(f"\nDistribuição de Predições:")
        for categoria, count in relatorio['distribuicao_predicoes'].items():
            percentual = (count / relatorio['total_alunos']) * 100
            print(f"  - {categoria}: {count} ({percentual:.1f}%)")
        
        # 6. Salvar resultados
        print(f"\n5. Salvando resultados...")
        sistema.salvar_resultados(predicoes, 'predicoes_exemplo.csv')
        print(f"   ✓ Resultados salvos em: predicoes_exemplo.csv\n")
        
        print("="*70)
        print("✓ EXEMPLO CONCLUÍDO COM SUCESSO!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"✗ Erro: {str(e)}\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
