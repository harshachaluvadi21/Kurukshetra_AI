import type { Metadata } from "next";
import NavBar from "./NavBar";
import "./globals.css";

export const metadata: Metadata = {
  title: "Kurukshetra AI — Battle-Test Your Startup",
  description: "Multi-agent AI platform that evaluates startup ideas using debates, web intelligence, RAG, and scoring engines.",
};

import { AuthProvider } from "./AuthProvider";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className="dark"
      suppressHydrationWarning
    >
      <body className="min-h-screen bg-zinc-950 text-zinc-50 antialiased" suppressHydrationWarning>
        <AuthProvider>
          <NavBar />
          <main>{children}</main>
        </AuthProvider>
      </body>
    </html>
  );
}
