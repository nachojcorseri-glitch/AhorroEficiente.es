---
layout: page
title: Inicio
---

<section class="hero">
  <div class="hero-text">
    <h1>Ahorra en tu factura sin complicarte</h1>
    <p class="site-intro">Guías claras y sin relleno sobre consumo eléctrico, tarifas, electrodomésticos y energía solar — para decidir con datos, no con suposiciones.</p>
    <a class="lang-link" href="/en/">🇬🇧 Read this site in English</a>
  </div>
  <div class="hero-icon">{% include icon.html name="house" %}</div>
</section>

<div class="topics">
  <span class="topic-badge">{% include icon.html name="gauge" %}Tarifas y factura</span>
  <span class="topic-badge">{% include icon.html name="plug" %}Electrodomésticos</span>
  <span class="topic-badge">{% include icon.html name="sun" %}Energía solar</span>
  <span class="topic-badge">{% include icon.html name="bulb" %}Domótica</span>
</div>

<h2 class="section-title">Últimos artículos</h2>
<ul class="post-list">
{% assign sorted_posts = site.posts | sort: 'date' | reverse %}
{% for post in sorted_posts %}
  <li class="post-card">
    <span class="post-card-icon">{% include icon.html name=post.icon | default: "house" %}</span>
    <div class="post-card-body">
      <span class="post-meta">{{ post.date | date: "%d %b %Y" }}</span>
      <h3><a class="post-link" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h3>
      <p class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 28 }}</p>
    </div>
  </li>
{% endfor %}
</ul>
