(function () {
  var root = document.getElementById('calc-root');
  if (!root) return;

  var lang = root.getAttribute('data-lang') === 'en' ? 'en' : 'es';
  var moneda = root.getAttribute('data-currency') || '';
  var solarUrl = root.getAttribute('data-solar-url') || '/calculadora-solar/';

  var TXT = {
    es: { otro: 'Otro (pongo los vatios)', cant: 'Cantidad', horas: 'Horas al día', vatios: 'Vatios', quitar: 'Quitar', locale: 'es-ES', mes: ' / mes' },
    en: { otro: 'Other (enter wattage)', cant: 'Quantity', horas: 'Hours per day', vatios: 'Watts', quitar: 'Remove', locale: 'en-US', mes: ' / mo' }
  }[lang];

  // [vatios típicos, nombre ES, nombre EN, horas/día por defecto]
  var APARATOS = [
    [150, 'Frigorífico', 'Refrigerator', 24],
    [800, 'Lavadora', 'Washing machine', 1],
    [1200, 'Lavavajillas', 'Dishwasher', 1.5],
    [1000, 'Aire acondicionado', 'Air conditioner', 4],
    [2000, 'Horno eléctrico', 'Electric oven', 1],
    [1000, 'Microondas', 'Microwave', 0.25],
    [2500, 'Secadora', 'Clothes dryer', 1],
    [100, 'Televisor LED', 'LED TV', 4],
    [200, 'Ordenador de sobremesa', 'Desktop computer', 4],
    [10, 'Bombilla LED', 'LED bulb', 5]
  ];

  var rowsBox = document.getElementById('calc-rows');
  var addBtn = document.getElementById('calc-add');
  var precio = document.getElementById('calc-precio');
  var outKwh = document.getElementById('calc-kwh');
  var outDia = document.getElementById('calc-dia');
  var outMes = document.getElementById('calc-mes');
  var outAnio = document.getElementById('calc-anio');
  var solarLink = document.getElementById('calc-solar-link');

  function clamp(n, max) {
    n = parseFloat(n);
    if (isNaN(n) || n < 0) return 0;
    return (typeof max === 'number' && n > max) ? max : n;
  }

  function dinero(n) {
    var t = n.toLocaleString(TXT.locale, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    if (!moneda) return t;
    return lang === 'es' ? t + ' ' + moneda : moneda + t;
  }

  function energia(n) {
    return n.toLocaleString(TXT.locale, { maximumFractionDigits: 1 }) + ' kWh';
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }

  function numero(min, max, step, valor) {
    var i = el('input');
    i.type = 'number';
    i.min = min;
    i.max = max;
    i.step = step;
    i.value = valor;
    return i;
  }

  function campo(etiqueta, input) {
    var w = el('div', 'calc-mini');
    w.appendChild(el('span', '', etiqueta));
    w.appendChild(input);
    return w;
  }

  function nuevaFila(idx) {
    var fila = el('div', 'calc-row');

    var sel = el('select');
    APARATOS.forEach(function (a, i) {
      var o = el('option', '', lang === 'es' ? a[1] : a[2]);
      o.value = String(i);
      sel.appendChild(o);
    });
    var oc = el('option', '', TXT.otro);
    oc.value = 'custom';
    sel.appendChild(oc);
    sel.value = String(idx);

    var custom = numero(0, 20000, 10, 1000);
    var customWrap = campo(TXT.vatios, custom);
    customWrap.style.display = 'none';
    var cant = numero(1, 99, 1, 1);
    var horas = numero(0, 24, 0.25, APARATOS[idx][3]);
    var coste = el('div', 'calc-row-cost');

    var quitar = el('button', 'calc-remove', '✕');
    quitar.type = 'button';
    quitar.title = TXT.quitar;
    quitar.setAttribute('aria-label', TXT.quitar);

    var top = el('div', 'calc-row-top');
    top.appendChild(sel);
    top.appendChild(quitar);

    var campos = el('div', 'calc-row-fields');
    campos.appendChild(customWrap);
    campos.appendChild(campo(TXT.cant, cant));
    campos.appendChild(campo(TXT.horas, horas));
    campos.appendChild(coste);

    fila.appendChild(top);
    fila.appendChild(campos);

    sel.addEventListener('change', function () {
      var esCustom = sel.value === 'custom';
      customWrap.style.display = esCustom ? 'block' : 'none';
      if (!esCustom) horas.value = APARATOS[parseInt(sel.value, 10)][3];
      recalcular();
    });
    [custom, cant, horas].forEach(function (i) {
      i.addEventListener('input', recalcular);
    });
    quitar.addEventListener('click', function () {
      rowsBox.removeChild(fila);
      recalcular();
    });

    fila.leer = function () {
      var w = sel.value === 'custom' ? clamp(custom.value, 20000) : APARATOS[parseInt(sel.value, 10)][0];
      return { w: w, q: clamp(cant.value, 99), h: clamp(horas.value, 24) };
    };
    fila.pintarCoste = function (kwhDia, precioKwh) {
      coste.textContent = dinero(kwhDia * 30 * precioKwh) + TXT.mes;
    };
    return fila;
  }

  function recalcular() {
    var p = clamp(precio.value);
    var kwhDia = 0;
    var filas = rowsBox.children;
    for (var i = 0; i < filas.length; i++) {
      var d = filas[i].leer();
      var k = (d.w / 1000) * d.q * d.h;
      kwhDia += k;
      filas[i].pintarCoste(k, p);
    }
    var kwhMes = kwhDia * 30;
    outKwh.textContent = energia(kwhMes);
    outDia.textContent = dinero(kwhDia * p);
    outMes.textContent = dinero(kwhMes * p);
    outAnio.textContent = dinero(kwhDia * 365 * p);
    solarLink.href = kwhMes > 0 ? solarUrl + '?kwh=' + Math.round(kwhMes) : solarUrl;
  }

  [0, 7, 1].forEach(function (i) { rowsBox.appendChild(nuevaFila(i)); });
  addBtn.addEventListener('click', function () {
    rowsBox.appendChild(nuevaFila(1));
    recalcular();
  });
  precio.addEventListener('input', recalcular);
  recalcular();
})();
