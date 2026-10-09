---
layout: page
title: "Electricity Cost Calculator"
permalink: /en/calculator/
---

<p class="site-intro">Add as many appliances as you like, set how many you have and how many hours a day you use them, and get the approximate combined usage and cost. Everything is calculated in your own browser — nothing is sent or stored anywhere.</p>

<div class="calc-card calc-card-wide" id="calc-root" data-lang="en" data-currency="" data-solar-url="/en/solar-calculator/">
  <div id="calc-rows"></div>
  <button type="button" class="calc-add" id="calc-add">+ Add appliance</button>

  <div class="calc-field">
    <label for="calc-precio">Price per kWh you pay (your currency)</label>
    <input type="number" id="calc-precio" min="0" step="0.01" value="0.17">
    <p class="calc-hint">Match this to your actual bill — rates change over time and by plan.</p>
  </div>

  <div class="calc-result calc-result-4">
    <div><span>Usage per month</span><strong id="calc-kwh">0 kWh</strong></div>
    <div><span>Cost per day</span><strong id="calc-dia">0.00</strong></div>
    <div><span>Cost per month</span><strong id="calc-mes">0.00</strong></div>
    <div><span>Cost per year</span><strong id="calc-anio">0.00</strong></div>
  </div>

  <a class="calc-solar-link" id="calc-solar-link" href="/en/solar-calculator/">What about solar panels? Estimate a system for this usage →</a>

  <p class="calc-hint">The wattages in the list are typical, approximate figures — your exact model may use more or less. Check the energy label or manual for the precise number. Picking an appliance fills in typical daily hours, which you can change.</p>
</div>

<script src="{{ '/assets/calc.js' | relative_url }}" defer></script>
