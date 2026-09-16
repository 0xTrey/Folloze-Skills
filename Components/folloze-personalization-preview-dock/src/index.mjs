const ROOT_TOKEN = "__AUDIENCE_ROOT__";
const FOLLOZE_LOGO = "https://cdn.prod.website-files.com/6464087fdf877a12a8bd4cd6/6464087fdf877a12a8bd4d26_folloze-logo.svg";
const DEFAULT_SIGNAL_COLORS = ["#00a0ff", "#11d175", "#ff469e", "#f6c344", "#8b5cf6", "#20c997"];
export const COMPONENT_VERSION = "1.0.0";

export function validatePickerOptions(options) {
  if (!Array.isArray(options) || options.length < 2 || options.length > 6) {
    throw new Error("Audience picker requires 2 to 6 manual options");
  }
  const keys = new Set();
  for (const option of options) {
    if (!/^[a-z][a-z0-9-]*$/.test(option.key) || !option.label?.trim() ||
        !option.pickerContext?.trim() || !option.pickerTrigger?.trim() ||
        !Array.isArray(option.pickerSignals)) {
      throw new Error("Every audience requires a key, label, context, trigger, and signal list");
    }
    if (keys.has(option.key)) throw new Error(`Duplicate audience key: ${option.key}`);
    keys.add(option.key);
  }
  return options;
}

function validatePickerConfig(config, options) {
  if (!config || !config.proofHeadline?.trim() || !config.signalLabel?.trim() ||
      !Array.isArray(config.signals) || config.signals.length < 1) {
    throw new Error("Picker needs one-URL proof and named context signals");
  }
  const signalKeys = new Set();
  for (const signal of config.signals) {
    if (!/^[a-z][a-z0-9-]*$/.test(signal.key) || !signal.label?.trim() || signalKeys.has(signal.key)) {
      throw new Error("Picker signals need unique keys and visible labels");
    }
    if (signal.color && !/^#[0-9a-f]{6}$/i.test(signal.color)) {
      throw new Error(`Invalid signal color for ${signal.key}`);
    }
    signalKeys.add(signal.key);
  }
  for (const option of options) {
    if (option.pickerSignals.some(key => !signalKeys.has(key))) {
      throw new Error(`Unknown context signal for ${option.key}`);
    }
  }
}

export function pickerMarkup(options, escapeHtml, activeKey = options[0]?.key, config) {
  validatePickerOptions(options);
  validatePickerConfig(config, options);
  const activeIndex = options.findIndex(option => option.key === activeKey);
  if (activeIndex < 0) throw new Error(`Unknown active audience key: ${activeKey}`);
  const activeOption = options[activeIndex];
  const buttons = options.map(option =>
    `<button class="audience-picker__option" type="button" role="tab" tabindex="${option.key === activeKey ? '0' : '-1'}" data-audience-key="${escapeHtml(option.key)}" data-picker-trigger="${escapeHtml(option.pickerTrigger)}" data-picker-signals="${escapeHtml(option.pickerSignals.join(','))}" aria-selected="${option.key === activeKey}"${option.key === activeKey ? ' data-current="true"' : ""}><b>${escapeHtml(option.label)}</b><small>${escapeHtml(option.pickerContext)}</small></button>`
  ).join("");
  const signals = config.signals.map((signal, index) =>
    `<span class="audience-picker__signal${activeOption.pickerSignals.includes(signal.key) ? ' is-active' : ''}" data-picker-signal="${escapeHtml(signal.key)}" style="--audience-picker-signal:${escapeHtml(signal.color || DEFAULT_SIGNAL_COLORS[index % DEFAULT_SIGNAL_COLORS.length])}">${escapeHtml(signal.label)}</span>`
  ).join("");
  const lockup = `<span class="audience-picker__lockup"><img src="${FOLLOZE_LOGO}" alt="Folloze"></span>`;
  const downArrow = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m7 9 5 5 5-5"/></svg>';
  const upArrow = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m7 15 5-5 5 5"/></svg>';
  return `<nav class="audience-picker" data-component="folloze-personalization-preview-dock" data-component-version="${COMPONENT_VERSION}" style="--audience-picker-count:${options.length}" aria-label="Manual audience preview controls">
  <div class="audience-picker__collapsed">${lockup}<strong>View controls</strong><button class="audience-picker__collapse" type="button" data-picker-toggle="expand" aria-label="Expand view controls" aria-expanded="false">${upArrow}</button></div>
  <div class="audience-picker__primary"><div class="audience-picker__heading">${lockup}<div><strong>View as</strong><span>Personalization preview</span></div></div><div class="audience-picker__options" role="tablist" aria-label="Choose an audience view">${buttons}</div><div class="audience-picker__counter" data-picker-counter aria-live="polite">${activeIndex + 1}/${options.length}</div><button class="audience-picker__collapse" type="button" data-picker-toggle="collapse" aria-label="Collapse view controls" aria-expanded="true">${downArrow}</button></div>
  <div class="audience-picker__secondary"><div class="audience-picker__signals" aria-label="Manual context applied"><span class="audience-picker__signal-label">${escapeHtml(config.signalLabel)}</span>${signals}</div><div class="audience-picker__proof"><div class="audience-picker__proof-copy"><div><strong>${escapeHtml(config.proofHeadline)}</strong><small data-picker-trigger-text>${escapeHtml(activeOption.pickerTrigger)}</small></div></div><span class="audience-picker__url-status">URL unchanged</span></div></div>
  <span class="audience-picker__sr-only" data-audience-status aria-live="polite">Showing ${escapeHtml(activeOption.label)}</span>
</nav>`;
}

export function pickerCss(rootClass) {
  if (!/^\.[a-z][a-z0-9-]*$/.test(rootClass)) throw new Error("Use a unique root class");
  return `
${ROOT_TOKEN} .audience-picker { --audience-picker-accent:#5b5bff; --audience-picker-blue:#00a0ff; --audience-picker-pink:#ff469e; --audience-picker-green:#11d175; position:fixed; z-index:80; right:18px; bottom:18px; left:18px; width:min(calc(100% - 36px),1180px); margin:0 auto; border:1px solid rgba(91,91,255,.58); border-radius:24px; background:radial-gradient(circle at 8% 0%,rgba(91,91,255,.24),transparent 30%),linear-gradient(135deg,rgba(16,25,64,.98),rgba(7,13,37,.98)); color:#fff; box-shadow:0 22px 70px rgba(10,18,48,.38),0 8px 24px rgba(91,91,255,.16); backdrop-filter:blur(18px); transition:width .28s ease; font-family:Arial,sans-serif; line-height:1.3; box-sizing:border-box; }
${ROOT_TOKEN} .audience-picker::before { content:""; position:absolute; top:-1px; right:28px; left:28px; height:1px; background:linear-gradient(90deg,transparent,var(--audience-picker-accent),var(--audience-picker-blue),var(--audience-picker-pink),transparent); pointer-events:none; }
${ROOT_TOKEN} .audience-picker.is-collapsed { right:18px; left:auto; width:auto; }
${ROOT_TOKEN} .audience-picker.is-collapsed .audience-picker__primary,${ROOT_TOKEN} .audience-picker.is-collapsed .audience-picker__secondary { display:none; }
${ROOT_TOKEN} .audience-picker.is-collapsed .audience-picker__collapsed { display:flex; }
${ROOT_TOKEN} .audience-picker__collapsed { display:none; align-items:center; gap:10px; min-height:54px; padding:8px 10px 8px 16px; }
${ROOT_TOKEN} .audience-picker__collapsed strong { font-size:11px; letter-spacing:.04em; text-transform:uppercase; }
${ROOT_TOKEN} .audience-picker__lockup { display:inline-flex; align-items:center; flex:0 0 auto; min-height:30px; padding:5px 8px; border-radius:9px; background:#fff; box-shadow:0 5px 16px rgba(0,0,0,.16); }
${ROOT_TOKEN} .audience-picker__lockup img { display:block; width:78px; height:auto; }
${ROOT_TOKEN} .audience-picker__collapsed .audience-picker__lockup { min-height:28px; padding:4px 7px; }
${ROOT_TOKEN} .audience-picker__collapsed .audience-picker__lockup img { width:70px; }
${ROOT_TOKEN} .audience-picker__primary { display:grid; grid-template-columns:210px minmax(0,1fr) auto auto; align-items:center; gap:14px; padding:12px 14px 9px; }
${ROOT_TOKEN} .audience-picker__heading { display:flex; align-items:center; gap:10px; }
${ROOT_TOKEN} .audience-picker__heading strong { display:block; font-size:12px; letter-spacing:.07em; text-transform:uppercase; }
${ROOT_TOKEN} .audience-picker__heading > div > span { display:block; color:rgba(255,255,255,.58); font:10px/1.3 ui-monospace,monospace; }
${ROOT_TOKEN} .audience-picker__options { display:grid; grid-template-columns:repeat(var(--audience-picker-count),minmax(118px,1fr)); gap:8px; }
${ROOT_TOKEN} .audience-picker__option { min-height:48px; border:1px solid rgba(255,255,255,.12); border-radius:13px; padding:8px 12px; background:rgba(255,255,255,.055); color:rgba(255,255,255,.72); cursor:pointer; text-align:left; transition:transform .22s ease,color .22s ease,background .22s ease,border-color .22s ease; font-family:inherit; }
${ROOT_TOKEN} .audience-picker__option:hover { transform:translateY(-2px); color:#fff; border-color:rgba(91,91,255,.72); background:rgba(91,91,255,.12); }
${ROOT_TOKEN} .audience-picker__option[aria-selected="true"] { color:#fff; background:var(--audience-picker-accent); border-color:rgba(255,255,255,.38); box-shadow:0 8px 26px rgba(91,91,255,.36); }
${ROOT_TOKEN} .audience-picker__option b { display:block; font-size:12px; }
${ROOT_TOKEN} .audience-picker__option small { display:block; margin-top:2px; font-size:10px; opacity:.7; }
${ROOT_TOKEN} .audience-picker__counter { display:grid; place-items:center; width:42px; height:42px; border:1px solid rgba(91,91,255,.56); border-radius:50%; color:var(--audience-picker-blue); background:rgba(91,91,255,.08); font:12px ui-monospace,monospace; }
${ROOT_TOKEN} .audience-picker__collapse { display:inline-grid; place-items:center; width:42px; height:42px; border:1px solid rgba(255,255,255,.14); border-radius:50%; background:rgba(255,255,255,.06); color:#fff; cursor:pointer; }
${ROOT_TOKEN} .audience-picker__collapse:hover { border-color:rgba(91,91,255,.7); background:rgba(91,91,255,.24); transform:translateY(-1px); }
${ROOT_TOKEN} .audience-picker__collapse:focus-visible,${ROOT_TOKEN} .audience-picker__option:focus-visible { outline:3px solid rgba(0,160,255,.65); outline-offset:2px; }
${ROOT_TOKEN} .audience-picker__collapse svg { width:17px; height:17px; }
${ROOT_TOKEN} .audience-picker__secondary { display:grid; grid-template-columns:max-content minmax(0,1fr); align-items:center; gap:12px; padding:0 14px 9px; }
${ROOT_TOKEN} .audience-picker__signals { display:flex; align-items:center; gap:8px; min-width:0; overflow-x:auto; scrollbar-width:none; }
${ROOT_TOKEN} .audience-picker__signals::-webkit-scrollbar,${ROOT_TOKEN} .audience-picker__options::-webkit-scrollbar { display:none; }
${ROOT_TOKEN} .audience-picker__signal-label { margin-right:3px; color:rgba(255,255,255,.48); font:10px ui-monospace,monospace; text-transform:uppercase; letter-spacing:.1em; white-space:nowrap; }
${ROOT_TOKEN} .audience-picker__signal { display:inline-flex; align-items:center; gap:7px; flex:0 0 auto; min-height:28px; padding:5px 10px; border:1px solid rgba(255,255,255,.1); border-radius:999px; color:rgba(251,253,249,.48); font-size:10px; box-sizing:border-box; }
${ROOT_TOKEN} .audience-picker__signal::before { content:""; width:6px; height:6px; border-radius:50%; background:currentColor; }
${ROOT_TOKEN} .audience-picker__signal.is-active { color:#fff; background:rgba(91,91,255,.12); border-color:rgba(91,91,255,.46); }
${ROOT_TOKEN} .audience-picker__signal.is-active::before { background:var(--audience-picker-signal); }
${ROOT_TOKEN} .audience-picker__proof { display:flex; align-items:center; justify-content:space-between; gap:16px; min-height:32px; padding:4px 8px 4px 11px; border:1px solid rgba(255,255,255,.1); border-radius:12px; background:rgba(255,255,255,.045); }
${ROOT_TOKEN} .audience-picker__proof-copy { display:flex; align-items:center; gap:10px; min-width:0; }
${ROOT_TOKEN} .audience-picker__proof-copy::before { content:""; flex:0 0 auto; width:3px; height:22px; border-radius:999px; background:linear-gradient(var(--audience-picker-blue),var(--audience-picker-accent),var(--audience-picker-pink)); }
${ROOT_TOKEN} .audience-picker__proof strong { display:block; color:rgba(255,255,255,.94); font-size:12px; line-height:1.25; }
${ROOT_TOKEN} .audience-picker__proof small { display:block; color:rgba(255,255,255,.5); font:9px/1.2 ui-monospace,monospace; }
${ROOT_TOKEN} .audience-picker__url-status { display:inline-flex; align-items:center; flex:0 0 auto; gap:7px; padding:6px 9px; border:1px solid rgba(0,160,255,.26); border-radius:999px; color:#a9ddff; background:rgba(0,160,255,.08); font:700 9px/1 ui-monospace,monospace; letter-spacing:.07em; text-transform:uppercase; white-space:nowrap; }
${ROOT_TOKEN} .audience-picker__url-status::before { content:""; width:6px; height:6px; border-radius:50%; background:var(--audience-picker-green); box-shadow:0 0 0 3px rgba(17,209,117,.12); }
${ROOT_TOKEN} .audience-picker__sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0; }
@media (max-width:1060px) { ${ROOT_TOKEN} .audience-picker__primary { grid-template-columns:170px minmax(0,1fr) auto auto; gap:10px; } ${ROOT_TOKEN} .audience-picker__secondary { grid-template-columns:max-content minmax(0,1fr); gap:10px; } ${ROOT_TOKEN} .audience-picker__proof small { display:none; } ${ROOT_TOKEN} .audience-picker__lockup img { width:66px; } ${ROOT_TOKEN} .audience-picker__option small { display:none; } }
@media (max-width:760px) { ${ROOT_TOKEN} .audience-picker { right:8px; bottom:8px; left:8px; width:calc(100% - 16px); border-radius:20px; } ${ROOT_TOKEN} .audience-picker.is-collapsed { right:8px; left:auto; } ${ROOT_TOKEN} .audience-picker__primary { grid-template-columns:1fr auto auto; padding:10px; } ${ROOT_TOKEN} .audience-picker__heading { grid-column:1; } ${ROOT_TOKEN} .audience-picker__heading > div > span { display:none; } ${ROOT_TOKEN} .audience-picker__lockup img { width:64px; } ${ROOT_TOKEN} .audience-picker__counter { grid-column:2; grid-row:1; } ${ROOT_TOKEN} .audience-picker__primary > .audience-picker__collapse { grid-column:3; grid-row:1; } ${ROOT_TOKEN} .audience-picker__options { grid-column:1/-1; grid-row:2; grid-template-columns:repeat(var(--audience-picker-count),minmax(118px,1fr)); overflow-x:auto; scrollbar-width:none; } ${ROOT_TOKEN} .audience-picker__option { min-height:44px; } ${ROOT_TOKEN} .audience-picker__secondary { display:block; padding:0 10px 10px; } ${ROOT_TOKEN} .audience-picker__signals { padding-bottom:8px; } ${ROOT_TOKEN} .audience-picker__proof { min-height:50px; } ${ROOT_TOKEN} .audience-picker__proof strong { font-size:11px; } ${ROOT_TOKEN} .audience-picker__proof small { display:block; } ${ROOT_TOKEN} .audience-picker__url-status { display:none; } }
@media (prefers-reduced-motion:reduce) { ${ROOT_TOKEN} .audience-picker,${ROOT_TOKEN} .audience-picker__option { transition:none; } }
`.replaceAll(ROOT_TOKEN, rootClass);
}

export function pickerRuntime(rootClass, area) {
  if (!/^\.[a-z][a-z0-9-]*$/.test(rootClass)) throw new Error("Use a unique root class");
  return `
(() => {
  const root = document.querySelector(${JSON.stringify(rootClass)});
  if (!root) return;
  const dock = root.querySelector('.audience-picker');
  const controls = [...dock.querySelectorAll('.audience-picker__option')];
  const status = dock.querySelector('[data-audience-status]');
  const counter = dock.querySelector('[data-picker-counter]');
  const triggerText = dock.querySelector('[data-picker-trigger-text]');
  const signals = [...dock.querySelectorAll('[data-picker-signal]')];
  const selectionKey = 'audience-preview:' + ${JSON.stringify(rootClass)} + ':' + window.location.pathname.split('/items/')[0].replace(/\\\/$/, '');
  const returnScrollKey = selectionKey + ':return-scroll';
  function rememberReturnScroll() {
    try {
      const top = document.scrollingElement?.scrollTop ?? window.scrollY;
      window.sessionStorage.setItem(returnScrollKey, String(Math.max(0, Math.round(top))));
    } catch { /* The content viewer still works without browser storage. */ }
  }
  function restoreReturnScroll() {
    if (window.location.pathname.includes('/items/')) return;
    let saved;
    try { saved = window.sessionStorage.getItem(returnScrollKey); }
    catch { return; }
    if (saved === null) return;
    const top = Number(saved);
    if (!Number.isSafeInteger(top) || top < 0) return;
    const restore = () => {
      const scroller = document.scrollingElement || document.documentElement;
      const max = Math.max(0, scroller.scrollHeight - window.innerHeight);
      window.scrollTo(0, Math.min(top, max));
      try { window.sessionStorage.removeItem(returnScrollKey); }
      catch { /* Scroll return is best-effort when storage is unavailable. */ }
    };
    const schedule = () => window.requestAnimationFrame(() => window.requestAnimationFrame(restore));
    if (document.readyState === 'complete') schedule();
    else window.addEventListener('load', schedule, {once: true});
  }
  function savedSelection() {
    try { return window.sessionStorage.getItem(selectionKey); }
    catch { return null; }
  }
  function rememberSelection(key) {
    try { window.sessionStorage.setItem(selectionKey, key); }
    catch { /* Picker still works when browser storage is unavailable. */ }
  }
  function select(control, track = true, force = false) {
    if (!force && control.getAttribute('aria-selected') === 'true') return;
    controls.forEach(item => {
      item.setAttribute('aria-selected', String(item === control));
      item.tabIndex = item === control ? 0 : -1;
      if (item === control) item.dataset.current = 'true';
      else delete item.dataset.current;
    });
    const label = control.querySelector('b').textContent.trim();
    const activeSignals = control.dataset.pickerSignals.split(',').filter(Boolean);
    signals.forEach(signal => signal.classList.toggle('is-active', activeSignals.includes(signal.dataset.pickerSignal)));
    triggerText.textContent = control.dataset.pickerTrigger;
    counter.textContent = String(controls.indexOf(control) + 1) + '/' + controls.length;
    status.textContent = 'Showing ' + label;
    rememberSelection(control.dataset.audienceKey);
    const detail = {key: control.dataset.audienceKey, label, signals: activeSignals, trigger: control.dataset.pickerTrigger, source: 'manual', componentVersion: ${JSON.stringify(COMPONENT_VERSION)}};
    root.dispatchEvent(new CustomEvent('folloze:personalization-preview-change', {detail}));
    root.dispatchEvent(new CustomEvent('audience-preview-change', {detail}));
    if (track && typeof flzAnalytic === 'function') flzAnalytic('audience_preview_selected', {text: label, area: ${JSON.stringify(area)}, audience: control.dataset.audienceKey}, control);
  }
  controls.forEach((control, index) => {
    control.addEventListener('click', () => select(control));
    control.addEventListener('keydown', event => {
      let next = index;
      if (event.key === 'ArrowRight') next = (index + 1) % controls.length;
      else if (event.key === 'ArrowLeft') next = (index - 1 + controls.length) % controls.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = controls.length - 1;
      else return;
      event.preventDefault();
      controls[next].focus();
      select(controls[next]);
    });
  });
  const collapse = dock.querySelector('[data-picker-toggle="collapse"]');
  const expand = dock.querySelector('[data-picker-toggle="expand"]');
  collapse.addEventListener('click', () => { dock.classList.add('is-collapsed'); collapse.setAttribute('aria-expanded', 'false'); expand.setAttribute('aria-expanded', 'false'); expand.focus(); });
  expand.addEventListener('click', () => { dock.classList.remove('is-collapsed'); collapse.setAttribute('aria-expanded', 'true'); expand.setAttribute('aria-expanded', 'true'); collapse.focus(); });
  root.addEventListener('folloze:content-item-open', rememberReturnScroll);
  root.addEventListener('audience-preview-item-open', rememberReturnScroll);
  root.addEventListener('click', event => {
    if (event.target instanceof Element && event.target.closest('[data-folloze-content-item]')) rememberReturnScroll();
  });
  window.addEventListener('popstate', restoreReturnScroll);
  window.addEventListener('pageshow', restoreReturnScroll);
  let lastRoute = window.location.pathname;
  new MutationObserver(() => {
    if (window.location.pathname === lastRoute) return;
    lastRoute = window.location.pathname;
    restoreReturnScroll();
  }).observe(document.body, {childList: true, subtree: true});
  const restored = controls.find(control => control.dataset.audienceKey === savedSelection());
  const initial = restored || controls.find(control => control.getAttribute('aria-selected') === 'true') || controls[0];
  queueMicrotask(() => select(initial, false, true));
  restoreReturnScroll();
})();`;
}

export function renderPersonalizationPreviewDock({views, escapeHtml, activeKey, config, rootClass, analyticsArea}) {
  if (typeof escapeHtml !== "function") throw new Error("Provide an HTML escaping function");
  if (!analyticsArea?.trim()) throw new Error("Provide an analytics area");
  return {
    componentVersion: COMPONENT_VERSION,
    css: pickerCss(rootClass),
    markup: pickerMarkup(views, escapeHtml, activeKey, config),
    runtime: pickerRuntime(rootClass, analyticsArea)
  };
}

export function renderPersonalizationPreviewFragment(options) {
  const rendered = renderPersonalizationPreviewDock(options);
  const safeRuntime = rendered.runtime.replaceAll("</script", "<\\/script");
  return `<style data-component="folloze-personalization-preview-dock" data-component-version="${rendered.componentVersion}">${rendered.css}</style>\n${rendered.markup}\n<script data-component="folloze-personalization-preview-dock" data-component-version="${rendered.componentVersion}">${safeRuntime}</script>`;
}
