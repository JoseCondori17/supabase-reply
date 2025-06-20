export interface Route {
  label: string;
  href: string;
  items?: Route[];
};