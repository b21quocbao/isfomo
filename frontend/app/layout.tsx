import '@mantine/core/styles.css';
import React from 'react';
import { ColorSchemeScript, createTheme, MantineProvider } from '@mantine/core';
import './layout.css';

export const metadata = {
  title: 'IsFOMO',
  description: 'ETHGlobal',
};

const theme = createTheme({
  fontFamily: 'Noto Sans Mono, monospace',
});

export default function RootLayout({ children }: { children: any }) {
  return (
    <html lang="en">
      <head>
        <ColorSchemeScript defaultColorScheme='dark' />
        <link rel="shortcut icon" href="/mood-crazy-happy.svg" />
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width, user-scalable=no"
        />
      </head>
      <body>
        <MantineProvider theme={theme}>{children}</MantineProvider>
      </body>
    </html>
  );
}
