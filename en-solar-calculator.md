---
layout: page
title: "Solar Installation Cost Calculator"
permalink: /en/solar-calculator/
---

<p class="site-intro">Estimate the system size you'd need, what it might cost with or without a battery, how much you'd save per year, and how long it would take to pay off. The ranges are wide on purpose — for a real quote, talk to local installers.</p>

<div class="calc-card calc-card-wide">
  <div class="calc-field">
    <label for="solar-consumo">Average monthly usage (kWh) — check your bill or <a href="/en/calculator/">work it out from your appliances</a></label>
    <input type="number" id="solar-consumo" min="0" step="10" value="900">
  </div>

  <div class="calc-field">
    <label for="solar-precio">Price per kWh you pay ($)</label>
    <input type="number" id="solar-precio" min="0" step="0.01" value="0.17">
  </div>

  <div class="calc-field">
    <label for="solar-bateria">Battery storage</label>
    <select id="solar-bateria">
      <option value="0">No battery</option>
      <option value="5">5 kWh</option>
      <option value="10">10 kWh</option>
      <option value="15">15 kWh</option>
      <option value="20">20 kWh</option>
    </select>
  </div>

  <div class="calc-result calc-result-4">
    <div><span>Rough system size</span><strong id="solar-kwp">0 kW</strong></div>
    <div><span>Estimated cost</span><strong id="solar-coste">$0</strong></div>
    <div><span>Savings per year</span><strong id="solar-ahorro">$0</strong></div>
    <div><span>Payback</span><strong id="solar-pay">—</strong></div>
  </div>

  <p class="calc-hint" id="solar-desglose"></p>
  <p class="calc-hint">Assumptions: system sized to cover your yearly usage; without a battery about 40% of what's produced is used at home, rising with a battery (55% at 5 kWh, 70% at 10, 80% at 15, 85% at 20). Prices are typical 2026 US figures before incentives; your state's sunshine, incentives and net-metering rules change the result a lot.</p>
</div>

<script>
(function () {
  var PRODUCCION = 1400, PANEL_MIN = 2500, PANEL_MAX = 3500, BAT_MIN = 800, BAT_MAX = 1300;
  var AUTOCONSUMO = { 0: 0.40, 5: 0.55, 10: 0.70, 15: 0.80, 20: 0.85 };

  var consumo = document.getElementById('solar-consumo');
  var precio = document.getElementById('solar-precio');
  var bateria = document.getElementById('solar-bateria');
  var outKw = document.getElementById('solar-kwp');
  var outCoste = document.getElementById('solar-coste');
  var outAhorro = document.getElementById('solar-ahorro');
  var outPay = document.getElementById('solar-pay');
  var desglose = document.getElementById('solar-desglose');

  function clamp(n) {
    n = parseFloat(n);
    return (isNaN(n) || n < 0) ? 0 : n;
  }

  function usd(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function years(a, b) {
    if (a > 30) return '30+ years';
    return Math.round(a) + '–' + (b > 30 ? '30+' : Math.round(b)) + ' years';
  }

  function recalcular() {
    var kwhAnual = clamp(consumo.value) * 12;
    var kw = kwhAnual / PRODUCCION;
    var kwhBat = parseInt(bateria.value, 10);

    var panelMin = kw * PANEL_MIN, panelMax = kw * PANEL_MAX;
    var batMin = kwhBat * BAT_MIN, batMax = kwhBat * BAT_MAX;
    var costeMin = panelMin + batMin, costeMax = panelMax + batMax;
    var ahorro = kwhAnual * AUTOCONSUMO[kwhBat] * clamp(precio.value);

    outKw.textContent = kw.toFixed(1) + ' kW';
    outCoste.textContent = usd(costeMin) + ' – ' + usd(costeMax);
    outAhorro.textContent = usd(ahorro) + ' / yr';
    outPay.textContent = ahorro > 0 ? years(costeMin / ahorro, costeMax / ahorro) : '—';

    var texto = 'Panels: ' + usd(panelMin) + ' – ' + usd(panelMax);
    if (kwhBat > 0) {
      texto += ' · ' + kwhBat + ' kWh battery: ' + usd(batMin) + ' – ' + usd(batMax);
    }
    desglose.textContent = texto;
  }

  [consumo, precio].forEach(function (i) { i.addEventListener('input', recalcular); });
  bateria.addEventListener('change', recalcular);

  var q = parseFloat(new URLSearchParams(window.location.search).get('kwh'));
  if (!isNaN(q) && q > 0) consumo.value = Math.round(q);

  recalcular();
})();
</script>
