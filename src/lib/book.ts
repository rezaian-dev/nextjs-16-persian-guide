/**
 * Online-edition data for the `/book` reader route.
 *
 * This is the typeset book's own outline: every chapter's first page, title
 * and subtitle, grouped into parts. The reader renders one `<figure>` per
 * page of `public/book/pages/*.webp` and drops a `#ch-NN` anchor wherever a
 * chapter starts, so `/chapters` and the README can deep-link to any chapter.
 *
 * Ported from the former `src/edition/chapters.json` so the repository stays
 * a pure TypeScript + CSS Next.js app.
 */

export type BookChapter = {
  /** 1-based chapter number. */
  num: number;
  /** First page of the chapter in the typeset edition. */
  page: number;
  title: string;
  subtitle: string;
};

export type BookPart = {
  num: number;
  name: string;
  /** First chapter number in this part (inclusive). */
  from: number;
  /** Last chapter number in this part (inclusive). */
  to: number;
};

export const BOOK = {
  title: "مرجع جامع Next.js 16",
  subtitle: "از مقدماتی تا سطح Production",
  edition: "1.0.0",
  year: 2026,
  pages: 178,
  author: "محمدرضا رضائیان",
  license: "CC BY-NC-SA 4.0",
  pdfFile: "Nextjs16-Persian-Guide.pdf",
  epubFile: "Nextjs16-Persian-Guide.epub",
  socialCard: "social-card.png",
  /** Stored pixel size of every `public/book/pages/*.webp` (3x the 820px paint width). */
  pageWidth: 2460,
  pageHeight: 3482,
} as const;

export const BOOK_PARTS: BookPart[] = [
  { num: 1, name: "بنیادها و مفاهیم اصلی", from: 1, to: 16 },
  { num: 2, name: "معماری، پیشرفته و فوق‌پیشرفته", from: 17, to: 32 },
  { num: 3, name: "جمع‌بندی و کارگاه", from: 33, to: 35 },
  { num: 4, name: "پیوست‌ها", from: 36, to: 37 },
];

export const BOOK_CHAPTERS: BookChapter[] = [
  { num: 1, page: 5, title: "معرفی Next.js 16 و تازه‌های نسخه", subtitle: "فریم‌ورک چیست و در نسخه ۱۶ چه تغییر کرده" },
  { num: 2, page: 7, title: "شروع به کار و ساختار پروژه", subtitle: "نصب، Turbopack، create-next-app و آناتومی فولدرها" },
  { num: 3, page: 9, title: "نقشه راه یادگیری", subtitle: "مسیر مبتدی تا حرفه‌ای و نحوه استفاده از کتاب" },
  { num: 4, page: 11, title: "روتینگ فایل‌محور (App Router)", subtitle: "صفحات، مسیرهای پویا، گروه‌ها و موازی" },
  { num: 5, page: 19, title: "Layout، فایل‌های ویژه و Metadata", subtitle: "قالب‌ها، loading، error، not-found و سئوی پایه" },
  { num: 6, page: 23, title: "پیوند و ناوبری", subtitle: "useRouter، prefetch، Link و useLinkStatus" },
  { num: 7, page: 29, title: "Server Components و Client Components", subtitle: "تفاوت، زمان استفاده و الگوی ترکیب" },
  { num: 8, page: 36, title: "واکشی داده و Streaming", subtitle: "Suspense، async، موازی و preload" },
  { num: 9, page: 45, title: "کشینگ مدرن با Cache Components", subtitle: "cacheTag، cacheLife، use cache و revalidate" },
  { num: 10, page: 51, title: "Server Actions و تغییر داده", subtitle: "فرم‌ها، useActionState و revalidation" },
  { num: 11, page: 56, title: "Route Handlers (مبانی API)", subtitle: "ساخت اندپوینت و پارامترهای async" },
  { num: 12, page: 60, title: "Middleware؛ جانشین proxy.ts", subtitle: "احراز هویت، ریدایرکت و نکات امنیتی" },
  { num: 13, page: 62, title: "استایل‌دهی با Tailwind v4", subtitle: "Tailwind، CSS Modules و shadcn/ui" },
  { num: 14, page: 64, title: "بهینه‌سازی: تصویر، فونت، لینک و سئو", subtitle: "next/font، next/image و sitemap" },
  { num: 15, page: 66, title: "محیط، TypeScript و استقرار", subtitle: "پیکربندی، تایپ‌ها و دیپلوی پایه" },
  { num: 16, page: 70, title: "پروژه عملی: مینی‌بالگ کامل", subtitle: "ترکیب مفاهیم پایه در یک نمونه واقعی" },
  { num: 17, page: 74, title: "معماری پروژه، ساختار پوشه و Clean Code", subtitle: "لایه‌بندی، DAL، feature-based و مقیاس‌پذیری" },
  { num: 18, page: 78, title: "استراتژی‌های رندر: SSG، ISR، SSR و PPR", subtitle: "چهار مدل رندر و پیش‌رندر جزئی" },
  { num: 19, page: 84, title: "API‌نویسی کامل با Route Handlers", subtitle: "استریم، CORS، Webhook، SSE و Runtime" },
  { num: 20, page: 94, title: "خطاهای Hydration — مرجع کامل", subtitle: "علت‌ها، راه‌حل و جدول مرجع سریع" },
  { num: 21, page: 102, title: "احراز هویت و کنترل دسترسی", subtitle: "session، کوکی httpOnly و RBAC" },
  { num: 22, page: 106, title: "امنیت اپلیکیشن — فصل کامل", subtitle: "اعتبارسنجی، rate limit، XSS، CSRF و اسرار" },
  { num: 23, page: 112, title: "فرم‌ها و اعتبارسنجی پیشرفته", subtitle: "schema، useFormStatus، مشترک و بهبود تدریجی" },
  { num: 24, page: 117, title: "مدیریت state و داده در کلاینت", subtitle: "هوک SWR، use()، Context" },
  { num: 25, page: 121, title: "تسلط بر کشینگ: لایه‌ها و باطل‌سازی", subtitle: "گونه‌های use cache و پروفایل سفارشی" },
  { num: 26, page: 125, title: "کارایی و Core Web Vitals", subtitle: "LCP، CLS، INP و React Compiler" },
  { num: 27, page: 128, title: "Metadata و سئو — کامل", subtitle: "OG، Open Graph پویا و JSON-LD" },
  { num: 28, page: 132, title: "TypeScript پیشرفته و امنیت تایپ", subtitle: "typedRoutes، infer، zod و satisfies" },
  { num: 29, page: 135, title: "مدیریت خطا — کامل", subtitle: "سلسله‌مراتب خطا و notFound" },
  { num: 30, page: 139, title: "تست‌نویسی", subtitle: "Vitest، Testing Library و Playwright" },
  { num: 31, page: 142, title: "استقرار حرفه‌ای و Self-Hosting", subtitle: "Docker، standalone، Vercel و چک‌لیست" },
  { num: 32, page: 146, title: "مهاجرت و ارتقا به نسخه ۱۶", subtitle: "codemod و تغییرات شکننده" },
  { num: 33, page: 149, title: "نکات و ترفندهای طلایی", subtitle: "React.cache، after، useOptimistic و …" },
  { num: 34, page: 155, title: "کارگاه مینی‌پروژه‌ها", subtitle: "هشت پروژه کوچک صفر تا صد" },
  { num: 35, page: 172, title: "بهترین شیوه‌ها، اشتباهات رایج و منابع", subtitle: "جمع‌بندی حرفه‌ای و مسیر ادامه" },
  { num: 36, page: 174, title: "پرسش‌های مصاحبه (Junior تا Senior)", subtitle: "پرکاربردترین سؤالات با پاسخ دقیق" },
  { num: 37, page: 176, title: "واژه‌نامه فارسی–انگلیسی", subtitle: "مرجع سریع اصطلاحات کلیدی" },
];

export const TOTAL_PAGES = BOOK.pages;
export const TOTAL_BOOK_CHAPTERS = BOOK_CHAPTERS.length;

const FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹";

/** Latin digits → Persian digits (`239` → `۲۳۹`). */
export function fa(n: number | string): string {
  return String(n).replace(/[0-9]/g, (d) => FA_DIGITS[Number(d)]);
}

/** DOM id of a chapter head, e.g. `ch-05`. */
export function chapterId(num: number): string {
  return `ch-${String(num).padStart(2, "0")}`;
}

/** The part a chapter belongs to. */
export function partOf(num: number): BookPart | undefined {
  return BOOK_PARTS.find((p) => p.from <= num && num <= p.to);
}

const chapterByPage = new Map(BOOK_CHAPTERS.map((c) => [c.page, c]));

/** The chapter that starts on a page, if any. */
export function chapterOnPage(page: number): BookChapter | undefined {
  return chapterByPage.get(page);
}
