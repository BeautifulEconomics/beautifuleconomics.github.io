<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Beautiful Economics</title>
  <meta name="description" content="Beautiful Economics — clarity, elegance and insight on economics. Short essays, visuals and practical ideas." />
  <!-- Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:wght@500;600&display=swap" rel="stylesheet">
  <style>
    :root{
      --bg: #faf9f7;             /* soft off-white */
      --card: #ffffff;
      --text: #101018;           /* deep charcoal */
      --muted: #6f6f77;
      --accent: #c69d53;         /* warm gold */
      --glass: rgba(255,255,255,0.6);
      --max-width: 1100px;
      --radius: 14px;
      --ease: cubic-bezier(.2,.9,.3,1);
    }

    /* Reset & base */
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      font-family:Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
      background: radial-gradient(1200px 600px at 10% 10%, rgba(198,157,83,0.04), transparent 8%),
                  radial-gradient(900px 400px at 90% 80%, rgba(16,16,24,0.02), transparent 6%),
                  var(--bg);
      color:var(--text);
      -webkit-font-smoothing:antialiased;
      -moz-osx-font-smoothing:grayscale;
      line-height:1.5;
      padding:32px 20px;
      display:flex;
      justify-content:center;
    }

    .wrap{max-width:var(--max-width); width:100%}

    /* Header / nav */
    header{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:20px;
      margin-bottom:48px;
    }
    .brand{
      display:flex;
      gap:12px;
      align-items:center;
      text-decoration:none;
      color:var(--text);
    }
    .logo{
      width:54px;
      height:54px;
      border-radius:12px;
      background:linear-gradient(135deg, rgba(198,157,83,0.14), rgba(16,16,24,0.03));
      display:grid;
      place-items:center;
      box-shadow: 0 6px 18px rgba(16,16,24,0.06);
      font-family: "Playfair Display", serif;
      font-weight:600;
      color:var(--text);
    }
    .brand h4{margin:0; font-family:"Playfair Display", serif; font-size:18px; letter-spacing:0.2px}
    .brand p{margin:0; font-size:12px; color:var(--muted)}

    nav a{
      text-decoration:none;
      color:var(--muted);
      font-size:14px;
      margin-left:18px;
      transition: color .25s var(--ease);
    }
    nav a:hover{color:var(--text)}

    /* Hero */
    .hero{
      display:grid;
      grid-template-columns: 1fr;
      gap:28px;
      align-items:center;
      padding:48px;
      background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(255,255,255,0.85));
      border-radius:var(--radius);
      box-shadow: 0 10px 30px rgba(16,16,24,0.06);
      overflow:hidden;
    }
    .hero-inner{
      max-width:760px;
      margin:auto;
      text-align:center;
    }
    h1{
      margin:0 0 12px 0;
      font-family:"Playfair Display", serif;
      font-weight:600;
      font-size:42px;
      letter-spacing:-0.6px;
      color:var(--text);
    }
    .tag{
      margin:0 auto;
      color:var(--muted);
      font-size:18px;
      max-width:640px;
    }
    .hero-cta{
      margin-top:26px;
      display:flex;
      gap:14px;
      justify-content:center;
      flex-wrap:wrap;
    }
    .btn{
      padding:12px 22px;
      border-radius:10px;
      text-decoration:none;
      font-weight:600;
      transition: transform .28s var(--ease), box-shadow .28s var(--ease);
      display:inline-block;
    }
    .btn-primary{
      background: linear-gradient(90deg, var(--text), rgba(16,16,24,0.9));
      color:#fff;
      box-shadow: 0 8px 30px rgba(16,16,24,0.08);
    }
    .btn-outline{
      border:1px solid rgba(16,16,24,0.06);
      background:transparent;
      color:var(--text);
    }
    .btn-primary:hover{transform:translateY(-4px); box-shadow: 0 14px 44px rgba(16,16,24,0.12)}
    .btn-outline:hover{transform:translateY(-2px)}

    /* Sections */
    section{margin-top:40px}
    .container{display:grid; gap:28px}

    .about{
      display:grid;
      grid-template-columns: 1fr 360px;
      gap:28px;
      align-items:center;
    }
    .about p{color:var(--muted); font-size:15px; margin:0}

    .card{
      background:var(--card);
      padding:20px;
      border-radius:12px;
      box-shadow: 0 6px 18px rgba(16,16,24,0.04);
    }

    /* Insights grid */
    .insights{
      display:grid;
      grid-template-columns: repeat(auto-fit, minmax(220px,1fr));
      gap:20px;
      margin-top:6px;
    }
    .insight{
      background:linear-gradient(180deg, #fff, rgba(250,249,247,0.9));
      padding:20px;
      border-radius:12px;
      min-height:140px;
      transition: transform .45s var(--ease), box-shadow .45s var(--ease);
      cursor:default;
    }
    .insight h3{margin:0 0 8px 0; font-size:18px; font-family:"Playfair Display", serif}
    .insight p{margin:0; color:var(--muted); font-size:14px}

    .insight:hover{transform:translateY(-8px); box-shadow:0 16px 40px rgba(16,16,24,0.06)}

    /* Connect bar */
    .connect{
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:20px;
      padding:18px;
      border-radius:12px;
      background:linear-gradient(180deg, rgba(255,255,255,0.85), rgba(255,255,255,0.8));
      box-shadow: 0 8px 22px rgba(16,16,24,0.03);
    }
    .socials{display:flex; gap:14px; align-items:center}
    .socials a{display:inline-grid; place-items:center; width:44px; height:44px; border-radius:10px; background:transparent; text-decoration:none; color:var(--text); transition:transform .22s var(--ease)}
    .socials a:hover{transform:translateY(-4px)}
    .socials svg{width:20px; height:20px; opacity:0.9}

    footer{margin-top:48px; text-align:center; color:var(--muted); font-size:13px; padding:28px 6px}

    /* small screens */
    @media (max-width:880px){
      .about{grid-template-columns:1fr; text-align:center}
      .hero{padding:36px}
      h1{font-size:32px}
    }

    /* animations */
    .fade-in {opacity:0; transform: translateY(8px); transition: opacity .9s var(--ease), transform .9s var(--ease)}
    .in-view{opacity:1; transform: none}
    /* subtle background motion */
    .bg-wave{
      pointer-events:none;
      position:absolute;
      inset:0;
      z-index:0;
      opacity:0.06;
      background-image:
        radial-gradient(800px 220px at 10% 20%, rgba(198,157,83,0.06), transparent 6%),
        radial-gradient(500px 160px at 86% 80%, rgba(16,16,24,0.04), transparent 6%);
      transition:opacity 1s;
    }
  </style>
</head>
<body>
  <div class="bg-wave"></div>

  <main class="wrap" role="main">
    <header>
      <a class="brand" href="#" aria-label="Beautiful Economics home">
        <div class="logo">BE</div>
        <div>
          <h4>Beautiful Economics</h4>
          <p>Clarity · Elegance · Insight</p>
        </div>
      </a>
      <nav aria-label="Primary">
        <a href="#about">About</a>
        <a href="#insights">Insights</a>
        <a href="#connect">Connect</a>
      </nav>
    </header>

    <section class="hero card" aria-labelledby="hero-title">
      <div class="hero-inner">
        <h1 id="hero-title" class="fade-in">Beautiful Economics</h1>
        <p class="tag fade-in">Where clarity meets thoughtful insight — short essays and visual explainers that make economic ideas simple and elegant.</p>

        <div class="hero-cta fade-in">
          <a class="btn btn-primary" href="#insights">Explore Insights</a>
          <a class="btn btn-outline" href="https://www.facebook.com/beautifulecos/" target="_blank" rel="noopener">Visit our Facebook</a>
        </div>
      </div>
    </section>

    <section id="about" class="container">
      <div class="about">
        <div class="card fade-in">
          <h2 style="margin-top:0; font-family:'Playfair Display', serif;">About Beautiful Economics</h2>
          <p>Beautiful Economics is a space to present important economic ideas with clarity and calm. We translate complex concepts into short, memorable insights and useful visuals — for students, thinkers, and curious readers.</p>
        </div>

        <aside class="card fade-in" aria-label="Quick facts">
          <h4 style="margin:0 0 8px 0">Quick facts</h4>
          <p style="margin:0; color:var(--muted);">18k+ followers on Facebook • Essays • Visual posts • Simple explainers</p>
        </aside>
      </div>
    </section>

    <section id="insights" class="card" aria-labelledby="insights-title">
      <h2 id="insights-title" style="margin-top:0; font-family:'Playfair Display', serif">Featured ideas</h2>
      <div class="insights" role="list">
        <article class="insight fade-in" role="listitem">
          <h3>Inflation — Simple Lens</h3>
          <p>Why prices rise, what it means for people, and how subtle policy choices shape outcomes.</p>
        </article>
        <article class="insight fade-in" role="listitem">
          <h3>Liquidity & Traps</h3>
          <p>Short explanation with a visual metaphor — how a market can run out of “push” even with low rates.</p>
        </article>
        <article class="insight fade-in" role="listitem">
          <h3>Growth That Lasts</h3>
          <p>Why investments in skills, ideas and institutions matter more than short-term signals.</p>
        </article>
        <article class="insight fade-in" role="listitem">
          <h3>Exchange & Value</h3>
          <p>Real Effective Exchange Rate explained in a single visual-friendly paragraph.</p>
        </article>
      </div>
    </section>

    <section id="connect" class="connect fade-in" aria-label="Connect">
      <div>
        <strong>Stay in touch</strong>
        <div style="color:var(--muted); margin-top:6px; font-size:14px">Short essays and visual explainers delivered on our social channels.</div>
      </div>

      <div class="socials" aria-hidden="false">
        <!-- Facebook -->
        <a href="https://www.facebook.com/beautifulecos/" target="_blank" rel="noopener" aria-label="Facebook">
          <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22 12a10 10 0 10-11.5 9.9v-7h-2v-3h2v-2.3c0-2 1.2-3.1 3-3.1.9 0 1.8.16 1.8.16v2h-1c-1 0-1.3.64-1.3 1.3V12h2.3l-.37 3H15v7A10 10 0 0022 12z"/></svg>
        </a>
        <!-- Instagram -->
        <a href="https://www.instagram.com/" target="_blank" rel="noopener" aria-label="Instagram">
          <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 2h10a5 5 0 015 5v10a5 5 0 01-5 5H7a5 5 0 01-5-5V7a5 5 0 015-5zm5 6.5A4.5 4.5 0 1016.5 13 4.5 4.5 0 0012 8.5zm6.8-.6a1.05 1.05 0 11-1.05-1.05 1.05 1.05 0 011.05 1.05zM12 10.5A1.5 1.5 0 1110.5 12 1.5 1.5 0 0112 10.5z"/></svg>
        </a>
        <!-- Linkedin -->
        <a href="https://www.linkedin.com/" target="_blank" rel="noopener" aria-label="LinkedIn">
          <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 3H4a1 1 0 00-1 1v16a1 1 0 001 1h16a1 1 0 001-1V4a1 1 0 00-1-1zM8.5 18H6.2V10.8h2.3V18zM7.35 9.6a1.3 1.3 0 110-2.6 1.3 1.3 0 010 2.6zM18 18h-2.3v-3.9c0-.9 0-2.1-1.3-2.1-1.3 0-1.5 1-1.5 2V18H10.6V10.8h2.2v1h.03c.3-.6 1-1.3 2.2-1.3 2.3 0 2.7 1.5 2.7 3.5V18z"/></svg>
        </a>
      </div>
    </section>

    <footer>
      © <span id="year"></span> Beautiful Economics · All rights reserved
    </footer>
  </main>

  <!-- Lightweight JS for animations & small UX -->
  <script>
    // set year
    document.getElementById('year').textContent = new Date().getFullYear();

    // Intersection Observer to reveal on scroll
    (function(){
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => {
          if(e.isIntersecting) e.target.classList.add('in-view');
        });
      }, { threshold: 0.15 });

      document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
    })();

    // Smooth scroll for same-page anchors
    document.querySelectorAll('a[href^="#"]').forEach(a=>{
      a.addEventListener('click', e=>{
        const href = a.getAttribute('href');
        if(href.length>1){
          e.preventDefault();
          document.querySelector(href).scrollIntoView({behavior:'smooth', block:'start'});
        }
      });
    });
  </script>
</body>
</html>
