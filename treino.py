"""treino.py


projeto para planta Adrine

Funcionalidades:
- Entrada validada para dimensões do terreno
- Cálculo de área, perímetro
- Estimativa de volume de terraplenagem (com profundidade/altura)
- Estimativa de custos: material por m3/m2, mão de obra, contingência
- Presets de materiais (areia, brita, aterro) com custo por m3
- Modo demo automático e funções reutilizáveis para integração

Uso: executar como script; segue também funções para importar.
"""

from dataclasses import dataclass
from typing import Optional, Dict
import math

# formatação: casas decimais para medidas e moeda
MEASURE_DECIMALS = 1
CURRENCY_DECIMALS = 2


def fmt_medida(value: float, unit: str = '') -> str:
    return f"{value:.{MEASURE_DECIMALS}f}" + (f" {unit}" if unit else '')


def fmt_moeda(value: float) -> str:
    return f"R$ {value:.{CURRENCY_DECIMALS}f}"


def float_input(prompt: str, min_value: Optional[float] = None) -> float:
    while True:
        try:
            s = input(prompt).strip().replace(',', '.')
            v = float(s)
            if min_value is not None and v < min_value:
                print(f"Valor deve ser >= {min_value}. Tente novamente.")
                continue
            return v
        except ValueError:
            print("Entrada inválida. Digite um número (use '.' ou ',').")


@dataclass
class Terreno:
    largura: float
    comprimento: float

    def area(self) -> float:
        return self.largura * self.comprimento

    def perimetro(self) -> float:
        return 2 * (self.largura + self.comprimento)


@dataclass
class Terraplenagem:
    terreno: Terreno
    profundidade_media: float  # em metros (positiva)

    def volume_m3(self) -> float:
        # volume simples: área * profundidade média
        return self.terreno.area() * self.profundidade_media



@dataclass
class Comodo:
    nome: str
    largura: float
    comprimento: float

    def area(self) -> float:
        return self.largura * self.comprimento


def parse_dimensoes(s: str) -> tuple[float, float]:
    """Aceita '3x4', '3 X 4', '3,5x4.2' ou '3 4' e retorna (largura, comprimento)."""
    s = s.strip().lower().replace(',', '.')
    if 'x' in s:
        parts = [p.strip() for p in s.split('x') if p.strip()]
    else:
        parts = [p for p in s.split() if p]
    if len(parts) < 2:
        raise ValueError('Formato de dimensões inválido. Use LxC ou "L C".')
    largura = float(parts[0])
    comprimento = float(parts[1])
    return largura, comprimento


def coletar_comodos_interativo() -> list:
    print('\nInforme os cômodos um por linha no formato: nome larguraxcomprimento  (ex: quarto 3x4)')
    print("Digite 'fim' ou 'fim dos comodos' para encerrar, ou pressione Enter em linha vazia.")
    comodos = []
    while True:
        linha = input('Cômodo: ').strip()
        if not linha:
            break
        # permitir palavra-chave para encerrar explicitamente
        if linha.strip().lower() in ('fim', 'fim dos comodos', 'f', 'done', 'end'):
            print('Fim dos cômodos informado pelo usuário.')
            break
        # tenta separar nome e dimensões
        parts = linha.split()
        if len(parts) == 1:
            print('Formato inválido. Informe: nome dimensões (ex: quarto 3x4)')
            continue
        nome = parts[0]
        dims = ' '.join(parts[1:])
        try:
            largura, comprimento = parse_dimensoes(dims)
        except Exception as e:
            print('Erro ao interpretar dimensões:', e)
            continue
        if largura <= 0 or comprimento <= 0:
            print('Dimensões devem ser maiores que zero.')
            continue
        comodos.append(Comodo(nome=nome, largura=largura, comprimento=comprimento))
    return comodos


def relatorio_comodos(comodos: list) -> str:
    if not comodos:
        return 'Nenhum cômodo informado.'
    lines = ['----- RELATÓRIO DE CÔMODOS -----']
    total = 0.0
    for c in comodos:
        a = c.area()
        total += a
        lines.append(f"{c.nome}: {fmt_medida(c.largura, 'm')} x {fmt_medida(c.comprimento, 'm')} -> Área: {fmt_medida(a, 'm²')}")
    lines.append(f"Área total: {fmt_medida(total, 'm²')}")
    return '\n'.join(lines)


DEFAULT_MATERIAIS: Dict[str, float] = {
    # custo por m3 (R$)
    'aterro': 80.0,
    'brita': 150.0,
    'areia': 60.0,
}


# Presets de plantas (lista de tuples: (nome, largura, comprimento))
PRESET_PLANTAS = {
    'casa_pequena': [
        ('quarto', 3.0, 3.0),
        ('sala', 4.0, 3.0),
        ('cozinha', 3.0, 2.5),
        ('banheiro', 2.0, 1.5),
    ],
    'planta_exemplo': [
        ('quarto1', 3.5, 3.0),
        ('quarto2', 3.0, 2.8),
        ('sala', 4.0, 4.0),
        ('cozinha', 3.0, 3.0),
        ('banheiro', 2.0, 1.8),
    ],
}


def escolher_ou_criar_planta() -> list:
    """Oferece ao usuário opção de usar um preset ou criar planta do zero."""
    print('\nOpções para planta da casa:')
    print('  1) Criar planta do zero (entrar cômodos manualmente)')
    print('  2) Usar planta pronta (preset)')
    escolha = input('Escolha 1 ou 2 [1]: ').strip() or '1'
    if escolha == '2':
        print('\nPlantas disponíveis:')
        for k in PRESET_PLANTAS.keys():
            print(f" - {k}")
        sel = input('Digite o nome do preset desejado: ').strip()
        if sel in PRESET_PLANTAS:
            raw = PRESET_PLANTAS[sel]
            comodos = [Comodo(nome=n, largura=w, comprimento=c) for (n, w, c) in raw]
            return comodos
        else:
            print('Preset não encontrado. Voltando para criação do zero.')
    # default: criar do zero
    return coletar_comodos_interativo()


def estimar_custo_area(area_m2: float, custo_m2: float) -> float:
    return area_m2 * custo_m2


def estimar_custo_volume(volume_m3: float, custo_m3: float) -> float:
    return volume_m3 * custo_m3


def aplicar_contingencia(valor: float, porcentagem: float) -> float:
    return valor * (1 + porcentagem / 100.0)


def relatorio_terreno(terreno: Terreno, custo_m2: Optional[float] = None) -> str:
    area = terreno.area()
    perim = terreno.perimetro()
    lines = [
        "----- RELATÓRIO DO TERRENO -----",
        f"Largura: {fmt_medida(terreno.largura, 'm')}",
        f"Comprimento: {fmt_medida(terreno.comprimento, 'm')}",
        f"Área: {fmt_medida(area, 'm²')}",
        f"Perímetro: {fmt_medida(perim, 'm')}",
    ]
    if custo_m2 is not None:
        lines.append(f"Custo unitário (m²): {fmt_moeda(custo_m2)}")
        lines.append(
            f"Estimativa (sem contingência): {fmt_moeda(estimar_custo_area(area, custo_m2))}"
        )
    return "\n".join(lines)


def relatorio_terraplenagem(t: Terraplenagem, material: str, custo_material_m3: float, custo_mao_obra_por_m3: float, contingencia_pct: float) -> str:
    volume = t.volume_m3()
    custo_material = estimar_custo_volume(volume, custo_material_m3)
    custo_mao_obra = estimar_custo_volume(volume, custo_mao_obra_por_m3)
    subtotal = custo_material + custo_mao_obra
    total = aplicar_contingencia(subtotal, contingencia_pct)

    lines = [
        "----- RELATÓRIO DE TERRAPLENAGEM -----",
        f"Profundidade média: {fmt_medida(t.profundidade_media, 'm')}",
        f"Volume estimado: {fmt_medida(volume, 'm³')}",
        f"Material: {material} — {fmt_moeda(custo_material_m3)}/m³",
        f"Custo material: {fmt_moeda(custo_material)}",
        f"Custo mão-de-obra (R$/m³): {fmt_moeda(custo_mao_obra_por_m3)}",
        f"Custo mão-de-obra: {fmt_moeda(custo_mao_obra)}",
        f"Subtotal: {fmt_moeda(subtotal)}",
        f"Contingência: {contingencia_pct:.{MEASURE_DECIMALS}f}%",
        f"Total estimado: {fmt_moeda(total)}",
    ]
    return "\n".join(lines)


def demo_interativo():
    print("Estimador rápido para engenheiros civis — Terreno e Terraplenagem\n")
    largura = float_input("Largura do terreno (m): ", min_value=0.01)
    comprimento = float_input("Comprimento do terreno (m): ", min_value=0.01)
    terreno = Terreno(largura=largura, comprimento=comprimento)

    print('\n' + relatorio_terreno(terreno))

    # opção para planta da casa: criar do zero ou usar preset
    quer_planta = input('\nDeseja criar a planta da casa (com cômodos)? (s/n): ').strip().lower() in ('s', 'sim')
    comodos = []
    if quer_planta:
        comodos = escolher_ou_criar_planta()
        print('\n' + relatorio_comodos(comodos))

    quer_terraplenagem = input('\nDeseja estimar terraplenagem/aterro? (s/n): ').strip().lower() in ('s', 'sim')
    if quer_terraplenagem:
        profundidade = float_input('Profundidade média / altura de aterro (m, positivo): ', min_value=0.0)
        t = Terraplenagem(terreno=terreno, profundidade_media=profundidade)

        print('\nMateriais disponíveis:')
        for k, v in DEFAULT_MATERIAIS.items():
            print(f" - {k}: R$ {v:.2f}/m³")

        mat = input('Escolha material (nome) [default aterro]: ').strip().lower() or 'aterro'
        if mat not in DEFAULT_MATERIAIS:
            print('Material não encontrado. Usando preset "aterro".')
            mat = 'aterro'

        custo_mat = DEFAULT_MATERIAIS[mat]
        custo_mao_obra = float_input('Custo de mão-de-obra estimado por m³ (R$): ', min_value=0.0)
        contingencia = float_input('Percentual de contingência (%): ', min_value=0.0)

        print('\n' + relatorio_terraplenagem(t, mat, custo_mat, custo_mao_obra, contingencia))


def demo_automatico():
    # Teste rápido para verificar cálculo sem interação
    terreno = Terreno(largura=20.0, comprimento=30.0)
    t = Terraplenagem(terreno=terreno, profundidade_media=0.5)
    print(relatorio_terreno(terreno, custo_m2=120.0))
    print()
    print(relatorio_terraplenagem(t, 'areia', DEFAULT_MATERIAIS['areia'], custo_mao_obra_por_m3=30.0, contingencia_pct=10.0))


if __name__ == '__main__':
    print('treino.py — versão para engenheiros civis')
    modo = input('Executar modo demo automático (a) ou interativo (i)? [a/i]: ').strip().lower() or 'a'
    if modo == 'i':
        demo_interativo()
    else:
        demo_automatico()
