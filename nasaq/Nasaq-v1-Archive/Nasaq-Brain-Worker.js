/**
 * نَسَق — عقل خارجي على Cloudflare Workers AI
 * إعداد وتقديم: غيث صادق كيوان · GEN CODE TEAM · مدرسة السدرة الخاصة — كلباء
 *
 * ما يفعله: يستقبل سؤالاً ولقطةً من الجدول من تطبيق نَسَق، ويمرّرهما إلى نموذج
 * لغة على Cloudflare Workers AI، ويعيد الإجابة. مفتاح الحساب لا يصل المتصفّح
 * إطلاقاً: الاستدعاء يتمّ عبر ربط Workers AI داخل الـ Worker نفسه.
 *
 * التركيب (٤ خطوات، بلا تثبيت أيّ برنامج):
 *   1) Cloudflare Dashboard ← Workers & Pages ← Create ← Worker ← سمِّه nasaq-brain
 *   2) الصق هذا الملفّ كاملاً مكان الكود الافتراضي ثمّ Deploy
 *   3) Settings ← Bindings ← Add ← Workers AI ← Variable name: AI ← Deploy
 *   4) انسخ رابط الـ Worker (https://nasaq-brain.<اسمك>.workers.dev)
 *      والصقه في مربّع «عقل خارجي» داخل تبويب «اسأل نَسَق».
 *
 * متغيّرات اختيارية (Settings ← Variables):
 *   MODEL          اسم موديل بديل. الافتراضي أدناه.
 *   ALLOWED_ORIGIN نطاق واحد مسموح، مثل https://nasaq.pages.dev
 *                  اتركه فارغاً أثناء التجربة من الملفّ المحلّي.
 */

const DEFAULT_MODEL = '@cf/meta/llama-3.1-8b-instruct';

const FALLBACK_SYS =
  'أنت مساعد داخل برنامج «نَسَق» لجدولة المدارس. أجب بالعربية الفصحى وباختصار شديد ' +
  '(٣ أسطر كحدّ أقصى) معتمداً حصراً على بيانات الجدول المرفقة. إن لم تكن المعلومة ' +
  'موجودة فقل: «هذه المعلومة ليست في الجدول الحالي». لا تخترع اسماً ولا رقماً.';

function corsHeaders(env, request) {
  const allowed = (env.ALLOWED_ORIGIN || '').trim();
  const origin = request.headers.get('Origin') || '';
  return {
    'Access-Control-Allow-Origin': allowed || '*',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
    'Vary': 'Origin',
    'Cache-Control': 'no-store',
    ...(allowed && origin && origin !== allowed ? { 'X-Nasaq-Origin': 'blocked' } : {}),
  };
}

const json = (obj, status, headers) =>
  new Response(JSON.stringify(obj), {
    status: status || 200,
    headers: { 'Content-Type': 'application/json; charset=utf-8', ...headers },
  });

async function handle(request, env) {
  const cors = corsHeaders(env, request);
  const model = (env.MODEL || DEFAULT_MODEL).trim();

  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });

  // فحص سريع بالمتصفّح: يفتح الرابط فيرى أنّ العقل حيّ
  if (request.method === 'GET')
    return json({ ok: true, service: 'nasaq-brain', model, ai_binding: !!env.AI }, 200, cors);

  if (request.method !== 'POST')
    return json({ error: 'الطريقة غير مدعومة' }, 405, cors);

  if (cors['X-Nasaq-Origin'] === 'blocked')
    return json({ error: 'هذا النطاق غير مسموح له باستخدام العقل' }, 403, cors);

  if (!env.AI)
    return json({ error: 'ربط Workers AI غير موجود. أضف Binding من نوع Workers AI باسم AI ثمّ أعد النشر.' }, 500, cors);

  let body;
  try { body = await request.json(); }
  catch { return json({ error: 'الطلب ليس JSON صالحاً' }, 400, cors); }

  const question = String(body.question || '').slice(0, 600).trim();
  const context  = String(body.context  || '').slice(0, 14000);
  const system   = String(body.system   || '').slice(0, 2000).trim() || FALLBACK_SYS;
  if (!question) return json({ error: 'لا يوجد سؤال' }, 400, cors);

  try {
    const out = await env.AI.run(model, {
      messages: [
        { role: 'system', content: system },
        { role: 'user', content: 'بيانات الجدول الحالي:\n' + context + '\n\nالسؤال: ' + question },
      ],
      max_tokens: 400,
      temperature: 0.2,
    });
    const answer = String((out && (out.response ?? out.result?.response)) || '').trim();
    if (!answer) return json({ error: 'لم يُرجع النموذج إجابة' }, 502, cors);
    return json({ answer, model }, 200, cors);
  } catch (err) {
    return json({ error: 'تعذّر تشغيل النموذج: ' + (err && err.message ? err.message : String(err)) }, 502, cors);
  }
}

/* Worker مستقلّ */
export default { fetch: (request, env) => handle(request, env) };

/* Pages Function — ضع نسخة من هذا الملفّ في functions/api/ask.js */
export const onRequest = (ctx) => handle(ctx.request, ctx.env);
