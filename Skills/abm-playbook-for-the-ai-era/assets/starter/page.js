(function (root) {
  if (!root) return;

  const header = root.querySelector('.cp-header');
  const menu = root.querySelector('.cp-menu');
  const transport = root.querySelector('.cp-transport');
  const stage = root.querySelector('.cp-chapter-stage');
  const scenes = [...stage.querySelectorAll('[data-cp-chapter]')];
  const navButtons = [...root.querySelectorAll('header nav [data-cp-jump]')];
  const previous = transport.querySelector('[data-cp-step="-1"]');
  const next = transport.querySelector('[data-cp-step="1"]');
  const progress = transport.querySelector('progress');
  const position = transport.querySelector('[data-cp-position]');
  const assumptions = root.querySelector('.cp-assumptions');
  const mobile = window.matchMedia('(max-width: 900px)');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const initialHash = window.location.hash === '#workflow' ? '#stack' : window.location.hash;
  let index = Math.max(0, scenes.findIndex((scene) => '#' + scene.id === initialHash));
  let frame = 0;
  let wheelTimer;
  let wheelDistance = 0;
  let wheelLocked = false;
  let printing = false;
  let assumptionsWasOpen = false;

  function track(name, text, element) {
    if (typeof flzAnalytic === 'function') {
      flzAnalytic(name, { text, area: root.dataset.cpAnalyticsArea }, element);
    }
  }

  function label(scene) {
    return navButtons.find((button) => button.dataset.cpJump === scene.id)?.textContent.trim() || 'Overview';
  }

  function setCurrent(id) {
    navButtons.forEach((button) => {
      if (button.dataset.cpJump === id) button.setAttribute('aria-current', 'location');
      else button.removeAttribute('aria-current');
    });
  }

  function focusHeading(scene) {
    const heading = scene.querySelector('h1, h2');
    heading.tabIndex = -1;
    heading.focus({ preventScroll: true });
  }

  function show(scene, visible) {
    scene.hidden = !visible;
    scene.inert = !visible;
    if (visible) scene.removeAttribute('aria-hidden');
    else scene.setAttribute('aria-hidden', 'true');
  }

  function renderGuided(focus) {
    const active = scenes[index];
    show(active, true);
    if (focus) focusHeading(active);
    scenes.forEach((scene) => {
      if (scene !== active) show(scene, false);
    });
    active.scrollTop = 0;
    setCurrent(active.id);
    previous.disabled = index === 0;
    previous.textContent = scenes[index - 1] ? '← ' + label(scenes[index - 1]) : 'Previous';
    next.disabled = index === scenes.length - 1;
    next.textContent = scenes[index + 1] ? label(scenes[index + 1]) + ' →' : 'End of playbook';
    position.textContent = label(active) + ' · ' + (index + 1) + ' of ' + scenes.length;
    progress.value = index + 1;
  }

  function syncMode() {
    const guided = !mobile.matches && !printing;
    root.toggleAttribute('data-cp-guided', guided);
    transport.hidden = !guided;
    if (guided) renderGuided(false);
    else scenes.forEach((scene) => show(scene, true));
  }

  function goTo(target, eventName) {
    if (target < 0 || target >= scenes.length) return;
    index = target;
    const scene = scenes[index];
    menu.open = false;
    if (root.hasAttribute('data-cp-guided')) renderGuided(true);
    else {
      focusHeading(scene);
      scene.scrollIntoView({ behavior: reducedMotion.matches ? 'instant' : 'smooth', block: 'start' });
      setCurrent(scene.id);
    }
    track(eventName, label(scene));
  }

  function canScroll(scene, direction) {
    if (direction < 0) return scene.scrollTop > 1;
    return scene.scrollHeight - scene.clientHeight - scene.scrollTop > 1;
  }

  function wheel(event) {
    if (!root.hasAttribute('data-cp-guided') || event.ctrlKey || Math.abs(event.deltaX) > Math.abs(event.deltaY) || !event.deltaY) return;
    const delta = event.deltaMode === 1 ? event.deltaY * 16 : event.deltaY;
    const direction = Math.sign(delta);
    if (!wheelLocked && canScroll(scenes[index], direction)) {
      wheelDistance = 0;
      return;
    }
    if (!wheelLocked && !scenes[index + direction]) return;
    event.preventDefault();
    window.clearTimeout(wheelTimer);
    wheelTimer = window.setTimeout(() => {
      wheelDistance = 0;
      wheelLocked = false;
    }, 190);
    if (wheelLocked) return;
    if (Math.sign(wheelDistance) !== direction) wheelDistance = 0;
    wheelDistance += delta;
    if (Math.abs(wheelDistance) >= 48) {
      wheelLocked = true;
      goTo(index + direction, 'chapter-change');
    }
  }

  function keydown(event) {
    if (!root.hasAttribute('data-cp-guided') || event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey) return;
    if (!root.contains(event.target) && event.target !== document.body) return;
    if (event.target.closest('input, textarea, select, summary, [contenteditable]')) return;
    const keys = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -1, ArrowDown: 1, PageUp: -1, PageDown: 1 };
    const direction = keys[event.key];
    if (!direction) return;
    const horizontal = event.key === 'ArrowLeft' || event.key === 'ArrowRight';
    const active = scenes[index];
    if (!horizontal && canScroll(active, direction)) {
      event.preventDefault();
      const distance = event.key.startsWith('Page') ? active.clientHeight * 0.85 : 48;
      active.scrollBy({ top: direction * distance, behavior: reducedMotion.matches ? 'instant' : 'smooth' });
      return;
    }
    if (!scenes[index + direction]) return;
    event.preventDefault();
    goTo(index + direction, 'chapter-change');
  }

  function updateFlowPosition() {
    frame = 0;
    if (!mobile.matches || printing) return;
    const threshold = header.getBoundingClientRect().bottom + 105;
    let current = 0;
    for (let n = 1; n < scenes.length; n += 1) {
      if (scenes[n].getBoundingClientRect().top > threshold) break;
      current = n;
    }
    index = current;
    setCurrent(scenes[index].id);
  }

  function scheduleFlowUpdate() {
    if (!frame && mobile.matches && !printing) frame = window.requestAnimationFrame(updateFlowPosition);
  }

  async function copyExampleUrl(button) {
    const url = root.querySelector('#' + button.dataset.cpCopyLink).href;
    const preview = button.closest('.cp-preview');
    const status = preview.querySelector('.cp-copy-status');
    const fallback = preview.querySelector('.cp-copy-fallback');
    status.textContent = '';
    fallback.hidden = true;

    try {
      await navigator.clipboard.writeText(url);
    } catch {
      const input = fallback.querySelector('input');
      input.value = url;
      fallback.hidden = false;
      input.focus();
      input.select();
      return;
    }

    status.textContent = 'URL copied.';
  }

  root.addEventListener('click', (event) => {
    const link = event.target.closest('[data-cp-example]');
    if (link) {
      track('cta_click', link.getAttribute('aria-label') || link.textContent.trim(), link);
      return;
    }
    const button = event.target.closest('button');
    if (!button) return;
    if (button.dataset.cpCopyLink) {
      copyExampleUrl(button);
      track('cta_click', button.innerText.trim(), button);
      return;
    }
    if (button.dataset.cpJump) goTo(scenes.findIndex((scene) => scene.id === button.dataset.cpJump), 'anchor-click');
    if (button.dataset.cpStep) goTo(index + Number(button.dataset.cpStep), 'chapter-change');
    if (button.hasAttribute('data-cp-print')) {
      track('pdf-export', 'Export PDF');
      window.print();
    }
  });

  menu.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    menu.open = false;
    menu.querySelector('summary').focus();
  });
  menu.addEventListener('toggle', () => {
    if (menu.open) track('chapter-menu-open', 'Sections');
  });
  stage.addEventListener('wheel', wheel, { passive: false });
  window.addEventListener('keydown', keydown);
  window.addEventListener('scroll', scheduleFlowUpdate, { passive: true, capture: true });
  mobile.addEventListener('change', () => {
    syncMode();
    if (mobile.matches && index && !printing) scenes[index].scrollIntoView({ behavior: 'instant', block: 'start' });
    scheduleFlowUpdate();
  });
  window.addEventListener('beforeprint', () => {
    assumptionsWasOpen = assumptions.open;
    printing = true;
    syncMode();
    assumptions.open = true;
  });
  window.addEventListener('afterprint', () => {
    assumptions.open = assumptionsWasOpen;
    printing = false;
    syncMode();
  });
  if (typeof ResizeObserver === 'function') {
    const resize = new ResizeObserver(() => {
      root.style.setProperty('--cp-jump-offset', Math.ceil(header.getBoundingClientRect().height + 20) + 'px');
      scheduleFlowUpdate();
    });
    resize.observe(header);
  }
  syncMode();
  scheduleFlowUpdate();
})(document.getElementById('abm-era-playbook'));
