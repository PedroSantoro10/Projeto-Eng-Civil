const DEFAULT_MATERIAIS = {aterro:80.0, areia:60.0, brita:150.0};
const MEASURE_DECIMALS = 1;
const CURRENCY_DECIMALS = 2;

function fmtMedida(v, unit=''){return `${v.toFixed(MEASURE_DECIMALS)}${unit? ' ' + unit: ''}`}
function fmtMoeda(v){return `R$ ${v.toFixed(CURRENCY_DECIMALS)}`}

function parseDimensoes(s){s=s.trim().toLowerCase().replace(',', '.');
  let parts = s.includes('x') ? s.split('x').map(p=>p.trim()) : s.split(/\s+/);
  if(parts.length<2) throw new Error('Formato inválido');
  return [parseFloat(parts[0]), parseFloat(parts[1])];
}

// Terreno
document.getElementById('calcTerreno').addEventListener('click', ()=>{
  const w = parseFloat(document.getElementById('largura').value)||0;
  const h = parseFloat(document.getElementById('comprimento').value)||0;
  if(w<=0 || h<=0){document.getElementById('saidaTerreno').textContent='Informe largura e comprimento maiores que zero.';return}
  const area = w*h; const per = 2*(w+h);
  document.getElementById('saidaTerreno').textContent = `Área: ${fmtMedida(area,'m²')}\nPerímetro: ${fmtMedida(per,'m')}`;
});

document.getElementById('limparTerreno').addEventListener('click', ()=>{document.getElementById('largura').value='';document.getElementById('comprimento').value='';document.getElementById('saidaTerreno').textContent='';});

// Terraplenagem
document.getElementById('calcTerra').addEventListener('click', ()=>{
  const w = parseFloat(document.getElementById('largura').value)||0;
  const h = parseFloat(document.getElementById('comprimento').value)||0;
  if(w<=0 || h<=0){document.getElementById('saidaTerra').textContent='Informe primeiro as dimensões do terreno.';return}
  const profundidade = parseFloat(document.getElementById('profundidade').value)||0;
  if(profundidade<=0){document.getElementById('saidaTerra').textContent='Profundidade/altura deve ser maior que zero.';return}
  const area = w*h;
  const volume = area * profundidade;
  const material = document.getElementById('material').value;
  const custoMat = DEFAULT_MATERIAIS[material]||80;
  const custoMO = parseFloat(document.getElementById('custoMO').value)||0;
  const contingencia = parseFloat(document.getElementById('contingencia').value)||0;
  const custoMaterial = volume * custoMat;
  const custoMao = volume * custoMO;
  const subtotal = custoMaterial + custoMao;
  const total = subtotal * (1 + contingencia/100);
  document.getElementById('saidaTerra').textContent = `Volume estimado: ${fmtMedida(volume,'m³')}\nCusto material: ${fmtMoeda(custoMaterial)}\nCusto mão-de-obra: ${fmtMoeda(custoMao)}\nSubtotal: ${fmtMoeda(subtotal)}\nContingência: ${contingencia.toFixed(1)}%\nTotal estimado: ${fmtMoeda(total)}`;
});

document.getElementById('limparTerra').addEventListener('click', ()=>{document.getElementById('profundidade').value='';document.getElementById('custoMO').value='30';document.getElementById('contingencia').value='10';document.getElementById('saidaTerra').textContent='';});

// Cômodos
document.getElementById('calcComodos').addEventListener('click', ()=>{
  const raw = document.getElementById('comodosText').value.trim();
  if(!raw){document.getElementById('saidaComodos').textContent='Nenhum cômodo informado.';return}
  const lines = raw.split(/\r?\n/);
  let total = 0; let out = ['----- RELATÓRIO DE CÔMODOS -----'];
  for(const line of lines){if(!line.trim()) continue; const parts = line.trim().split(/\s+/); if(parts.length<2) continue; const nome = parts[0]; const dims = parts.slice(1).join(' ');
    try{const [w,c] = parseDimensoes(dims); if(w<=0||c<=0) continue; const area = w*c; total+=area; out.push(`${nome}: ${fmtMedida(w,'m')} x ${fmtMedida(c,'m')} -> Área: ${fmtMedida(area,'m²')}`);}catch(e){continue}}
  out.push(`Área total: ${fmtMedida(total,'m²')}`);
  document.getElementById('saidaComodos').textContent = out.join('\n');
});

document.getElementById('limparComodos').addEventListener('click', ()=>{document.getElementById('comodosText').value='';document.getElementById('saidaComodos').textContent='';});

// Export to PDF
document.getElementById('exportPdf').addEventListener('click', ()=>{
  try{
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    let y = 12;
    doc.setFontSize(14);
    doc.text('Relatório - Calculadora de Engenharia', 14, y);
    y += 8;

    const terrenoText = document.getElementById('saidaTerreno').textContent || 'Nenhum terreno calculado.';
    doc.setFontSize(11);
    doc.text('--- Terreno ---', 14, y); y+=6;
    terrenoText.split('\n').forEach(line=>{doc.text(line, 14, y); y+=6}); y+=4;

    const terraText = document.getElementById('saidaTerra').textContent || 'Nenhuma terraplenagem calculada.';
    doc.text('--- Terraplenagem ---', 14, y); y+=6;
    terraText.split('\n').forEach(line=>{doc.text(line, 14, y); y+=6}); y+=4;

    const comodosText = document.getElementById('saidaComodos').textContent || 'Nenhum cômodo informado.';
    doc.text('--- Cômodos ---', 14, y); y+=6;
    comodosText.split('\n').forEach(line=>{doc.text(line, 14, y); y+=6});

    doc.save('relatorio-adrine.pdf');
  }catch(e){
    alert('Falha ao gerar PDF: ' + e.message);
  }
});
