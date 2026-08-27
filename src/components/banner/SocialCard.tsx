import { asset } from "@/lib/links";

/** Introductory banner. Render /social-card at 1280 × 640 to export the PNG. */
export default function SocialCard() {
  return (
    <div dir="rtl" role="img" aria-label="مرجع جامع Next.js 16؛ راهنمای فارسی از مفاهیم پایه تا Production، نوشتهٔ محمدرضا رضائیان" className="relative isolate h-[640px] w-[1280px] overflow-hidden bg-[#080c14] font-sans text-white">
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_14%_40%,#153b56_0%,transparent_48%)]" />
      <div className="absolute inset-0 -z-10 bg-[linear-gradient(#ffffff05_1px,transparent_1px),linear-gradient(90deg,#ffffff05_1px,transparent_1px)] bg-size-[48px_48px] mask-[linear-gradient(to_right,black,transparent_75%)]" />
      <div className="absolute inset-x-12 top-0 h-px bg-linear-to-r from-transparent via-cyan-300/70 to-transparent" />
      <div className="absolute top-12 right-14 flex items-center gap-3 text-[15px] font-medium tracking-wide text-cyan-200">
        <span className="size-2 rounded-full bg-cyan-300 shadow-[0_0_16px_#67e8f9]" />
        راهنمای فارسی توسعهٔ وب
      </div>
      <div dir="ltr" className="absolute top-12 left-14 font-mono text-[11px] tracking-[0.22em] text-slate-400">THE PERSIAN HANDBOOK / 01</div>

      <div className="absolute top-[128px] right-14 w-[690px]">
        <h1 className="text-[51px] font-extrabold leading-[1.45] tracking-tight">مرجع جامع <span dir="ltr" className="inline-block text-cyan-200">Next.js 16</span></h1>
        <p className="mt-5 text-[28px] font-medium text-slate-100">از مفاهیم پایه تا توسعه در سطح <span dir="ltr" className="inline-block">Production</span></p>
        <p className="mt-6 text-[18px] leading-9 text-slate-400">یادگیری عمیق، مثال‌های کاربردی و پروژه‌های عملی<br />برای ساخت تجربه‌های سریع، امن و مقیاس‌پذیر.</p>
        <div className="mt-8 flex items-center gap-5 text-[17px] text-slate-200">
          <span><b className="ml-2 text-[25px] text-white">۳۷</b>فصل</span>
          <span className="h-5 w-px bg-white/15" />
          <span><b className="ml-2 text-[25px] text-white">۱۷۸</b>صفحه</span>
          <span className="h-5 w-px bg-white/15" />
          <span className="text-cyan-200">مطالعهٔ رایگان</span>
        </div>
      </div>

      <div dir="ltr" className="absolute top-[148px] left-[60px] h-[330px] w-[370px]">
        <div className="absolute inset-5 rotate-[-9deg] rounded-[30px] border border-cyan-200/15 bg-cyan-200/[0.025]" />
        <div className="absolute inset-5 rotate-[7deg] rounded-[30px] border border-white/10 bg-white/[0.025]" />
        <div className="absolute inset-0 flex flex-col items-center justify-center rounded-[28px] border border-white/20 bg-linear-to-br from-[#182430] via-[#0e151e] to-[#080c14] shadow-[0_30px_90px_#00000080]">
          {/* Official wordmark from vercel/next.js create-next-app template. */}
          <img src={asset("/nextjs-wordmark.svg")} alt="Next.js" width={236} height={48} className="h-auto w-[236px] invert" />
          <div className="mt-6 font-sans text-[126px] font-extrabold leading-none tracking-[-0.08em] text-white">16<span className="text-cyan-300">.</span></div>
          <div className="mt-6 font-mono text-[10px] tracking-[0.23em] text-slate-400">LEARN. BUILD. SHIP.</div>
        </div>
        <span className="absolute -right-5 -bottom-3 rounded-xl border border-cyan-200/30 bg-[#122633] px-5 py-3 font-mono text-[12px] text-cyan-100 shadow-xl">App Router → Production</span>
      </div>

      <div className="absolute inset-x-14 bottom-[94px] h-px bg-white/10" />
      <div className="absolute right-14 bottom-10 flex items-center gap-3">
        <img src={asset("/author.webp")} alt="" width={38} height={38} className="size-[38px] rounded-full border border-white/20 object-cover" />
        <div><p className="text-[15px] font-bold">محمدرضا رضائیان</p><p className="mt-1 text-[11px] text-slate-400">نویسندهٔ راهنمای فارسی Next.js</p></div>
      </div>
      <div dir="ltr" className="absolute bottom-12 left-14 flex items-center gap-4 font-mono text-[12px] text-slate-400"><span className="text-cyan-200">READ ONLINE</span><span className="text-slate-600">/</span>PDF<span className="text-slate-600">/</span>EPUB</div>
    </div>
  );
}
