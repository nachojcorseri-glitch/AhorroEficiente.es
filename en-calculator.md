---
layout: page
title: "Electricity Cost Calculator"
permalink: /en/calculator/
---

<p class="site-intro">Pick an appliance (or enter its wattage by hand), how many hours a day you use it, and your price per kWh. Everything is calculated instantly in your own browser — nothing is sent or stored anywhere.</p>

<div class="calc-card">
  <div class="calc-field">
    <label for="calc-aparato">Appliance</label>
    <select id="calc-aparato">
      <option value="150">Refrigerator (~150 W average)</option>
      <option value="800">Washing machine (~800 W)</option>
      <option value="1200">Dishwasher (~1200 W)</option>
      <option value="1000">Air conditioner (~1000 W)</option>
      <option value="2000">Electric oven (~2000 W)</option>
      <option value="1000">Microwave (~1000 W)</option>
      <option value="2500">Clothes dryer (~2500 W)</option>
      <option value="100">LED TV (~100 W)</option>
      <option value="200">Desktop computer (~200 W)</option>
      <option value="10">LED bulb (~10 W)</option>
      <option value="custom">Other (enter wattage)</option>
    </select>
  </div>

  <div class="calc-field" id="calc-custom-wrap" style="display:none;">
    <label for="calc-custom">Appliance wattage</label>
    <input type="number" id="calc-custom" min="0" value="1000">
  </div>

  <div class="calc-field">
    <label for="calc-horas">Hours used per day</label>
    <input type="number" id="calc-horas" min="0" step="0.25" value="2">
  </div>

  <div class="calc-field">
    <label for="calc-precio">Price per kWh you pay (your currency)</label>
    <input type="number" id="calc-precio" min="0" step="0.01" value="0.17">
    <p class="calc-hint">Match this to your actual bill — rates change over time and by plan.</p>
  </div>

  <div class="calc-result">
    <div><span>Per day</span><strong id="calc-dia">0.00</strong></div>
    <div><span>Per month</span><strong id="calc-mes">0.00</strong></div>
    <div><span>Per year</span><strong id="calc-anio">0.00</strong></div>
  </div>

  <p class="calc-hint">The wattages in the list are typical, approximate figures — your exact model may use more or less. Check the energy label or manual for the precise number.</p>
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

  function clamp(n) {
    n = parseFloat(n);
    if (isNaN(n) || n < 0) return 0;
    return n;
  }

  function fmt(n) {
    return n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function recalcular() {
    var vatios = sel.value === 'custom' ? clamp(customInput.value) : clamp(sel.value);
    var h = clamp(horas.value);
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
