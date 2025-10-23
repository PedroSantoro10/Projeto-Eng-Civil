// interatividade para adicionar/editar cômodos e atualizar textarea para submissão
(function(){
  const addBtn = document.getElementById('addComodoBtn');
  const nome = document.getElementById('nomeComodo');
  const dims = document.getElementById('dimsComodo');
  const list = document.getElementById('comodosList');
  const comodosText = document.getElementById('comodosText');
  const areaTotalEl = document.getElementById('areaTotal');
  const resetBtn = document.getElementById('resetBtn');
  const doTerrap = document.getElementById('do_terraplenagem');
  const terrapOptions = document.getElementById('terrapOptions');

  let comodos = [];

  function parseDims(s){
    s = (s||'').trim().toLowerCase().replace(',', '.');
    let parts = s.includes('x') ? s.split('x') : s.split(/\s+/);
    if(parts.length<2) return null;
    const w = parseFloat(parts[0]);
    const h = parseFloat(parts[1]);
    if(isNaN(w) || isNaN(h)) return null;
    return [w,h];
  }

  function calculaAreaTotal(){
    return comodos.reduce((acc,c)=>acc + (c.w*c.h), 0);
  }

  function renderList(){
    list.innerHTML='';
    comodos.forEach((c,idx)=>{
      const el = document.createElement('div'); el.className='comodo-item';
      el.innerHTML = `<div><div class="comodo-name">${c.name}</div><div class="comodo-dims">${c.w} x ${c.h} m</div></div><div class="comodo-actions"><button data-idx="${idx}" class="remove">✕</button></div>`;
      list.appendChild(el);
    });
    areaTotalEl.innerText = calculaAreaTotal().toFixed(1) + ' m²';
    comodosText.value = comodos.map(c=>`${c.name} ${c.w}x${c.h}`).join('\n');
  }

  addBtn.addEventListener('click', ()=>{
    const n = nome.value.trim();
    const d = dims.value.trim();
    if(!n || !d) return alert('Informe nome e dimensões do cômodo.');
    const parsed = parseDims(d);
    if(!parsed) return alert('Dimensões inválidas. Use 3x4 ou 3 4');
    comodos.push({name:n, w:parsed[0], h:parsed[1]});
    nome.value=''; dims.value=''; nome.focus();
    renderList();
  });

  list.addEventListener('click', (ev)=>{
    if(ev.target.matches('button.remove')){
      const idx = parseInt(ev.target.dataset.idx,10);
      comodos.splice(idx,1);
      renderList();
    }
  });

  resetBtn.addEventListener('click', ()=>{
    if(!confirm('Limpar todos os campos?')) return;
    document.getElementById('mainForm').reset();
    comodos=[]; renderList();
  });

  doTerrap.addEventListener('change', ()=>{
    terrapOptions.style.display = doTerrap.checked ? 'block' : 'none';
  });

  // inicializa
  renderList();
})();
