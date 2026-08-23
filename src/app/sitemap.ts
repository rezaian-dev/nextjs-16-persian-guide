import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/links";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: `${SITE_URL}/`, changeFrequency: "monthly", priority: 1 },
    { url: `${SITE_URL}/book/`, changeFrequency: "monthly", priority: 0.9 },
    { url: `${SITE_URL}/chapters/`, changeFrequency: "monthly", priority: 0.8 },
  ];
}
