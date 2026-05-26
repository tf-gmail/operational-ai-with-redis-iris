import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Operational AI with Redis IRIS",
  description: "Productionizing LangGraph Agents with Redis IRIS"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
