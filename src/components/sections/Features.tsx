"use client";

import { Layers, Database, Zap, ShieldCheck, Gauge, GraduationCap } from "lucide-react";

import SectionHeader from "@/components/layout/SectionHeader";
import Reveal from "@/components/motion/Reveal";
import TiltCard from "@/components/motion/TiltCard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const FEATURES = [
  { icon: Layers, title: "مرز سرور و کلاینت، روشن", text: "می‌دانی چه چیزی روی سرور می‌ماند و `\"use client\"` را کجا و چرا می‌نویسی." },
  { icon: Database, title: "کشینگ مدرن", text: "`use cache`، `cacheTag` و `cacheLife`؛ در نسخهٔ ۱۶ همه‌چیز پیش‌فرض پویاست و کش را صریح انتخاب می‌کنی." },
  { icon: Zap, title: "رندر و Streaming", text: "SSG، ISR، SSR و PPR کنار هم؛ با `Suspense` و واکشی موازی به‌جای آبشار درخواست." },
  { icon: ShieldCheck, title: "امنیت Production", text: "اعتبارسنجی، rate limit، XSS، CSRF، کوکی `httpOnly` و مدیریت اسرار." },
  { icon: Gauge, title: "کارایی و Core Web Vitals", text: "LCP، CLS و INP با `next/image`، `next/font` و React Compiler‏." },
  { icon: GraduationCap, title: "کارگاه و مصاحبه", text: "هشت مینی‌پروژه، بهترین شیوه‌ها و بیست‌وچهار جعبهٔ پرسش مصاحبه." },
];

export default function Features() {
  return (
    <section className="py-24 md:py-32" id="features">
      <div className="container">
        <SectionHeader
          eyebrow="Why this guide"
          title={<>Server-first، با <span className="grad-text">مرزهای روشن</span></>}
          lead="هر مفهوم اول روی مدل اجرای Next.js می‌نشیند؛ بعد در یک نمونهٔ واقعی پیاده می‌شود."
        />
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {FEATURES.map((f, i) => (
            <Reveal key={f.title} delay={(i % 3) * 0.08}>
              <TiltCard className="h-full">
                <Card className="h-full">
                  <CardHeader>
                    <span className="mb-1 grid size-12 place-items-center rounded-[14px] border border-primary/25 bg-linear-to-br from-primary/15 to-sky/10 text-primary-soft">
                      <f.icon className="size-6" />
                    </span>
                    <CardTitle className="text-[17px]">{f.title}</CardTitle>
                  </CardHeader>
                  <CardContent className="flex-1 text-[13.5px] leading-7 text-muted-foreground">
                    {f.text.split("`").map((p, j) =>
                      j % 2 === 1 ? (
                        <code key={j} className="rounded-md border border-border bg-secondary/60 px-1.5 py-0.5 font-mono text-xs text-primary-soft">{p}</code>
                      ) : (
                        <span key={j}>{p}</span>
                      )
                    )}
                  </CardContent>
                </Card>
              </TiltCard>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
