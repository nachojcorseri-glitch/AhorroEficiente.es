---
layout: page
title: "Calculadora de instalación solar"
permalink: /calculadora-solar/
---

<p class="site-intro">Calcula la potencia que necesitarías, cuánto podría costar con o sin batería, cuánto ahorrarías al año y en cuántos años se amortizaría. Son rangos orientativos a propósito: para un precio real, pide presupuesto a instaladores locales.</p>

<div class="calc-card calc-card-wide">
  <div class="calc-field">
    <label for="solar-pais">País</label>
    <select id="solar-pais">
      <option value="es">España</option>
      <option value="mx">México</option>
    </select>
  </div>

  <div class="calc-field">
    <label for="solar-consumo">Consumo medio mensual (kWh) — mira tu factura o <a href="/calculadora/">calcúlalo con tus aparatos</a></label>
    <input type="number" id="solar-consumo" min="0" step="10" value="300">
  </div>

  <div class="calc-field">
    <label for="solar-precio" id="solar-precio-label">Precio por kWh que pagas (€)</label>
    <input type="number" id="solar-precio" min="0" step="0.01" value="0.17">
  </div>

  <div class="calc-field">
    <label for="solar-bateria">Batería de almacenamiento</label>
    <select id="solar-bateria">
      <option value="0">Sin batería</option>
      <option value="5">5 kWh</option>
      <option value="10">10 kWh</option>
      <option value="15">15 kWh</option>
      <option value="20">20 kWh</option>
    </select>
  </div>

  <div class="calc-result calc-result-4">
    <div><span>Potencia orientativa</span><strong id="solar-kwp">0 kWp</strong></div>
    <div><span>Coste estimado</span><strong id="solar-coste">0</strong></div>
    <div><span>Ahorro anual</span><strong id="solar-ahorro">0</strong></div>
    <div><span>Amortización</span><strong id="solar-pay">—</strong></div>
  </div>

  <p class="calc-hint" id="solar-desglose"></p>
  <p class="calc-hint">Supuestos: instalación dimensionada para cubrir tu consumo anual; sin batería se aprovecha en casa el 40 % de lo producido, y con batería sube (55 % con 5 kWh, 70 % con 10, 80 % con 15 y 85 % con 20). Los precios son de referencia de 2026; las ayudas, la compensación de excedentes y el sol de tu zona cambian mucho el resultado.</p>
</div>

<script>
(function () {
  var DATOS = {
    es: { produccion: 1400, panelMin: 1000, panelMax: 1800, batMin: 800, batMax: 1200, precio: 0.17, paso: 0.01, moneda: '€' },
    mx: { produccion: 1700, panelMin: 15000, panelMax: 25000, batMin: 14000, batMax: 24000, precio: 2.5, paso: 0.1, moneda: 'MXN' }
  };
  var AUTOCONSUMO = { 0: 0.40, 5: 0.55, 10: 0.70, 15: 0.80, 20: 0.85 };

  var pais = document.getElementById('solar-pais');
  var consumo = document.getElementById('solar-consumo');
  var precio = document.getElementById('solar-precio');
  var precioLabel = document.getElementById('solar-precio-label');
  var bateria = document.getElementById('solar-bateria');
  var outKwp = document.getElementById('solar-kwp');
  var outCoste = document.getElementById('solar-coste');
  var outAhorro = document.getElementById('solar-ahorro');
  var outPay = document.getElementById('solar-pay');
  var desglose = document.getElementById('solar-desglose');

  function clamp(n) {
    n = parseFloat(n);
    return (isNaN(n) || n < 0) ? 0 : n;
  }

  function fmt(n, moneda) {
    return Math.round(n).toLocaleString('es-ES') + ' ' + moneda;
  }

  function rangoAnios(a, b) {
    if (a > 30) return '+30 años';
    return Math.round(a) + '–' + (b > 30 ? '+30' : Math.round(b)) + ' años';
  }

  function recalcular() {
    var d = DATOS[pais.value];
    var kwhAnual = clamp(consumo.value) * 12;
    var kwp = kwhAnual / d.produccion;
    var kwhBat = parseInt(bateria.value, 10);

    var panelMin = kwp * d.panelMin, panelMax = kwp * d.panelMax;
    var batMin = kwhBat * d.batMin, batMax = kwhBat * d.batMax;
    var costeMin = panelMin + batMin, costeMax = panelMax + batMax;
    var ahorro = kwhAnual * AUTOCONSUMO[kwhBat] * clamp(precio.value);

    outKwp.textContent = kwp.toFixed(1).replace('.', ',') + ' kWp';
    outCoste.textContent = fmt(costeMin, d.moneda) + ' – ' + fmt(costeMax, d.moneda);
    outAhorro.textContent = fmt(ahorro, d.moneda) + ' / año';
    outPay.textContent = ahorro > 0 ? rangoAnios(costeMin / ahorro, costeMax / ahorro) : '—';

    var texto = 'Paneles: ' + fmt(panelMin, d.moneda) + ' – ' + fmt(panelMax, d.moneda);
    if (kwhBat > 0) {
      texto += ' · Batería de ' + kwhBat + ' kWh: ' + fmt(batMin, d.moneda) + ' – ' + fmt(batMax, d.moneda);
    }
    desglose.textContent = texto;
  }

  pais.addEventListener('change', function () {
    var d = DATOS[pais.value];
    precio.value = d.precio;
    precio.step = d.paso;
    precioLabel.textContent = 'Precio por kWh que pagas (' + d.moneda + ')';
    recalcular();
  });
  [consumo, precio].forEach(function (i) { i.addEventListener('input', recalcular); });
  bateria.addEventListener('change', recalcular);

  var q = parseFloat(new URLSearchParams(window.location.search).get('kwh'));
  if (!isNaN(q) && q > 0) consumo.value = Math.round(q);

  recalcular();
})();
</script>
