export type Chapter = { n: number; title: string };

export type Part = {
  id: string;
  emoji: string;
  label: string;
  range: string;
  tagline: string;
  outcome: string;
  chapters: Chapter[];
};

export const PARTS: Part[] = [
  {
    id: "part-1",
    emoji: "🌱",
    label: "بنیادها و مفاهیم اصلی",
    range: "فصل‌های ۱ تا ۱۶",
    tagline: "روتینگ، Layout، Server و Client Components، واکشی داده، کشینگ و Actions.",
    outcome: "یک اپ کامل می‌سازی و می‌دانی هر کد کجا اجرا می‌شود.",
    chapters: [
      { n: 1, title: "معرفی Next.js 16 و تازه‌های نسخه" },
      { n: 2, title: "شروع به کار و ساختار پروژه" },
      { n: 3, title: "نقشه راه یادگیری" },
      { n: 4, title: "روتینگ فایل‌محور (App Router)" },
      { n: 5, title: "Layout، فایل‌های ویژه و Metadata" },
      { n: 6, title: "پیوند و ناوبری" },
      { n: 7, title: "Server Components و Client Components" },
      { n: 8, title: "واکشی داده و Streaming" },
      { n: 9, title: "کشینگ مدرن با Cache Components" },
      { n: 10, title: "Server Actions و تغییر داده" },
      { n: 11, title: "Route Handlers (مبانی API)" },
      { n: 12, title: "Middleware؛ جانشین proxy.ts" },
      { n: 13, title: "استایل‌دهی با Tailwind v4" },
      { n: 14, title: "بهینه‌سازی: تصویر، فونت، لینک و سئو" },
      { n: 15, title: "محیط، TypeScript و استقرار" },
      { n: 16, title: "پروژه عملی: مینی‌بالگ کامل" },
    ],
  },
  {
    id: "part-2",
    emoji: "🏗️",
    label: "معماری، پیشرفته و فوق‌پیشرفته",
    range: "فصل‌های ۱۷ تا ۳۲",
    tagline: "استراتژی رندر، API، Hydration، احراز هویت، امنیت، تست و استقرار.",
    outcome: "معماری Production با مرزهای روشن و کیفیت قابل دفاع.",
    chapters: [
      { n: 17, title: "معماری پروژه، ساختار پوشه و Clean Code" },
      { n: 18, title: "استراتژی‌های رندر: SSG، ISR، SSR و PPR" },
      { n: 19, title: "API‌نویسی کامل با Route Handlers" },
      { n: 20, title: "خطاهای Hydration — مرجع کامل" },
      { n: 21, title: "احراز هویت و کنترل دسترسی" },
      { n: 22, title: "امنیت اپلیکیشن — فصل کامل" },
      { n: 23, title: "فرم‌ها و اعتبارسنجی پیشرفته" },
      { n: 24, title: "مدیریت state و داده در کلاینت" },
      { n: 25, title: "تسلط بر کشینگ: لایه‌ها و باطل‌سازی" },
      { n: 26, title: "کارایی و Core Web Vitals" },
      { n: 27, title: "Metadata و سئو — کامل" },
      { n: 28, title: "TypeScript پیشرفته و امنیت تایپ" },
      { n: 29, title: "مدیریت خطا — کامل" },
      { n: 30, title: "تست‌نویسی" },
      { n: 31, title: "استقرار حرفه‌ای و Self-Hosting" },
      { n: 32, title: "مهاجرت و ارتقا به نسخه ۱۶" },
    ],
  },
  {
    id: "part-3",
    emoji: "🚀",
    label: "جمع‌بندی و کارگاه",
    range: "فصل‌های ۳۳ تا ۳۵",
    tagline: "ترفندهای طلایی، هشت مینی‌پروژه و بهترین شیوه‌ها.",
    outcome: "تثبیت مهارت روی پروژه‌های واقعی.",
    chapters: [
      { n: 33, title: "نکات و ترفندهای طلایی" },
      { n: 34, title: "کارگاه مینی‌پروژه‌ها" },
      { n: 35, title: "بهترین شیوه‌ها، اشتباهات رایج و منابع" },
    ],
  },
  {
    id: "part-4",
    emoji: "🏁",
    label: "پیوست‌ها",
    range: "فصل‌های ۳۶ تا ۳۷",
    tagline: "پرسش‌های مصاحبه از Junior تا Senior و واژه‌نامهٔ فارسی–انگلیسی.",
    outcome: "آمادگی مصاحبه و مرجع سریع اصطلاحات.",
    chapters: [
      { n: 36, title: "پرسش‌های مصاحبه (Junior تا Senior)" },
      { n: 37, title: "واژه‌نامه فارسی–انگلیسی" },
    ],
  },
];

export const TOTAL_CHAPTERS = PARTS.reduce((sum, p) => sum + p.chapters.length, 0);
