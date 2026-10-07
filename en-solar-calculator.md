---
layout: page
title: "Solar Installation Cost Calculator"
permalink: /en/solar-calculator/
---

<p class="site-intro">A rough estimate of the system size you'd need and what it might cost, based on your usage. The ranges are wide on purpose — for a real quote, talk to local installers.</p>

<div class="calc-card">
  <div class="calc-field">
    <label for="solar-consumo">Average monthly usage (kWh) — check your bill</label>
    <input type="number" id="solar-consumo" min="0" step="10" value="900">
  </div>

  <div class="calc-field calc-checkbox">
    <label><input type="checkbox" id="solar-bateria"> I want battery storage</label>
  </div>

  <div class="calc-result calc-result-solar">
    <div><span>Rough system size</span><strong id="solar-kwp">0 kW</strong></div>
    <div><span>Estimated cost</span><strong id="solar-coste">$0</strong></div>
  </div>

  <p class="calc-hint">Estimate based on average US sun-hours and typical 2026 installed cost per kW — your state's sun exposure and local incentives change this a lot. If you check the battery box, the range already includes it. For a real number, get quotes from local installers.</p>
</div>

<script>
(function () {
  var PRODUCCION = 1400; // kWh per kW installed per year, rough US average
  var COSTE_MIN = 2500;  // $ per kW installed, before any incentives
  var COSTE_MAX = 3500;
  var BATERIA_MIN = 10000; // $ typical home battery, installed
  var BATERIA_MAX = 15000;

  var consumo = document.getElementById('solar-consumo');
  var bateria = document.getElementById('solar-bateria');
  var outKwp = document.getElementById('solar-kwp');
  var outCoste = document.getElementById('solar-coste');

  function clamp(n) {
    n = parseFloat(n);
    if (isNaN(n) || n < 0) return 0;
    return n;
  }

  function fmtUSD(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function recalcular() {
    var kwhMes = clamp(consumo.value);
    var kwhAnual = kwhMes * 12;
    var kw = kwhAnual / PRODUCCION;

    var costeMin = kw * COSTE_MIN;
    var costeMax = kw * COSTE_MAX;

    if (bateria.checked) {
      costeMin += BATERIA_MIN;
      costeMax += BATERIA_MAX;
    }

    outKwp.textContent = kw.toFixed(1) + ' kW';
    outCoste.textContent = fmtUSD(costeMin) + ' – ' + fmtUSD(costeMax);
  }

  consumo.addEventListener('input', recalcular);
  bateria.addEventListener('change', recalcular);

  recalcular();
})();
</script>
