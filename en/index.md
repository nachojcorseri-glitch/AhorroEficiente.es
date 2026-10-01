---
layout: page
title: Home
permalink: /en/
---

<p class="site-intro">Practical, no-nonsense guides on home energy costs and savings —
how much things actually cost to run, and what's worth doing about it.</p>

<p><a class="lang-link" href="/">🇪🇸 Leer este sitio en español</a></p>

<div class="home">
<ul class="post-list">
{% assign sorted_posts = site.posts_en | sort: 'date' | reverse %}
{% for post in sorted_posts %}
  <li>
    <span class="post-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
    <h3>
      <a class="post-link" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
    </h3>
  </li>
{% endfor %}
</ul>
</div>
