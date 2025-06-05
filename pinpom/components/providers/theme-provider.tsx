'use client'

import { ThemeProvider as NextThemeProviders } from 'next-themes';

export function ThemeProvider({
  children,
  ...props
}: React.ComponentProps<
  typeof NextThemeProviders
>) {
  return (
    <NextThemeProviders {...props}>
      {children}
    </NextThemeProviders>
  );
}