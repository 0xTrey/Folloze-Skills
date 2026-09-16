import test from 'node:test';
import assert from 'node:assert/strict';
import {
  COMPONENT_VERSION,
  pickerCss,
  pickerMarkup,
  pickerRuntime,
  renderPersonalizationPreviewDock,
  renderPersonalizationPreviewFragment,
  validatePickerOptions
} from '../src/index.mjs';
import {buildPreviewDock, buildPreviewDockFragment} from '../examples/integration.mjs';

const options = [
  {key: 'industrials', label: 'Industrials', pickerContext: 'Industry view', pickerTrigger: 'Industry changes the message.', pickerSignals: ['industry']},
  {key: 'acme-operations', label: 'Acme Operations', pickerContext: 'Account view', pickerTrigger: 'Account changes the logo.', pickerSignals: ['industry', 'account']},
  {key: 'acme-service', label: 'Acme Service', pickerContext: 'Account + role', pickerTrigger: 'Role changes the message.', pickerSignals: ['industry', 'account', 'role']},
  {key: 'apex-engineering', label: 'Apex Engineering', pickerContext: 'Account + role', pickerTrigger: 'Role changes the resources.', pickerSignals: ['industry', 'account', 'role']}
];
const config = {signalLabel: 'Manual context applied', proofHeadline: 'One URL. Four manually selectable audience views.', signals: [{key:'account',label:'Account',color:'#00a0ff'},{key:'industry',label:'Industry',color:'#11d175'},{key:'role',label:'Role',color:'#ff469e'}]};
const escapeHtml = value => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;');

test('manual picker validates stable, distinct choices', () => {
  assert.equal(validatePickerOptions(options), options);
  assert.throws(() => validatePickerOptions([{...options[0], key: 'same'}, {...options[1], key: 'same'}]), /Duplicate audience key/);
  assert.throws(() => validatePickerOptions([{key: 'one', label: 'Only one'}]), /2 to 6 manual options/);
});

test('markup starts on the requested audience and remains accessible', () => {
  const markup = pickerMarkup(options, escapeHtml, 'apex-engineering', config);
  assert.equal(COMPONENT_VERSION, '1.0.0');
  assert.match(markup, /<nav class="audience-picker" data-component="folloze-personalization-preview-dock" data-component-version="1.0.0" style="--audience-picker-count:4" aria-label="Manual audience preview controls">/);
  assert.match(markup, /data-audience-key="apex-engineering"[^>]*aria-selected="true" data-current="true"/);
  assert.match(markup, /role="tab" tabindex="0" data-audience-key="apex-engineering"/);
  assert.match(markup, /data-picker-counter aria-live="polite">4\/4/);
  assert.match(markup, /Manual context applied/);
  assert.match(markup, /One URL\. Four manually selectable audience views\./);
  assert.match(markup, /URL unchanged/);
  assert.match(markup, /data-picker-trigger-text>Role changes the resources\./);
  assert.match(markup, /data-picker-signal="role" style="--audience-picker-signal:#ff469e"/);
  assert.equal((markup.match(/role="tab"/g) ?? []).length, 4);
  assert.equal((markup.match(/data-picker-toggle=/g) ?? []).length, 2);
  assert.throws(() => pickerMarkup(options, escapeHtml, 'unknown', config), /Unknown active audience key/);
  assert.throws(() => pickerMarkup(options, escapeHtml, 'industrials', {...config, signals:[]}), /one-URL proof/);
  assert.throws(() => pickerMarkup(options, escapeHtml, 'industrials', {...config, signals:[{key:'industry',label:'Industry',color:'red'}]}), /Invalid signal color/);
});

test('style and runtime are rooted and use an explicit selection event', () => {
  const css = pickerCss('.fz-example-demo');
  const runtime = pickerRuntime('.fz-example-demo', 'example audience demo');
  assert.match(css, /\.fz-example-demo \.audience-picker \{[^\n]*position:fixed/);
  assert.match(css, /border-radius:24px/);
  assert.match(css, /grid-template-columns:repeat\(var\(--audience-picker-count\),minmax\(118px,1fr\)\)/);
  assert.match(css, /overflow-x:auto/);
  assert.match(runtime, /audience-preview-change/);
  assert.match(runtime, /folloze:personalization-preview-change/);
  assert.match(runtime, /source: 'manual'/);
  assert.match(runtime, /aria-selected/);
  assert.match(runtime, /is-collapsed/);
  assert.match(runtime, /data-picker-trigger-text/);
  assert.match(runtime, /window\.location\.pathname\.split\('\/items\/'\)\[0\]/);
  assert.ok(runtime.includes(".replace(/\\/$/, '')"));
  assert.match(runtime, /sessionStorage\.setItem\(selectionKey, key\)/);
  assert.match(runtime, /item\.tabIndex = item === control \? 0 : -1/);
  assert.match(runtime, /queueMicrotask\(\(\) => select\(initial, false, true\)\)/);
  assert.match(runtime, /audience-preview-item-open/);
  assert.match(runtime, /folloze:content-item-open/);
  assert.match(runtime, /data-folloze-content-item/);
  assert.match(runtime, /returnScrollKey = selectionKey \+ ':return-scroll'/);
  assert.match(runtime, /window\.scrollTo\(0, Math\.min\(top, max\)\)/);
  assert.match(runtime, /sessionStorage\.removeItem\(returnScrollKey\)/);
  assert.match(runtime, /addEventListener\('popstate', restoreReturnScroll\)/);
  assert.match(runtime, /new MutationObserver\(\(\) => \{/);
  assert.match(runtime, /lastRoute = window\.location\.pathname/);
  assert.doesNotMatch(runtime, /document\.cookie|localStorage|6sense|ipify/i);
});

test('high-level renderers return reusable parts and a self-contained fragment', () => {
  const renderOptions = {
    views: options,
    escapeHtml,
    activeKey: 'industrials',
    config,
    rootClass: '.fz-example-demo',
    analyticsArea: 'manual personalization preview'
  };
  const rendered = renderPersonalizationPreviewDock(renderOptions);
  assert.equal(rendered.componentVersion, COMPONENT_VERSION);
  assert.match(rendered.css, /\.fz-example-demo \.audience-picker/);
  assert.match(rendered.markup, /data-component-version="1.0.0"/);
  assert.match(rendered.runtime, /audience_preview_selected/);
  const fragment = renderPersonalizationPreviewFragment(renderOptions);
  assert.match(fragment, /^<style data-component="folloze-personalization-preview-dock"/);
  assert.match(fragment, /<nav class="audience-picker"/);
  assert.match(fragment, /<script data-component="folloze-personalization-preview-dock"/);
  assert.throws(() => renderPersonalizationPreviewDock({...renderOptions, analyticsArea: ''}), /analytics area/);
});

test('the neutral four-view example compiles without tenant-specific code', () => {
  const rendered = buildPreviewDock();
  assert.match(rendered.markup, /Acme Operations/);
  assert.match(rendered.markup, /Apex Engineering/);
  assert.match(buildPreviewDockFragment(), /One URL\. Four manually selectable audience views\./);
});
