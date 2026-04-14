import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'CMOS Failure Dashboard',
  description: 'AI-powered predictive maintenance dashboard',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
