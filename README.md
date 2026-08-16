<a id="top"></a>

<p align="center">
  <img src="./assets/readme/readme-hero.webp" alt="مرجع فارسی Next.js 16" width="880">
</p>

<p align="center" dir="rtl">
  <strong>🎉 راهنمای کامل Next.js 16 به زبان فارسی — رایگان و بدون محدودیت</strong>
</p>

<p align="center">
  <a href="https://rezaian-dev.github.io/nextjs-16-persian-guide/"><img src="https://img.shields.io/badge/READ_ONLINE-0EA5E9?style=for-the-badge&logo=githubpages&logoColor=white" alt="مطالعه آنلاین"></a>
  <a href="./docs/pdf/Nextjs16-Persian-Guide.pdf"><img src="https://img.shields.io/badge/DOWNLOAD_PDF-DC2626?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="دانلود PDF"></a>
  <a href="./docs/pdf/Nextjs16-Persian-Guide.epub"><img src="https://img.shields.io/badge/DOWNLOAD_EPUB-7C3AED?style=for-the-badge&logo=applebooks&logoColor=white" alt="دانلود EPUB"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-16-F8FAFC?style=flat-square&logo=nextdotjs&logoColor=000" alt="Next.js 16">
  <img src="https://img.shields.io/badge/فصل-۳۷-0F172A?style=flat-square" alt="۳۷ فصل">
  <img src="https://img.shields.io/badge/صفحه-۱۷۸-0F172A?style=flat-square" alt="۱۷۸ صفحه">
  <img src="https://img.shields.io/badge/قطعه_کد-۲۱۶-0F172A?style=flat-square" alt="۲۱۶ قطعه کد">
  <img src="https://img.shields.io/badge/Edition-1.0.0-16A34A?style=flat-square" alt="ویرایش ۱.۰.۰">
  <img src="https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-64748B?style=flat-square" alt="مجوز CC BY-NC-SA 4.0">
</p>

---

<div dir="rtl">

## ✨ این راهنما چیست؟

> **مرجع فارسی، پروژه‌محور و به‌روز Next.js 16** — از اولین `page.tsx` تا استقرار در Production.

Next.js 16 دنیای خودش را دارد: **Cache Components**، رندر سروری عمیق، `proxy.ts` و React 19.2. این کتاب همان‌هایی را — برای اولین بار به فارسی — با **زبان ساده، مدل ذهنی درست و کد واقعی** توضیح می‌دهد.

اینجا قرار نیست فهرست APIها را حفظ کنید؛ قرار است یاد بگیرید مثل یک مهندس ارشد **فکر کنید، تصمیم بگیرید و معماری بچینید**. 🧠

## 👥 برای چه کسی؟

| 🎯 اگر شما… | 📦 این کتاب به شما می‌دهد |
|:---:|:---|
| تازه وارد دنیای Next.js شده‌اید | مسیر یادگیری گام‌به‌گام از صفر تا اولین اپ کامل |
| با نسخه‌های قبلی کار کرده‌اید | نقشهٔ ارتقای دقیق به ۱۶ و تازه‌های Cache Components |
| دنبال سطح ارشد هستید | معماری، امنیت، تست، کارایی و الگوهای Production |
| در مسیر استخدام هستید | ۱۰۰+ پرسش مصاحبه با پاسخ تشریحی و واژه‌نامهٔ تخصصی |

## 💎 چرا این کتاب متفاوت است؟

- ⚡ **همگام با نسخهٔ ۱۶** — Cache Components، `use cache`، `cacheLife`، `cacheTag`، Turbopack و `proxy.ts`
- 🧠 **تمرکز بر «چرا»** — درک رفتار فریم‌ورک به‌جای حفظ‌کردن سینتکس
- 💻 **کد واقعی، نه اسلایدهای تئوری** — ۲۱۶ قطعه‌کد TypeScript و ترمینال
- 🛠️ **یادگیری با دست** — یک مینی‌بالگ کامل + ۸ مینی‌پروژهٔ کارگاهی
- 🔐 **Production از روز اول** — احراز هویت، RBAC، امنیت، Rate Limit، Docker و Core Web Vitals
- 🇮🇷 **فارسی روان، اصطلاح‌ها دوزبانه** — با واژه‌نامهٔ فارسی–انگلیسی پایان کتاب

## 🗺️ مسیر کتاب در یک نگاه

| 🌱 بنیادها<br><sub>فصل ۱–۱۶</sub> | 🏗️ معماری و Production<br><sub>فصل ۱۷–۳۲</sub> | 🛠️ کارگاه<br><sub>فصل ۳۳–۳۵</sub> | 🎓 مرجع شغلی<br><sub>فصل ۳۶–۳۷</sub> |
|:---:|:---:|:---:|:---:|
| App Router، RSC، داده،<br>کشینگ و اولین اپ کامل | رندر، امنیت، فرم، سئو،<br>تست و استقرار | ۸ مینی‌پروژه،<br>نکات طلایی و بهترین شیوه‌ها | پرسش‌های مصاحبه<br>و واژه‌نامهٔ فارسی–انگلیسی |

<sub>💡 مسیر پیشنهادی همین ترتیب است؛ اما اگر تجربه دارید، هر فصل مستقل هم خوانده می‌شود. [فهرست کامل فصل‌ها ↓](#chapters)</sub>

<a id="preview"></a>

## 🖼️ نگاهی به داخل کتاب

<p align="center">
  <a href="./assets/readme/page-toc.png"><img src="./assets/readme/preview-toc.webp" alt="فهرست مطالب" width="180"></a>
  <a href="./assets/readme/page-chapter.png"><img src="./assets/readme/preview-chapter.webp" alt="ساختار فصل" width="180"></a>
  <a href="./assets/readme/page-code.png"><img src="./assets/readme/preview-code.webp" alt="نمونهٔ کد" width="180"></a>
  <a href="./assets/readme/page-workshop.png"><img src="./assets/readme/preview-workshop.webp" alt="کارگاه پروژه" width="180"></a>
</p>

## 📦 در چه قالبی می‌خواهید؟

| قالب | مناسب برای | لینک |
|:---:|:---:|:---:|
| 🌐 **آنلاین** | مطالعهٔ فوری در مرورگر با پیوند مستقیم به هر فصل | [**شروع مطالعه**](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/) |
| 📕 **PDF** | دانلود، جست‌وجو و چاپ — قطع A4 رنگی | [**دانلود**](./docs/pdf/Nextjs16-Persian-Guide.pdf) |
| 📗 **EPUB** | موبایل، تبلت و کتاب‌خوان | [**دانلود**](./docs/pdf/Nextjs16-Persian-Guide.epub) |
| 🧰 **سورس** | کد سایت و ابزارهای ساخت کتاب | [**همین مخزن**](https://github.com/rezaian-dev/nextjs-16-persian-guide) |

<a id="chapters"></a>

<details>
<summary><strong>📚 فهرست کامل ۳۷ فصل</strong> <em>(برای باز کردن کلیک کنید)</em></summary>

**🌱 بخش اول — بنیادها و اولین اپ · فصل‌های ۱ تا ۱۶**

1. [معرفی Next.js 16 و تازه‌های نسخه](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-01) — ص ۵
2. [شروع به کار و ساختار پروژه](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-02) — ص ۷
3. [نقشه راه یادگیری](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-03) — ص ۹
4. [روتینگ فایل‌محور (App Router)](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-04) — ص ۱۱
5. [Layout، فایل‌های ویژه و Metadata](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-05) — ص ۱۹
6. [پیوند و ناوبری](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-06) — ص ۲۳
7. [Server Components و Client Components](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-07) — ص ۲۹
8. [واکشی داده و Streaming](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-08) — ص ۳۶
9. [کشینگ مدرن با Cache Components](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-09) — ص ۴۵
10. [Server Actions و تغییر داده](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-10) — ص ۵۱
11. [Route Handlers (مبانی API)](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-11) — ص ۵۶
12. [Middleware؛ جانشین proxy.ts](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-12) — ص ۶۰
13. [استایل‌دهی با Tailwind v4](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-13) — ص ۶۲
14. [بهینه‌سازی: تصویر، فونت، لینک و سئو](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-14) — ص ۶۴
15. [محیط، TypeScript و استقرار](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-15) — ص ۶۶
16. [پروژه عملی: مینی‌بالگ کامل](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-16) — ص ۷۰

**🏗️ بخش دوم — معماری و Production · فصل‌های ۱۷ تا ۳۲**

17. [معماری پروژه، ساختار پوشه و Clean Code](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-17) — ص ۷۴
18. [استراتژی‌های رندر: SSG، ISR، SSR و PPR](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-18) — ص ۷۸
19. [API‌نویسی کامل با Route Handlers](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-19) — ص ۸۴
20. [خطاهای Hydration — مرجع کامل](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-20) — ص ۹۴
21. [احراز هویت و کنترل دسترسی](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-21) — ص ۱۰۲
22. [امنیت اپلیکیشن — فصل کامل](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-22) — ص ۱۰۶
23. [فرم‌ها و اعتبارسنجی پیشرفته](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-23) — ص ۱۱۲
24. [مدیریت state و داده در کلاینت](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-24) — ص ۱۱۷
25. [تسلط بر کشینگ: لایه‌ها و باطل‌سازی](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-25) — ص ۱۲۱
26. [کارایی و Core Web Vitals](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-26) — ص ۱۲۵
27. [Metadata و سئو — کامل](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-27) — ص ۱۲۸
28. [TypeScript پیشرفته و امنیت تایپ](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-28) — ص ۱۳۲
29. [مدیریت خطا — کامل](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-29) — ص ۱۳۵
30. [تست‌نویسی](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-30) — ص ۱۳۹
31. [استقرار حرفه‌ای و Self-Hosting](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-31) — ص ۱۴۲
32. [مهاجرت و ارتقا به نسخه ۱۶](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-32) — ص ۱۴۶

**🛠️ بخش سوم — کارگاه و تثبیت · فصل‌های ۳۳ تا ۳۵**

33. [نکات و ترفندهای طلایی](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-33) — ص ۱۴۹
34. [کارگاه مینی‌پروژه‌ها](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-34) — ص ۱۵۵
35. [بهترین شیوه‌ها، اشتباهات رایج و منابع](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-35) — ص ۱۷۲

**🎓 بخش چهارم — مرجع و آمادگی شغلی · فصل‌های ۳۶ تا ۳۷**

36. [پرسش‌های مصاحبه (Junior تا Senior)](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-36) — ص ۱۷۴
37. [واژه‌نامه فارسی–انگلیسی](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/#ch-37) — ص ۱۷۶

</details>

<a id="quickstart"></a>

## 🚀 دو قدم تا شروع

۱. **سریع‌ترین راه:** کتاب را همان [نسخهٔ آنلاین](https://rezaian-dev.github.io/nextjs-16-persian-guide/book/) بخوانید — نصب لازم نیست. ⚡

۲. **اگر سورس را می‌خواهید:**

```bash
git clone https://github.com/rezaian-dev/nextjs-16-persian-guide.git
cd nextjs-16-persian-guide && npm install && npm run dev
```

<details>
<summary><strong>🛠️ بیلد کامل و ابزارهای کتاب (پایتون، PDF، EPUB)</strong></summary>

```bash
# سایت — بیلد استاتیک برای GitHub Pages
npm run build        # بیلد استاندارد (Vercel / Node)
npm run build:pages  # خروجی استاتیک در out/ با basePath

# کتاب — پیش‌نیاز Python 3.10+
python -m venv .venv && source .venv/bin/activate
python -m pip install -r src/requirements.txt
python src/tools/build_edition.py   # PDF
python src/tools/build_epub.py      # EPUB
python src/tools/build_reader.py    # نسخهٔ آنلاین در public/book/
python src/tools/qa.py              # کنترل کیفیت
```

```text
src/app/        صفحه‌ها و layout اپ Next.js
src/components/ کامپوننت‌های رابط کاربری
src/lib/        داده فصل‌ها و پیوندها
src/edition/    منبع ساختاری فصل‌ها (chapters.json)
src/tools/      ساخت کتاب، پیش‌نمایش و QA
public/         دارایی‌ها، PDF، EPUB و نسخهٔ آنلاین
docs/           خروجی منتشرشده روی GitHub Pages
```

</details>

## 🧩 مجموعهٔ کامل راهنماهای فارسی

چهار مرجع، یک مسیر هماهنگ برای فرانت‌اند مدرن:

| راهنما | موضوع | لینک‌ها |
|:---|:---|:---|
| 🌱 [**Git و GitHub ۲۰۲۶**](https://github.com/rezaian-dev/git-github-persian-guide) | نسخه‌بندی، VS Code و همکاری | [آنلاین](https://rezaian-dev.github.io/git-github-persian-guide/) |
| 🟨 [**JavaScript ES2025**](https://github.com/rezaian-dev/javascript-persian-guide) | زبان و مدل ذهنی | [آنلاین](https://rezaian-dev.github.io/javascript-persian-guide/) |
| ⚛️ [**React 19.2**](https://github.com/rezaian-dev/react-19-persian-guide) | رابط کاربری، state و معماری | [آنلاین](https://rezaian-dev.github.io/react-19-persian-guide/) |
| ▲ [**Next.js 16**](https://github.com/rezaian-dev/nextjs-16-persian-guide) | فریم‌ورک، رندر سرور و استقرار | [آنلاین](https://rezaian-dev.github.io/nextjs-16-persian-guide/) · 📍 **همین کتاب** |

## 🤝 مشارکت

خطایی دیدید؟ پیشنهادی دارید؟ یک [Issue](https://github.com/rezaian-dev/nextjs-16-persian-guide/issues) باز کنید 🐛 — PRهای کوچک و متمرکز هم همیشه خوش‌آمدند. 🙏

## ✍️ نویسنده و مجوز

**محمدرضا رضائیان** — [@rezaian-dev](https://github.com/rezaian-dev)

این اثر با مجوز [Creative Commons BY-NC-SA 4.0](./LICENSE) منتشر شده است: استفاده و بازنشر غیرتجاری با ذکر منبع آزاد است و نسخهٔ اقتباسی باید با همین مجوز منتشر شود. ⚖️

</div>

---

<p align="center" dir="rtl">
  ⭐ اگر این راهنما برایتان مفید بود، با ثبت یک ستاره از ادامهٔ راه مجموعه حمایت کنید.
  <br>
  <a href="#top">بازگشت به بالا ↑</a>
</p>
