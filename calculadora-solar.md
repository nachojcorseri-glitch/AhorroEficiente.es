---
layout: page
title: "Calculadora de instalación solar"
permalink: /calculadora-solar/
---

<p class="site-intro">Un cálculo orientativo de cuánta potencia necesitarías y qué podría costar, según tu consumo y tu país. Son rangos amplios a propósito — para un precio real, pide presupuesto a instaladores locales.</p>

<div class="calc-card">
  <div class="calc-field">
    <label for="solar-pais">País</label>
    <select id="solar-pais">
      <option value="es">España</option>
      <option value="mx">México</option>
    </select>
  </div>

  <div class="calc-field">
    <label for="solar-consumo">Consumo medio mensual (kWh) — mira tu factura</label>
    <input type="number" id="solar-consumo" min="0" step="10" value="300">
  </div>

  <div class="calc-field calc-checkbox">
    <label><input type="checkbox" id="solar-bateria"> Quiero batería de almacenamiento</label>
  </div>

  <div class="calc-result calc-result-solar">
    <div><span>Potencia orientativa</span><strong id="solar-kwp">0 kWp</strong></div>
    <div><span>Coste estimado</span><strong id="solar-coste">0 €</strong></div>
  </div>

  <p class="calc-hint" id="solar-nota">Estimación basada en horas de sol medias y precios por kWp instalado de referencia en 2026. La batería, si la marcas, sube el rango bastante — depende mucho de la capacidad que elijas.</p>
</div>

<script>
(function () {
  var DATOS = {
    es: { produccion: 1400, costeMin: 1000, costeMax: 1800, bateriaMin: 4000, bateriaMax: 7000, moneda: '€', nombre: 'España' },
    mx: { produccion: 1700, costeMin: 15000, costeMax: 25000, bateriaMin: 60000, bateriaMax: 120000, moneda: 'MXN', nombre: 'México' }
  };

  var pais = document.getElementById('solar-pais');
  var consumo = document.getElementById('solar-consumo');
  var bateria = document.getElementById('solar-bateria');
  var outKwp = document.getElementById('solar-kwp');
  var outCoste = document.getElementById('solar-coste');
  var nota = document.getElementById('solar-nota');

  function clamp(n) {
    n = parseFloat(n);
    if (isNaN(n) || n < 0) return 0;
    return n;
  }

  function fmtMoneda(n, moneda) {
    var texto = Math.round(n).toLocaleString('es-ES');
    return moneda === '€' ? (texto + ' €') : (texto + ' ' + moneda);
  }

  function recalcular() {
    var d = DATOS[pais.value];
    var kwhMes = clamp(consumo.value);
    var kwhAnual = kwhMes * 12;
    var kwp = d.produccion > 0 ? kwhAnual / d.produccion : 0;

    var costeMin = kwp * d.costeMin;
    var costeMax = kwp * d.costeMax;

    if (bateria.checked) {
      costeMin += d.bateriaMin;
      costeMax += d.bateriaMax;
    }

    outKwp.textContent = kwp.toFixed(1).replace('.', ',') + ' kWp';
    outCoste.textContent = fmtMoneda(costeMin, d.moneda) + ' – ' + fmtMoneda(costeMax, d.moneda);
    nota.textContent = 'Estimación orientativa para ' + d.nombre + ', con precios de referencia de 2026. La batería, si la marcas, ya está sumada al rango — varía mucho según la capacidad elegida. Para un precio real, pide presupuesto a instaladores locales.';
  }

  pais.addEventListener('change', recalcular);
  consumo.addEventListener('input', recalcular);
  bateria.addEventListener('change', recalcular);

  recalcular();
})();
</script>
