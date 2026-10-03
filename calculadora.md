---
layout: page
title: "Calculadora de consumo eléctrico"
permalink: /calculadora/
---

<p class="site-intro">Elige un aparato (o pon los vatios a mano), cuántas horas lo usas al día, y el precio que pagas por kWh. El cálculo se hace al momento en tu propio navegador — no se envía ni se guarda nada.</p>

<div class="calc-card">
  <div class="calc-field">
    <label for="calc-aparato">Aparato</label>
    <select id="calc-aparato">
      <option value="150">Frigorífico (~150 W de media)</option>
      <option value="800">Lavadora (~800 W)</option>
      <option value="1200">Lavavajillas (~1200 W)</option>
      <option value="1000">Aire acondicionado (~1000 W)</option>
      <option value="2000">Horno eléctrico (~2000 W)</option>
      <option value="1000">Microondas (~1000 W)</option>
      <option value="2500">Secadora (~2500 W)</option>
      <option value="100">Televisor LED (~100 W)</option>
      <option value="200">Ordenador de sobremesa (~200 W)</option>
      <option value="10">Bombilla LED (~10 W)</option>
      <option value="custom">Otro (pongo los vatios)</option>
    </select>
  </div>

  <div class="calc-field" id="calc-custom-wrap" style="display:none;">
    <label for="calc-custom">Vatios del aparato</label>
    <input type="number" id="calc-custom" min="0" value="1000">
  </div>

  <div class="calc-field">
    <label for="calc-horas">Horas de uso al día</label>
    <input type="number" id="calc-horas" min="0" max="24" step="0.25" value="2">
  </div>

  <div class="calc-field">
    <label for="calc-precio">Precio por kWh que pagas (€)</label>
    <input type="number" id="calc-precio" min="0" step="0.01" value="0.17">
    <p class="calc-hint">Ajusta esto al precio real de tu factura actual — cambia con el tiempo y según la tarifa.</p>
  </div>

  <div class="calc-result">
    <div><span>Al día</span><strong id="calc-dia">0,00 €</strong></div>
    <div><span>Al mes</span><strong id="calc-mes">0,00 €</strong></div>
    <div><span>Al año</span><strong id="calc-anio">0,00 €</strong></div>
  </div>

  <p class="calc-hint">Los vatios de la lista son valores típicos orientativos: el consumo real de tu modelo concreto puede variar bastante. Para el dato exacto, mira la etiqueta energética o el manual del aparato.</p>
</div>

<script>
(function () {
  var sel = document.getElementById('calc-aparato');
  var customWrap = document.getElementById('calc-custom-wrap');
  var customInput = document.getElementById('calc-custom');
  var horas = document.getElementById('calc-horas');
  var precio = document.getElementById('calc-precio');
  var outDia = document.getElementById('calc-dia');
  var outMes = document.getElementById('calc-mes');
  var outAnio = document.getElementById('calc-anio');

  function clamp(n, max) {
    n = parseFloat(n);
    if (isNaN(n) || n < 0) return 0;
    if (typeof max === 'number' && n > max) return max;
    return n;
  }

  function fmt(n) {
    return n.toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €';
  }

  function recalcular() {
    var vatios = sel.value === 'custom' ? clamp(customInput.value) : clamp(sel.value);
    var h = clamp(horas.value, 24);
    var p = clamp(precio.value);

    var kwhDia = (vatios / 1000) * h;
    var costeDia = kwhDia * p;

    outDia.textContent = fmt(costeDia);
    outMes.textContent = fmt(costeDia * 30);
    outAnio.textContent = fmt(costeDia * 365);
  }

  sel.addEventListener('change', function () {
    customWrap.style.display = sel.value === 'custom' ? 'block' : 'none';
    recalcular();
  });
  customInput.addEventListener('input', recalcular);
  horas.addEventListener('input', recalcular);
  precio.addEventListener('input', recalcular);

  recalcular();
})();
</script>
