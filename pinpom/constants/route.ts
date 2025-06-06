export interface Route {
  label: string;
  path?: string;
  icon?: string;
  items?: Route[];
};

export const routes: Route[] = [
  {
    label: 'General',
    items: [
      { label: 'Project Overview', path: '/dashboard/project', icon: 'House' },
      { label: 'Table Editor', path: '/dashboard/table-editor', icon: 'Table2' },
      { label: 'SQL Editor', path: '/dashboard/sql-editor', icon: 'SquareTerminal' },
    ]
  },
  {
    label: 'Database',
    items: [
      { label: 'Database', path: '/dashboard/database', icon: 'Database' },
      { label: 'Authentication', path: '/dashboard/authentication', icon: 'Fingerprint' },
      { label: 'Storage', path: '/dashboard/storage', icon: 'Package2' },
    ]
  },
  {
    label: 'Settings',
    items: [
      { label: 'Security Advisor', path: '/advisors/security', icon: 'Wand' },
      { label: 'Reports', path: '/reports', icon: 'ChartNoAxesCombined' },
      { label: 'API Docs', path: '/api-docs', icon: 'FileText' },
    ]
  }
];

export const routes_database: Route[] = [
  {
    label: 'Database management',
    items: [
      { label: 'Schema Visualizer', path: '/dashboard/database/schema-visualizer' },
      { label: 'Tables', path: '/dashboard/database/tables' },
      { label: 'Functions', path: '/dashboard/database/functions' },
      { label: 'Triggers', path: '/dashboard/database/triggers' },
      { label: 'Enumerated Types', path: '/dashboard/database/enumerated-types' },
      { label: 'Indexes', path: '/dashboard/database/indexes' },
      { label: 'Publications', path: '/dashboard/database/publications' },
    ]
  },
  {
    label: 'Access control',
    items: [
      { label: 'Roles', path: '/dashboard/database/roles' },
      { label: 'Policies', path: '/dashboard/database/policies' },
    ]
  },
  {
    label: 'Platform',
    items: [
      { label: 'Backups', path: '/dashboard/database/backups' },
      { label: 'Migrations', path: '/dashboard/database/migrations' },
    ]
  }
]