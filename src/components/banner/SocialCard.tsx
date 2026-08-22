import { asset } from "@/lib/links";
import "./social-card.css";

/**
 * Fixed-size (1280×640) social / OG card for the Next.js 16 handbook.
 *
 * Rendered by the `/social-card` route (not linked anywhere in the UI) —
 * screenshot that route at 1280×640 to regenerate the
 * `public/social-card.png` Open Graph image.
 */
export default function SocialCard() {
  return (
    <div className="sc" role="img" aria-label="مرجع جامع Next.js 16">
      <div className="sc-grid" aria-hidden="true" />

      <div className="sc-title">
        <div className="sc-kicker">PERSIAN DEVELOPER HANDBOOK</div>
        <div className="sc-h1">
          مرجع جامع{" "}
          <span className="en">
            Next.js <b>16</b>
          </span>
        </div>
        <div className="sc-sub">
          از <b>App Router</b> تا معماری Production · رایگان و متن‌باز
        </div>
      </div>

      <div className="sc-stats">
        <span>
          <b>۳۷</b>فصل
        </span>
        <span>
          <b>۱۷۸</b>صفحه
        </span>
        <span>
          <b>۲۱۶</b>قطعه‌کد
        </span>
        <span>
          <b>۸</b>مینی‌پروژه
        </span>
        <span>PDF · EPUB · نسخه آنلاین</span>
      </div>

      <div className="sc-tags">
        <span>Next.js 16</span>
        <span>React 19</span>
        <span>TypeScript</span>
        <span>Tailwind CSS</span>
        <span>Server Actions</span>
      </div>

      <div className="sc-author">
        <img src={asset("/author.webp")} alt="" width={62} height={62} />
        <div className="txt">
          <div className="n">محمدرضا رضائیان</div>
          <div className="r">Front-End Developer</div>
        </div>
      </div>
      <div className="sc-url">github.com/rezaian-dev/nextjs-16-persian-guide</div>

      <div className="sc-win">
        <div className="sc-window">
          <div className="sc-win-head">
            <span className="d r" />
            <span className="d y" />
            <span className="d g" />
            <span className="fn">app/dashboard/page.tsx</span>
          </div>
          <pre>
            <span className="k">import</span> {"{ Suspense } "}<span className="k">from</span> <span className="s">'react'</span>;{"\n"}
            <span className="k">import type</span> {"{ Metadata } "}<span className="k">from</span> <span className="s">'next'</span>;{"\n"}
            {"\n"}
            <span className="k">export const</span> metadata: <span className="t">Metadata</span> = {"{"}{"\n"}
            {"  "}title: <span className="s">'Next.js 16 Dashboard'</span>,{"\n"}
            {"}"};{"\n"}
            {"\n"}
            <span className="k">export default async function</span> <span className="f">Page</span>() {"{"}{"\n"}
            {"  "}<span className="k">return</span> ({"\n"}
            {"    "}&lt;<span className="tag">main</span>&gt;{"\n"}
            {"      "}&lt;<span className="tag">h1</span>&gt;Dashboard&lt;/<span className="tag">h1</span>&gt;{"\n"}
            {"      "}&lt;<span className="tag">Suspense</span> <span className="a">fallback</span>={"{"}&lt;<span className="tag">Loading</span> /&gt;{"}"}&gt;{"\n"}
            {"        "}&lt;<span className="tag">Dashboard</span> /&gt;{"\n"}
            {"      "}&lt;/<span className="tag">Suspense</span>&gt;{"\n"}
            {"    "}&lt;/<span className="tag">main</span>&gt;{"\n"}
            {"  "});{"\n"}
            {"}"}
          </pre>
        </div>
      </div>
    </div>
  );
}
