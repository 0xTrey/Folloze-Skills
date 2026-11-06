(function (root) {
  if (!root) return;

  const form = root.querySelector('[data-cp-calculator]');
  if (!form) return;
  const fields = [...form.querySelectorAll('input')];
  const results = root.querySelector('[data-cp-results]');
  const validation = results.querySelector('[data-cp-validation]');
  const announcement = results.querySelector('[data-cp-announcement]');
  const bar = root.querySelector('[data-cp-bar]');
  const segments = [...bar.querySelectorAll('[data-bar]')];
  const outputs = [...results.querySelectorAll('[data-output]')];
  const formula = results.querySelector('[data-cp-formula]');
  const headlineTarget = root.querySelector('[data-cp-headline-target]');
  const engagementLabel = results.querySelector('[data-cp-rate=engagement]');
  const opportunityLabel = results.querySelector('[data-cp-rate=opportunity]');
  const number = new Intl.NumberFormat('en-US');
  const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: root.dataset.cpCurrency, minimumFractionDigits: 0, maximumFractionDigits: 2 });
  const compactMoney = new Intl.NumberFormat('en-US', { style: 'currency', currency: root.dataset.cpCurrency, notation: 'compact', maximumFractionDigits: 2 });
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const winRate = Number(root.dataset.cpWinRate) / 100;
  let lastAccounts;
  let barPulse;

  function fieldValue(field) {
    const value = field.valueAsNumber;
    const percentage = field.name.endsWith('-rate');
    let error = '';
    if (!Number.isFinite(value)) error = 'Enter a number.';
    else if (percentage && (value <= 0 || value > 100)) error = 'Enter a rate greater than 0% and up to 100%.';
    else if (!percentage && value <= 0) error = 'Enter an amount greater than 0.';
    field.setAttribute('aria-invalid', String(Boolean(error)));
    form.querySelector('[data-error="' + field.name + '"]').textContent = error;
    return error ? NaN : value;
  }

  function clearOutputs(message) {
    outputs.forEach((node) => { node.textContent = 'N/A'; });
    segments.forEach((node) => { node.style.width = '0%'; });
    formula.textContent = '';
    validation.textContent = message;
    announcement.textContent = message;
  }

  function update() {
    const [target, size, engagementPercent, opportunityPercent] = fields.map(fieldValue);
    headlineTarget.textContent = Number.isFinite(target) ? compactMoney.format(target) : 'your target amount';
    engagementLabel.textContent = Number.isFinite(engagementPercent) ? number.format(engagementPercent) + '% engage' : 'Engagement rate';
    opportunityLabel.textContent = Number.isFinite(opportunityPercent) ? number.format(opportunityPercent) + '% become opportunities' : 'Opportunity rate';
    if ([target, size, engagementPercent, opportunityPercent].some(Number.isNaN)) {
      clearOutputs('Enter valid assumptions to calculate the account model.');
      return;
    }

    const opportunities = target / size;
    const engaged = opportunities / (opportunityPercent / 100);
    const accounts = engaged / (engagementPercent / 100);
    if (accounts > Number.MAX_SAFE_INTEGER || accounts <= 0) {
      clearOutputs('Use a smaller target or higher conversion rates to model this scenario.');
      return;
    }
    const won = opportunities * winRate;
    const values = [Math.ceil(accounts), Math.ceil(engaged), Math.ceil(opportunities), Math.round(won)];
    outputs.forEach((node, index) => { node.textContent = number.format(values[index]); });
    validation.textContent = '';
    formula.textContent = money.format(target) + ' ÷ (' + money.format(size) + ' × ' + number.format(engagementPercent) + '% × ' + number.format(opportunityPercent) + '%) = ' + number.format(values[0]) + ' target accounts';
    announcement.textContent = number.format(values[0]) + ' target accounts, ' + number.format(values[1]) + ' engaged accounts, ' + number.format(values[2]) + ' opportunities, and ' + number.format(values[3]) + ' illustrative closed won.';

    const portions = [accounts - engaged, engaged - opportunities, opportunities - won, won];
    segments.forEach((node, index) => { node.style.width = (100 * portions[index] / accounts) + '%'; });
    if (lastAccounts !== undefined && lastAccounts !== values[0] && !reducedMotion.matches && typeof bar.animate === 'function') {
      if (barPulse) barPulse.cancel();
      barPulse = bar.animate([{ opacity: 0.55 }, { opacity: 1 }], { duration: 350, easing: 'ease-out' });
    }
    lastAccounts = values[0];
  }

  function track(name, text) {
    if (typeof flzAnalytic === 'function') {
      flzAnalytic(name, { text, area: root.dataset.cpAnalyticsArea });
    }
  }

  form.addEventListener('submit', (event) => { event.preventDefault(); });
  form.addEventListener('input', update);
  form.addEventListener('change', (event) => {
    if (event.target.matches('input') && event.target.getAttribute('aria-invalid') === 'false') {
      track('pipeline-assumption-change', event.target.name);
    }
  });
  root.querySelector('.cp-assumptions').addEventListener('toggle', (event) => {
    if (event.target.open) track('calculator-open', 'Edit planning assumptions');
  });
  update();

  const signal = root.querySelector('[data-cp-feedback]');
  if (signal && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      if (!entries.some((entry) => entry.isIntersecting)) return;
      signal.classList.add('cp-signal-enter');
      observer.disconnect();
    }, { threshold: 0.3 });
    observer.observe(signal);
  }
})(document.getElementById('abm-era-playbook'));
