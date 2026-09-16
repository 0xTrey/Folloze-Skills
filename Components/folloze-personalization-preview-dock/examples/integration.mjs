import {
  renderPersonalizationPreviewDock,
  renderPersonalizationPreviewFragment
} from '../src/index.mjs';
import {
  activeKey,
  analyticsArea,
  config,
  rootClass,
  views
} from './four-view.config.mjs';

export const escapeHtml = value => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#39;');

const renderOptions = {
  views,
  escapeHtml,
  activeKey,
  config,
  rootClass,
  analyticsArea
};

export function buildPreviewDock() {
  return renderPersonalizationPreviewDock(renderOptions);
}

export function buildPreviewDockFragment() {
  return renderPersonalizationPreviewFragment(renderOptions);
}

export function connectPreviewDock(root, applyBoardVariant) {
  if (!(root instanceof Element)) throw new Error('Provide the owning board root element');
  if (typeof applyBoardVariant !== 'function') throw new Error('Provide a board variant function');
  root.addEventListener('folloze:personalization-preview-change', event => {
    applyBoardVariant(event.detail.key, event.detail);
  });
}
