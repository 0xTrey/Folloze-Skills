export const rootClass = '.fz-example-experience';
export const activeKey = 'industrials';
export const analyticsArea = 'manual personalization preview';

export const config = {
  signalLabel: 'Manual context applied',
  proofHeadline: 'One URL. Four manually selectable audience views.',
  signals: [
    {key: 'account', label: 'Account', color: '#00a0ff'},
    {key: 'industry', label: 'Industry', color: '#11d175'},
    {key: 'role', label: 'Role', color: '#ff469e'}
  ]
};

export const views = [
  {
    key: 'industrials',
    label: 'Industrials',
    pickerContext: 'Industry view',
    pickerTrigger: 'Industry changes the hero, message, CTA, and resources.',
    pickerSignals: ['industry']
  },
  {
    key: 'acme-operations',
    label: 'Acme Operations',
    pickerContext: 'Account view',
    pickerTrigger: 'Account adds the logo, account story, CTA, and proof.',
    pickerSignals: ['industry', 'account']
  },
  {
    key: 'acme-service',
    label: 'Acme Service',
    pickerContext: 'Account + role',
    pickerTrigger: 'Role changes the problem, value path, CTA, and resources.',
    pickerSignals: ['industry', 'account', 'role']
  },
  {
    key: 'apex-engineering',
    label: 'Apex Engineering',
    pickerContext: 'Account + role',
    pickerTrigger: 'Selected account and role change the complete page story.',
    pickerSignals: ['industry', 'account', 'role']
  }
];
