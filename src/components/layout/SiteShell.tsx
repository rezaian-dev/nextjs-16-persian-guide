import type { ReactNode } from "react";
import Background from "./Background";
import ScrollProgress from "./ScrollProgress";
import Navbar from "./Navbar";
import Footer from "./Footer";

/** Shared site chrome; the reader and social card keep their own layouts. */
export default function SiteShell({ children }: { children: ReactNode }) {
  return (
    <>
      <Background />
      <ScrollProgress />
      <Navbar />
      {children}
      <Footer />
    </>
  );
}
