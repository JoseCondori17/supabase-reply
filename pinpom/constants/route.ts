
export interface Route {
  label: string;
  url: string;
  icon?: string;
  items?: Route[];
};

export const routes = (id: string) => {
  return [
    {
      label: 'General',
      url: `/dashboard/project/${id}`,
      items: [
        { label: 'Project Overview', url: `/dashboard/project/${id}`, icon: 'House' },
        { label: 'Table Editor', url: `/dashboard/project/${id}/editor`, icon: 'Table2' },
        { label: 'SQL Editor', url: `/dashboard/project/${id}/sql`, icon: 'SquareTerminal' },
      ]
    },
    {
      label: 'Database',
      url: `/dashboard/project/${id}/database/schemas`,
      items: [
        { label: 'Database', url: `/dashboard/project/${id}/database/schemas`, icon: 'Database' },
        { label: 'Authentication', url: `/dashboard/project/${id}/auth/users`, icon: 'Fingerprint' },
        { label: 'Storage', url: `/dashboard/project/${id}/storage`, icon: 'Package2' },
      ]
    },
    {
      label: 'Settings',
      url: `/dashboard/project/${id}/advisors/security`,
      items: [
        { label: 'Advisors', url: `/dashboard/project/${id}/advisors/security`, icon: 'Wand' },
        { label: 'Reports', url: `/dashboard/project/${id}/reports`, icon: 'ChartNoAxesCombined' },
        { label: 'API Docs', url: `/dashboard/project/${id}/api`, icon: 'FileText' },
      ]
    }
  ];
}

export const routes_database = (id: string) => {
  return [
    {
      label: 'Database management',
      url: `/dashboard/project/${id}/database/schemas`,
      items: [
        { label: 'Schema Visualizer', url: `/dashboard/project/${id}/database/schemas` },
        { label: 'Tables', url: `/dashboard/project/${id}/database/tables` },
        { label: 'Functions', url: `/dashboard/project/${id}/database/functions` },
        { label: 'Triggers', url: `/dashboard/project/${id}/database/triggers` },
        { label: 'Enumerated Types', url: `/dashboard/project/${id}/database/enumerated-types` },
        { label: 'Indexes', url: `/dashboard/project/${id}/database/indexes` },
        { label: 'Publications', url: `/dashboard/project/${id}/database/publications` },
      ]
    },
    {
      label: 'Access control',
      url: `/dashboard/project/${id}/database/roles`,
      items: [
        { label: 'Roles', url: `/dashboard/project/${id}/database/roles` },
        { label: 'Policies', url: `/dashboard/project/${id}/database/policies` },
      ]
    },
    {
      label: 'Platform',
      url: `/dashboard/project/${id}/database/backups`,
      items: [
        { label: 'Backups', url: `/dashboard/project/${id}/database/backups` },
        { label: 'Migrations', url: `/dashboard/project/${id}/database/migrations` },
      ]
    }
  ]
}

export const route_authentication = (id: string) => {
  return [
    {
      label: 'Manage',
      url: `/dashboard/auth/user`,
      items: [
        { label: 'Users', url: `/dashboard/auth/user` }
      ]
    },
    {
      label: 'Configuration',
      url: '',
      items: [
        { label: 'Policies', url: `/dashboard/auth/policies` },
        { label: 'Sign In/Providers', url: `/dashboard/auth/providers` },
        { label: 'Sessions', url: `/dashboard/auth/sessions` },
        { label: 'Rate Limits', url: `/dashboard/auth/rate-limits` },
        { label: 'Emails', url: `/dashboard/auth/emails` },
        { label: 'Multi-Factor', url: `/dashboard/auth/mfa` },
        { label: 'URL Configuration', url: `/dashboard/auth/url-configuration` },
        { label: 'Attack Protection', url: `/dashboard/auth/protection` },
      ]
    }
  ]
}

export const route_api_docs = (id: string) => {
  return [
    {
      label: 'Getting started',
      url: '',
      items: [
        { label: 'Introduction', url: `/dashboard/project/${id}/api` },
        { label: 'Authentication', url: `/dashboard/project/${id}/api` },
        { label: 'User Management', url: `/dashboard/project/${id}/api` },
      ],
    },
    {
      label: 'Tables and views',
      url: '',
      items: [
        { label: 'Introduction', url: `/dashboard/project/${id}/api` },
      ]
    },
    {
      label: 'Stored procedures',
      url: '',
      items: [
        { label: 'Introduction', url: `/dashboard/project/${id}/api` },
      ]
    }
  ]
}