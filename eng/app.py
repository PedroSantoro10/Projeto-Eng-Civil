from flask import Flask, render_template, request, redirect, url_for
from treino import Terreno, Comodo, parse_dimensoes, relatorio_terreno, relatorio_comodos, Terraplenagem, relatorio_terraplenagem, DEFAULT_MATERIAIS, fmt_moeda

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    materiais = DEFAULT_MATERIAIS
    return render_template('index.html', materiais=materiais)


@app.route('/report', methods=['POST'])
def report():
    # terreno
    largura = float(request.form.get('largura') or 0)
    comprimento = float(request.form.get('comprimento') or 0)
    terreno = Terreno(largura=largura, comprimento=comprimento)

    # cômodos: textarea com linhas "nome dims"
    raw_comodos = request.form.get('comodos_text', '')
    comodos = []
    for line in raw_comodos.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.lower() in ('fim', 'fim dos comodos', 'f', 'done', 'end'):
            break
        parts = line.split()
        if len(parts) < 2:
            # ignorar linha inválida
            continue
        nome = parts[0]
        dims = ' '.join(parts[1:])
        try:
            w, c = parse_dimensoes(dims)
        except Exception:
            continue
        comodos.append(Comodo(nome=nome, largura=w, comprimento=c))

    # terraplenagem (opcional)
    do_terra = request.form.get('do_terraplenagem') == 'on'
    terrap = None
    terrap_report = None
    if do_terra:
        profundidade = float(request.form.get('profundidade') or 0)
        terrap = Terraplenagem(terreno=terreno, profundidade_media=profundidade)
        material = request.form.get('material') or 'aterro'
        custo_mat = DEFAULT_MATERIAIS.get(material, 80.0)
        custo_mo = float(request.form.get('custo_mao_obra') or 0)
        contingencia = float(request.form.get('contingencia') or 0)
        terrap_report = relatorio_terraplenagem(terrap, material, custo_mat, custo_mo, contingencia)

    terreno_report = relatorio_terreno(terreno)
    comodos_report = relatorio_comodos(comodos)

    return render_template('report.html', terreno_report=terreno_report, comodos_report=comodos_report, terrap_report=terrap_report)


if __name__ == '__main__':
    app.run(debug=True)
