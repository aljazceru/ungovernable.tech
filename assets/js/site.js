/* ungovernable.tech site JS: search palette, theme toggle, mobile menu,
   contents scroll-spy, heading anchors, directory filter.
   Enhancement only — all content is in the static HTML. */
(function () {
'use strict';
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"]/g,
  c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const debounce = (fn, ms) => { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; };

/* ---------- theme (dark is the default; light is opt-in) ---------- */
const root = document.documentElement;
function applyTheme(t) {
  root.setAttribute('data-theme', t === 'light' ? 'light' : 'dark');
}
$('#theme-toggle')?.addEventListener('click', () => {
  const cur = root.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
  const next = cur === 'dark' ? 'light' : 'dark';
  applyTheme(next);
  try { localStorage.setItem('theme', next); } catch (e) { /* private mode */ }
});

/* ---------- overlays ---------- */
const scrim = $('#scrim');
function hideOverlays() {
  closeSheet();
  closeMenu(true);
  if (scrim) scrim.hidden = true;
}
scrim?.addEventListener('click', hideOverlays);

/* ---------- mobile menu ---------- */
const mbtn = $('#open-menu'), msheet = $('#menusheet');
function openMenu() {
  if (!msheet) return;
  msheet.hidden = false;
  if (scrim) scrim.hidden = false;
  mbtn?.setAttribute('aria-expanded', 'true');
  msheet.querySelector('a')?.focus();
}
function closeMenu(restore) {
  if (!msheet || msheet.hidden) return;
  msheet.hidden = true;
  if (!($('#sheet')?.hidden === false)) scrim.hidden = true;
  mbtn?.setAttribute('aria-expanded', 'false');
  if (restore) mbtn?.focus();
}
mbtn?.addEventListener('click', () => {
  msheet.hidden ? openMenu() : closeMenu(true);
});
msheet?.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
msheet?.addEventListener('keydown', e => {  /* focus trap */
  if (e.key !== 'Tab') return;
  const f = msheet.querySelectorAll('a[href]');
  if (!f.length) return;
  const first = f[0], last = f[f.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
});

/* ---------- search ---------- */
let IDX = null;
const sheet = $('#sheet'), input = $('#q'), resBox = $('#res'), resN = $('#res-n');
let sel = 0;

function loadIndex() {
  if (IDX) return Promise.resolve(IDX);
  return fetch('/assets/search.json')
    .then(r => r.json())
    .then(d => { IDX = d; return d; })
    .catch(() => { IDX = []; return IDX; });
}
const norm = s => String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
const titleHit = (t, q) => {
  const n = norm(t);
  if (n === q) return 6;
  if (n.startsWith(q)) return 5;
  if (n.includes(q)) return 4;
  const words = norm(t).split(/\W+/);
  if (words.some(w => w === q)) return 3;
  if (words.some(w => w.startsWith(q))) return 2;
  return 0;
};
function score(it, q) {
  if (!q) return 1;
  let s = titleHit(it.t, q) * 10;
  const alias = norm(it.a || '');
  if (alias.includes(q)) s += 8;
  if ((it.h || '') && norm(it.h).includes(q)) s += 5;
  if ((it.d || '') && norm(it.d).includes(q)) s += 2;
  if ((it.p || []).some(p => norm(p).includes(q))) s += 3;
  return s;
}
const bdg = r => r ? '<span class="bdg bdg-' +
  r.toLowerCase().replace(/[^a-z]+/g, '-') + '">' + esc(r) + '</span>' : '';
function rowHTML(it, isSel) {
  const meta = [(it.p || []).join(' · ')].filter(Boolean).join(' · ');
  return `<a class="row${isSel ? ' sel' : ''}" href="${it.u}">` +
    `<span class="nm">${esc(it.t)}<small>${esc(meta)}</small></span>` +
    bdg(it.r) +
    `<span class="ty">${esc(it.k)}</span></a>`;
}
function render() {
  const q = norm(input.value.trim());
  const hits = IDX.map(it => [score(it, q), it])
    .filter(x => x[0] > 0)
    .sort((a, b) => b[0] - a[0] || a[1].t.localeCompare(b[1].t))
    .slice(0, 25)
    .map(x => x[1]);
  sel = Math.min(sel, Math.max(0, hits.length - 1));
  resBox.innerHTML = hits.length
    ? hits.map((it, i) => rowHTML(it, i === sel)).join('')
    : '<p class="empty-dir">No matches. Try a protocol name, a pillar, or a term.</p>';
  resN.textContent = hits.length ? hits.length + ' results' : '';
}
function openSheet() {
  if (!sheet) return;
  sheet.hidden = false;
  if (scrim) scrim.hidden = false;
  loadIndex().then(() => { input.value = ''; sel = 0; render(); input.focus(); });
}
function closeSheet() {
  if (!sheet || sheet.hidden) return;
  sheet.hidden = true;
  if (msheet?.hidden !== false) scrim.hidden = true;
}
$('#open-search')?.addEventListener('click', e => { e.preventDefault(); openSheet(); });
$('#open-search-m')?.addEventListener('click', openSheet);
$('#bigsearch')?.addEventListener('click', e => { e.preventDefault(); openSheet(); });
input?.addEventListener('input', () => { sel = 0; render(); });
input?.addEventListener('keydown', e => {
  const rows = $$('#res .row');
  if (e.key === 'ArrowDown') { sel = Math.min(sel + 1, rows.length - 1); e.preventDefault(); render(); }
  else if (e.key === 'ArrowUp') { sel = Math.max(sel - 1, 0); e.preventDefault(); render(); }
  else if (e.key === 'Enter' && rows[sel]) { e.preventDefault(); location.href = rows[sel].getAttribute('href'); }
});
document.addEventListener('keydown', e => {
  const typing = /INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName || '');
  if (e.key === '/' && !typing) { e.preventDefault(); openSheet(); }
  if ((e.key === 'k' || e.key === 'K') && (e.ctrlKey || e.metaKey) && !typing) {
    e.preventDefault(); openSheet();
  }
  if (e.key === 'Escape') hideOverlays();
});

/* ---------- contents scroll-spy ---------- */
const toc = $('#toc');
if (toc && 'IntersectionObserver' in window) {
  const spy = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        $$('#toc a').forEach(a =>
          a.classList.toggle('on', a.getAttribute('href') === '#' + en.target.id));
      }
    });
  }, { rootMargin: '-15% 0px -75% 0px' });
  $$('.prose h2[id]').forEach(h => spy.observe(h));
}

/* ---------- heading anchors ---------- */
$$('.prose h2[id]').forEach(h => {
  const a = document.createElement('button');
  a.className = 'anchor-link';
  a.type = 'button';
  a.textContent = '#';
  a.setAttribute('aria-label', 'Copy link to this section');
  a.addEventListener('click', () => {
    const url = location.href.split('#')[0] + '#' + h.id;
    navigator.clipboard?.writeText(url).then(
      () => { a.textContent = 'copied'; setTimeout(() => (a.textContent = '#'), 1400); },
      () => {});
  });
  h.appendChild(a);
});

/* ---------- directory filter ---------- */
const dirFilter = $('#dir-filter');
if (dirFilter) {
  const items = $$('.links li');
  const run = () => {
    const q = norm(dirFilter.value.trim());
    let shown = 0;
    items.forEach(li => {
      const hit = !q || norm(li.dataset.hay || li.textContent).includes(q);
      li.hidden = !hit;
      if (hit) shown++;
    });
    $$('.dsub, .dsec').forEach(sec => {
      const any = [...sec.querySelectorAll('.links li')].some(li => !li.hidden);
      sec.hidden = !any;
    });
    const empty = $('#dir-filter') && $('.empty-dir');
    if (empty) empty.hidden = shown !== 0;
  };
  dirFilter.addEventListener('input', debounce(run, 90));
}

/* ---------- what's possible: pillar filter (enhancement; all shown w/o JS) ---------- */
const posGrid = $('#pos-grid');
if (posGrid) {
  const chips = $$('.pos-chip');
  const cards = $$('.scn');
  const setActive = key => {
    chips.forEach(c => c.setAttribute('aria-pressed', String(c.dataset.pillar === key)));
    cards.forEach(card => {
      const show = key === 'all' ||
        (card.dataset.pillars || '').split(' ').includes(key);
      card.hidden = !show;
    });
  };
  chips.forEach(c => c.addEventListener('click', () => setActive(c.dataset.pillar)));
}

})();
