---
layout: page
title: "Calculadora de consumo eléctrico"
permalink: /calculadora/
---

<p class="site-intro">Añade todos los aparatos que quieras, indica cuántos tienes y cuántas horas los usas al día, y te sale el consumo y el coste aproximado de todos juntos. El cálculo se hace en tu navegador: no se envía ni se guarda nada.</p>

<div class="calc-card calc-card-wide" id="calc-root" data-lang="es" data-currency="€" data-solar-url="/calculadora-solar/">
  <div id="calc-rows"></div>
  <button type="button" class="calc-add" id="calc-add">+ Añadir aparato</button>

  <div class="calc-field">
    <label for="calc-precio">Precio por kWh que pagas (€)</label>
    <input type="number" id="calc-precio" min="0" step="0.01" value="0.17">
    <p class="calc-hint">Ajusta esto al precio real de tu factura actual — cambia con el tiempo y según la tarifa.</p>
  </div>

  <div class="calc-result calc-result-4">
    <div><span>Consumo al mes</span><strong id="calc-kwh">0 kWh</strong></div>
    <div><span>Coste al día</span><strong id="calc-dia">0,00 €</strong></div>
    <div><span>Coste al mes</span><strong id="calc-mes">0,00 €</strong></div>
    <div><span>Coste al año</span><strong id="calc-anio">0,00 €</strong></div>
  </div>

  <a class="calc-solar-link" id="calc-solar-link" href="/calculadora-solar/">¿Y con placas solares? Calcula una instalación para este consumo →</a>

  <p class="calc-hint">Los vatios de la lista son valores típicos orientativos: el consumo real de tu modelo concreto puede variar bastante. Para el dato exacto, mira la etiqueta energética o el manual del aparato. Al elegir un aparato se rellenan unas horas de uso habituales, que puedes cambiar.</p>
</div>

<script src="{{ '/assets/calc.js' | relative_url }}" defer></script>
