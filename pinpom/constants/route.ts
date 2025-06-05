import type { LucideIcon } from 'lucide-react';

export interface Route {
  path: string;
  label: string;
  icon: string;
}

export interface RouteGroup {
  label: string;
  routes: Route[];
}

export const routes: RouteGroup[] = [
  {
    label: 'General',
    routes: [
      { path: '/project', label: 'Project Overview', icon: 'House' },
      { path: '/table-editor', label: 'Table Editor', icon: 'Table2' },
      { path: '/sql-editor', label: 'SQL Editor', icon: 'SquareTerminal' },
    ]
  },
  {
    label: 'Database',
    routes: [
      { path: '/database', label: 'Database', icon: 'Database' },
      { path: '/authentication', label: 'Authentication', icon: 'Fingerprint' },
      { path: '/storage', label: 'Storage', icon: 'Package2' },
    ]
  },
  {
    label: 'Settings',
    routes: [
      { path: '/advisors/security', label: 'Security Advisor', icon: 'Wand' },
      { path: '/reports', label: 'Reports', icon: 'ChartNoAxesCombined' },
      { path: '/api-docs', label: 'API Docs', icon: 'FileText' },
    ]
  }
];