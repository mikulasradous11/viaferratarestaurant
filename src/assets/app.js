/* Restaurace Via Ferrata – sdílený skript pro všechny stránky a jazyky */
{
  const D = JSON.parse(document.getElementById('site-data').textContent);
  const S = D.strings;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const pad = n => String(n).padStart(2, '0');
  const toMin = t => { const [h, m] = t.split(':').map(Number); return h * 60 + m; };
  const fromMin = m => pad(Math.floor(m / 60)) + ':' + pad(m % 60);
  const esc = v => String(v).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  // dny: 0 = pondělí … 6 = neděle
  const dayIdx = d => (d.getDay() + 6) % 7;

  /* ---------- hlavička ---------- */
  const hdr = $('.hdr');
  const onScroll = () => hdr && hdr.classList.toggle('solid', window.scrollY > 40);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  const mb = $('.menu-btn');
  if (mb) mb.addEventListener('click', () => {
    const open = hdr.classList.toggle('open');
    mb.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
  $$('.nav a').forEach(a => a.addEventListener('click', () => {
    hdr.classList.remove('open'); document.body.style.overflow = '';
    if (mb) mb.setAttribute('aria-expanded', 'false');
  }));

  /* ---------- světlý / tmavý režim ---------- */
  const root = document.documentElement;
  const metaTheme = document.querySelector('meta[name=theme-color]');
  const applyTheme = (t, save) => {
    root.dataset.theme = t;
    if (metaTheme) metaTheme.content = t === 'dark' ? '#141414' : '#ffffff';
    $$('.theme-btn').forEach(b => b.setAttribute('aria-pressed', t === 'dark'));
    if (save) { try { localStorage.setItem('vf-theme', t); } catch (e) {} }
  };
  if (root.dataset.theme !== 'dark' && root.dataset.theme !== 'light') {
    applyTheme(window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light', false);
  } else applyTheme(root.dataset.theme, false);
  $$('.theme-btn').forEach(b => b.addEventListener('click', () => applyTheme(root.dataset.theme === 'dark' ? 'light' : 'dark', true)));
  if (window.matchMedia) {
    const mq = matchMedia('(prefers-color-scheme: dark)');
    const follow = e => { let saved = null; try { saved = localStorage.getItem('vf-theme'); } catch (err) {} if (!saved) applyTheme(e.matches ? 'dark' : 'light', false); };
    if (mq.addEventListener) mq.addEventListener('change', follow);
  }

  /* ---------- otevírací doba ---------- */
  const now = new Date();
  const today = D.hours[dayIdx(now)];
  const nowMin = now.getHours() * 60 + now.getMinutes();
  $$('[data-open-status]').forEach(el => {
    let txt, cls;
    if (today && nowMin >= toMin(today[0]) && nowMin < toMin(today[1])) {
      txt = S.openNow.replace('{t}', today[1]); cls = 'on';
    } else if (today && nowMin < toMin(today[0])) {
      txt = S.opensAt.replace('{t}', today[0]); cls = 'off';
    } else {
      // najdi další otevřený den
      let k = 1, nd = null;
      while (k < 8 && !(nd = D.hours[(dayIdx(now) + k) % 7])) k++;
      txt = nd ? S.closedNext.replace('{d}', S.days[(dayIdx(now) + k) % 7]).replace('{t}', nd[0]) : S.closed;
      cls = 'off';
    }
    el.innerHTML = '<span class="dot ' + cls + '"></span>' + esc(txt);
  });
  $$('[data-today-hours]').forEach(el => {
    el.textContent = today ? today[0] + '–' + today[1] : S.closed;
  });
  $$('.hours tr[data-day]').forEach(tr => {
    if (Number(tr.dataset.day) === dayIdx(now)) tr.classList.add('today');
  });

  /* ---------- odhalení při skrolování ---------- */
  const rvs = $$('.rv');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    rvs.forEach(el => io.observe(el));
  } else rvs.forEach(el => el.classList.add('in'));

  /* ---------- lightbox týdenního menu ---------- */
  const dlg = $('#menu-dialog');
  $$('[data-open-menu]').forEach(b => b.addEventListener('click', () => {
    if (dlg && dlg.showModal) dlg.showModal();
  }));
  if (dlg) dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });

  /* ---------- rezervační formulář ---------- */
  const rf = $('#reservation-form');
  if (rf) {
    const R = D.reservation;
    const date = $('#r-date'), guests = $('#r-guests'), slots = $('#r-slots'), timeIn = $('#r-time');
    const big = $('.big-group'), done = $('.done');
    const iso = d => d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
    const max = new Date(); max.setDate(max.getDate() + R.daysAhead);
    date.min = iso(now); date.max = iso(max);
    // první den, kdy je ještě volný slot
    const firstSlots = d => buildSlots(d).length;
    let start = new Date(now); let guard = 0;
    while (!firstSlots(start) && guard++ < 14) start.setDate(start.getDate() + 1);
    date.value = iso(start);

    function buildSlots(d) {
      const h = D.hours[dayIdx(d)];
      if (!h) return [];
      const out = [];
      const last = toMin(h[1]) - R.lastBeforeClose;
      const isToday = iso(d) === iso(new Date());
      const minNow = isToday ? new Date().getHours() * 60 + new Date().getMinutes() + R.leadMinutes : 0;
      for (let m = toMin(h[0]); m <= last; m += R.step) if (m >= minNow) out.push(fromMin(m));
      return out;
    }
    function renderSlots() {
      const d = new Date(date.value + 'T12:00');
      const list = isNaN(d) ? [] : buildSlots(d);
      const keep = timeIn.value;
      timeIn.value = list.includes(keep) ? keep : '';
      slots.innerHTML = list.length
        ? list.map(t => '<button type="button" class="slot" aria-pressed="' + (t === timeIn.value) + '" data-t="' + t + '">' + t + '</button>').join('')
        : '<p class="slots-empty">' + esc(S.noSlots) + '</p>';
    }
    slots.addEventListener('click', e => {
      const b = e.target.closest('.slot'); if (!b) return;
      timeIn.value = b.dataset.t;
      $$('.slot', slots).forEach(x => x.setAttribute('aria-pressed', x === b));
      setErr(timeIn, '');
    });
    date.addEventListener('change', () => { renderSlots(); setErr(date, ''); });
    guests.addEventListener('change', () => big.classList.toggle('show', guests.value === 'big'));
    renderSlots();

    function setErr(el, msg) {
      const f = el.closest('.field'); if (!f) return;
      f.classList.toggle('err', !!msg);
      const m = $('.msg', f); if (m) m.textContent = msg;
    }
    function validate() {
      let ok = true;
      const req = (el, cond, msg) => { if (!cond) { setErr(el, msg); ok = false; } else setErr(el, ''); };
      req(date, date.value && date.value >= date.min && date.value <= date.max, S.errDate);
      req(timeIn, !!timeIn.value, S.errTime);
      req(guests, guests.value && guests.value !== 'big', guests.value === 'big' ? S.errBig : S.errGuests);
      const name = $('#r-name'), tel = $('#r-phone'), mail = $('#r-email'), gdpr = $('#r-gdpr');
      req(name, name.value.trim().length > 1, S.errName);
      req(tel, /^[+\d][\d\s()-]{7,}$/.test(tel.value.trim()), S.errPhone);
      req(mail, /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mail.value.trim()), S.errEmail);
      req(gdpr, gdpr.checked, S.errGdpr);
      return ok;
    }
    rf.addEventListener('submit', async e => {
      e.preventDefault();
      if (!validate()) { const f = $('.field.err', rf); if (f) f.scrollIntoView({ block: 'center' }); return; }
      const data = {
        date: date.value, time: timeIn.value, guests: guests.value,
        area: (rf.querySelector('input[name=area]:checked') || {}).value || '',
        name: $('#r-name').value.trim(), phone: $('#r-phone').value.trim(),
        email: $('#r-email').value.trim(), note: $('#r-note').value.trim(), lang: D.lang
      };
      const btn = $('button[type=submit]', rf);
      btn.disabled = true; btn.textContent = S.sending;
      let sent = false;
      if (R.endpoint) {
        try {
          const res = await fetch(R.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) });
          sent = res.ok;
        } catch (err) { sent = false; }
        if (!sent) { btn.disabled = false; btn.textContent = S.submit; alertBox(S.errSend); return; }
      }
      const d = new Date(data.date + 'T12:00');
      const areaTxt = data.area ? S.areas[data.area] : S.noPref;
      $('.done dl').innerHTML = [
        [S.fDate, d.toLocaleDateString(D.locale, { weekday: 'long', day: 'numeric', month: 'long' })],
        [S.fTime, data.time], [S.fGuests, data.guests], [S.fArea, areaTxt],
        [S.fName, data.name], [S.fContact, data.phone + ', ' + data.email]
      ].map(([k, v]) => '<dt>' + esc(k) + '</dt><dd>' + esc(v) + '</dd>').join('');
      $('.demo', done).hidden = !!R.endpoint;
      rf.hidden = true; done.classList.add('show');
      done.scrollIntoView({ block: 'start' });
    });
    function alertBox(msg) {
      let a = $('.form-alert', rf);
      if (!a) { a = document.createElement('p'); a.className = 'big-group show form-alert'; rf.prepend(a); }
      a.textContent = msg;
    }
    const again = $('[data-again]');
    if (again) again.addEventListener('click', () => {
      rf.reset(); done.classList.remove('show'); rf.hidden = false;
      const b = $('button[type=submit]', rf); b.disabled = false; b.textContent = S.submit;
      date.value = iso(start); renderSlots(); big.classList.remove('show');
    });
  }

  /* ---------- poptávka pronájmu (e-mail) ---------- */
  const qf = $('#rental-form');
  if (qf) {
    qf.addEventListener('submit', e => {
      e.preventDefault();
      const f = n => (qf.elements[n] && qf.elements[n].value || '').trim();
      const name = qf.elements['q-name'], contact = qf.elements['q-contact'];
      let ok = true;
      [[name, f('q-name').length > 1], [contact, f('q-contact').length > 5]].forEach(([el, c]) => {
        el.closest('.field').classList.toggle('err', !c); $('.msg', el.closest('.field')).textContent = c ? '' : S.errRequired; if (!c) ok = false;
      });
      if (!ok) return;
      const body = [
        S.qHello, '',
        S.qType + ': ' + f('q-type'),
        S.fDate + ': ' + (f('q-date') || '—'),
        S.fGuests + ': ' + (f('q-guests') || '—'),
        S.qNote + ': ' + (f('q-note') || '—'), '',
        f('q-name'), f('q-contact')
      ].join('\n');
      const subject = S.qSubject + ' – ' + f('q-type') + (f('q-date') ? ' – ' + f('q-date') : '');
      const href = 'mailto:' + D.email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      const box = $('.copy-box'); $('textarea', box).value = subject + '\n\n' + body;
      box.classList.add('show');
      window.location.href = href;
    });
    const cp = $('[data-copy]');
    if (cp) cp.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText($('.copy-box textarea').value); cp.textContent = S.copied; }
      catch (e) { $('.copy-box textarea').select(); }
    });
  }
}
