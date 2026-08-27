import type { SVGProps } from "react";

/**
 * Next.js mark — the "N" glyph inside the circle.
 * Inherits currentColor so it can sit on the gradient brand tile.
 */
export default function NextIcon(props: SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 180 180" fill="none" aria-hidden="true" {...props}>
      <mask
        id="next-mark"
        className="[mask-type:alpha]"
        maskUnits="userSpaceOnUse"
        x="0"
        y="0"
        width="180"
        height="180"
      >
        <circle cx="90" cy="90" r="90" fill="black" />
      </mask>
      <g mask="url(#next-mark)">
        <circle cx="90" cy="90" r="87" fill="none" stroke="currentColor" strokeWidth="6" />
        <path
          d="M149.508 157.52 69.142 54H54v71.971h12.114V69.183l73.885 95.777a90.052 90.052 0 0 0 9.509-7.44ZM115.811 54h11.999v72h-11.999V54Z"
          fill="currentColor"
        />
      </g>
    </svg>
  );
}
