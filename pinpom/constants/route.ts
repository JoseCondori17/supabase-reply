export interface Route {
  label: string;
  path?: string;
  icon?: string;
  items?: Route[];
};

export const routes = (id: string) => {
  return [
    {
      label: 'General',
      items: [
        { label: 'Project Overview', path: `/dashboard/project/${id}`, icon: 'House' },
        { label: 'Table Editor', path: `/dashboard/project/${id}/editor`, icon: 'Table2' },
        { label: 'SQL Editor', path: `/dashboard/project/${id}/sql`, icon: 'SquareTerminal' },
      ]
    },
    {
      label: 'Database',
      items: [
        { label: 'Database', path: `/dashboard/project/${id}/database/schemas`, icon: 'Database' },
        { label: 'Authentication', path: `/dashboard/project/${id}/auth/users`, icon: 'Fingerprint' },
        { label: 'Storage', path: `/dashboard/project/${id}/storage`, icon: 'Package2' },
      ]
    },
    {
      label: 'Settings',
      items: [
        { label: 'Advisors', path: `/dashboard/project/${id}/advisors/security`, icon: 'Wand' },
        { label: 'Reports', path: `/dashboard/project/${id}/reports`, icon: 'ChartNoAxesCombined' },
        { label: 'API Docs', path: `/dashboard/project/${id}/api`, icon: 'FileText' },
      ]
    }
  ];
}

export const routes_database = (id: string) => {
  return [
    {
      label: 'Database management',
      items: [
        { label: 'Schema Visualizer', path: `/dashboard/project/${id}/database/schema-visualizer` },
        { label: 'Tables', path: `/dashboard/project/${id}/database/tables` },
        { label: 'Functions', path: `/dashboard/project/${id}/database/functions` },
        { label: 'Triggers', path: `/dashboard/project/${id}/database/triggers` },
        { label: 'Enumerated Types', path: `/dashboard/project/${id}/database/enumerated-types` },
        { label: 'Indexes', path: `/dashboard/project/${id}/database/indexes` },
        { label: 'Publications', path: `/dashboard/project/${id}/database/publications` },
      ]
    },
    {
      label: 'Access control',
      items: [
        { label: 'Roles', path: `/dashboard/project/${id}/database/roles` },
        { label: 'Policies', path: `/dashboard/project/${id}/database/policies` },
      ]
    },
    {
      label: 'Platform',
      items: [
        { label: 'Backups', path: `/dashboard/project/${id}/database/backups` },
        { label: 'Migrations', path: `/dashboard/project/${id}/database/migrations` },
      ]
    }
  ]
}

export const route_authentication = (id: string) => {
  return [
    {
      label: 'Manage',
      items: [
        { label: 'Users', path: `/dashboard/auth/user` }
      ]
    },
    {
      label: 'Configuration',
      items: [
        { label: 'Policies', path: `/dashboard/auth/policies` },
        { label: 'Sign In/Providers', path: `/dashboard/auth/providers` },
        { label: 'Sessions', path: `/dashboard/auth/sessions` },
        { label: 'Rate Limits', path: `/dashboard/auth/rate-limits` },
        { label: 'Emails', path: `/dashboard/auth/emails` },
        { label: 'Multi-Factor', path: `/dashboard/auth/mfa` },
        { label: 'URL Configuration', path: `/dashboard/auth/url-configuration` },
        { label: 'Attack Protection', path: `/dashboard/auth/protection` },
      ]
    }
  ]
}

export const route_api_docs = (id: string) => {
  return [
    {
      label: 'Getting started',
      items: [
        { label: 'Introduction', path: `/dashboard/project/${id}/api` },
        { label: 'Authentication', path: `/dashboard/project/${id}/api` },
        { label: 'User Management', path: `/dashboard/project/${id}/api` },
      ],
    },
    {
      label: 'Tables and views',
      items: [
        { label: 'Introduction', path: `/dashboard/project/${id}/api` },
      ]
    },
    {
      label: 'Stored procedures',
      items: [
        { label: 'Introduction', path: `/dashboard/project/${id}/api` },
      ]
    }
  ]
}