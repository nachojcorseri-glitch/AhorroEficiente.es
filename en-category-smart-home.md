---
layout: page
title: "Smart Home"
permalink: /en/category/smart-home/
---

<p class="site-intro">Smart plugs, thermostats, and devices that help you save without thinking about it.</p>

<ul class="post-list">
{% assign posts_categoria = site.posts_en | where_exp: "post", "post.categories contains 'domotica'" | sort: 'date' | reverse %}
{% for post in posts_categoria %}
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

{% if posts_categoria.size == 0 %}
<p class="calc-hint">No articles in this category yet — check back soon.</p>
{% endif %}
