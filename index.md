---
layout: page
title: Inicio
<section class="hero">
  <div class="hero-text">
    <h1>Ahorra en tu factura sin complicarte</h1>
    <p class="site-intro">Guías claras y sin relleno sobre consumo eléctrico, tarifas, electrodomésticos y energía solar — para decidir con datos, no con suposiciones.</p>
    <a class="lang-link" href="/en/">🇬🇧 Read this site in English</a>
  </div>
  <div class="hero-icon">{% include icon.html name="house" %}</div>
</section>
<div class="topics">
  <a class="topic-badge" href="/categoria/tarifas/">{% include icon.html name="gauge" %}Tarifas y factura</a>
  <a class="topic-badge" href="/categoria/electrodomesticos/">{% include icon.html name="plug" %}Electrodomésticos</a>
  <a class="topic-badge" href="/categoria/solar/">{% include icon.html name="sun" %}Energía solar</a>
  <a class="topic-badge" href="/categoria/domotica/">{% include icon.html name="bulb" %}Domótica</a>
</div>
<div class="calc-cta">
  {% include icon.html name="gauge" %}
  <div class="calc-cta-text">
    <strong>¿Cuánto gasta realmente tu frigorífico, tu aire acondicionado o cualquier aparato?</strong>
    <a class="button" href="/calculadora/">Pruébalo en la calculadora →</a>
  </div>
</div>
<h2 class="section-title">Últimos artículos</h2>
<ul class="post-list">
{% assign sorted_posts = site.posts | sort: 'date' | reverse %}
{% for post in sorted_posts %}
  <li class="post-card">
    <span class="post-card-icon">{% include icon.html name=post.icon %}</span>
    <div class="post-card-body">
      <span class="post-meta">{{ post.date | date: "%d %b %Y" }}</span>
      <h3><a class="post-link" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h3>
      <p class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 28 }}</p>
    </div>
  </li>
{% endfor %}
</ul>
