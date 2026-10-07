---
layout: page
title: Home
permalink: /en/
---

<section class="hero">
  <div class="hero-text">
    <h1>Lower your power bill without the guesswork</h1>
    <p class="site-intro">Clear, no-filler guides on home energy costs — appliances, heating and cooling, smart home gear, and solar.</p>
    <a class="lang-link" href="/">🇪🇸 Leer este sitio en español</a>
  </div>
  <div class="hero-icon">{% include icon.html name="house" %}</div>
</section>

<div class="topics">
  <a class="topic-badge" href="/en/category/bills-rates/">{% include icon.html name="gauge" %}Bills &amp; Rates</a>
  <a class="topic-badge" href="/en/category/appliances/">{% include icon.html name="plug" %}Appliances</a>
  <a class="topic-badge" href="/en/category/solar/">{% include icon.html name="sun" %}Solar</a>
  <a class="topic-badge" href="/en/category/smart-home/">{% include icon.html name="bulb" %}Smart Home</a>
</div>

<div class="calc-cta">
  {% include icon.html name="gauge" %}
  <div class="calc-cta-text">
    <strong>How much does your fridge, AC, or any appliance really cost to run?</strong>
    <a class="button" href="/en/calculator/">Try the calculator →</a>
  </div>
</div>

<h2 class="section-title">Latest articles</h2>
<ul class="post-list">
{% assign sorted_posts = site.posts_en | sort: 'date' | reverse %}
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
