
/* ======================= BRAIN (عقل خارجي اختياري) =======================
   يربط «اسأل نَسَق» بنموذج لغة على Cloudflare Workers AI عبر Worker وسيط
   يحتفظ بالمفتاح. بدون رابط، أو عند أيّ فشل، يردّ المحرّك المحلّي كما كان. */
const BKEY='nasaq_brain_v1';
let BRAIN={url:'',on:false}, BSTATE='off', BBUSY=false;

function brainLoad(){try{const r=localStorage.getItem(BKEY);if(r){const o=JSON.parse(r)||{};BRAIN.url=String(o.url||'');BRAIN.on=!!o.on;BSTATE=BRAIN.on?'ok':'off';}}catch(e){}}
function brainStore(){try{localStorage.setItem(BKEY,JSON.stringify(BRAIN));}catch(e){}}

function brainPill(){
  const p=$('#brainState');if(!p)return;
  const MAP={off:['محلّي','rgba(148,163,184,.18)','#94A3B8'],
             busy:['يتصل…','rgba(251,191,36,.18)','#FBBF24'],
             ok:['🧠 متصل','rgba(52,211,153,.18)','#34D399'],
             fail:['فشل — يعمل محلّياً','rgba(248,113,113,.18)','#F87171']};
  const M=MAP[BSTATE]||MAP.off;
  p.textContent=M[0];p.style.background=M[1];p.style.color=M[2];
  const i=$('#brainUrl');if(i&&document.activeElement!==i)i.value=BRAIN.url;
  const b=$('#brainOff');if(b)b.style.display=BRAIN.on?'':'none';
}
function brainSay(t,bad){const m=$('#brainMsg');if(m){m.textContent=t||'';m.style.color=bad?'#F87171':'var(--tx2)';}}

/* لقطة الجدول — بالأسماء كما يسمح بها مستوى الخصوصية الحالي، لا أكثر */
function brainCtx(){
  if(!G)return null;
  const hideT = S.role==='student';
  const L=[];
  L.push('المدرسة: '+NC+' صفوف، '+D+' أيام، '+P+' حصص يومياً. الحصص: '+PN.map((n,i)=>n+' '+TIMES[i]).join(' · '));
  if(!hideT)L.push('مستوى عرض الأسماء: '+PRIV[effPriv()].n+' (الأسماء أدناه معروضة بهذا المستوى، وقد تكون مختصرة أو رموزاً).');
  else L.push('هذا سؤال من طالب أو وليّ أمر: أسماء المعلّمين غير متاحة، أجب عن جدول الصفّ فقط.');
  CLASSES.forEach((c,ci)=>{
    DAYS.forEach((d,di)=>{
      const cells=[];
      for(let p=0;p<P;p++){const s=di*P+p,j=G[ci][s];
        cells.push(PN[p]+' '+SUBJ[j].n+(hideT?'':'/'+TN(tOf(ci,s))));}
      L.push(c+' — '+d+': '+cells.join(' | '));
    });
  });
  if(!hideT){
    L.push('نصاب المعلّمين: '+TEACH.map((t,i)=>TN(i)+'='+t.load).join(' · '));
    const st=S.stats;if(st)L.push('قياسات آخر توليد: تعارضات صلبة='+st.hard+' · زمن التوليد='+(st.ms/1000).toFixed(2)+'ث');
  }
  return L.join('\n');
}

const BRAIN_SYS='أنت مساعد داخل برنامج «نَسَق» لجدولة المدارس في الإمارات. أجب بالعربية الفصحى وباختصار شديد (٣ أسطر كحدّ أقصى) معتمداً حصراً على بيانات الجدول المرفقة. إن لم تكن المعلومة موجودة في البيانات فقل بوضوح: «هذه المعلومة ليست في الجدول الحالي». لا تخترع اسماً ولا رقماً ولا حصّة. الأسماء قد تظهر مختصرة أو كرموز لأسباب خصوصية، فاستخدمها كما وردت ولا تحاول استنتاج الاسم الكامل.';

async function brainCall(q,ms){
  const ctl=new AbortController(),t=setTimeout(()=>ctl.abort(),ms||20000);
  try{
    const r=await fetch(BRAIN.url,{method:'POST',headers:{'Content-Type':'application/json'},
      signal:ctl.signal,body:JSON.stringify({question:q,context:brainCtx()||'',role:S.role,
      privacy:effPriv(),system:BRAIN_SYS})});
    const txt=await r.text();let j={};try{j=JSON.parse(txt);}catch(e){}
    if(!r.ok)throw new Error(j.error||('HTTP '+r.status));
    const a=(j.answer||j.response||'').trim();
    if(!a)throw new Error('لم يرجع العقل إجابة');
    return a;
  } finally { clearTimeout(t); }
}

async function brainConnect(){
  const u=($('#brainUrl').value||'').trim();
  if(!u){brainSay('الصق رابط الـ Worker أوّلاً.',true);return;}
  if(/sk-|api[_-]?key|Bearer/i.test(u)){brainSay('هذا يشبه مفتاحاً لا رابطاً. المفتاح يبقى داخل الـ Worker ولا يوضع هنا.',true);return;}
  BRAIN.url=u;BSTATE='busy';brainPill();brainSay('أختبر الاتصال…');
  try{
    const a=await brainCall('اختبار اتصال: اذكر عدد الصفوف في هذا الجدول فقط.',20000);
    BRAIN.on=true;BSTATE='ok';brainStore();brainPill();
    brainSay('تمّ الربط ✓ — ردّ العقل: '+a.slice(0,120));
    logAccess('ربط عقل خارجي');
    toast('العقل الخارجي متصل 🧠');
  }catch(e){
    BRAIN.on=false;BSTATE='fail';brainPill();
    brainSay('فشل الاتصال: '+(e&&e.message||e)+' — تأكّد من نشر الـ Worker ومن إضافة ربط Workers AI باسم AI. المحرّك المحلّي يعمل كالمعتاد.',true);
  }
}
function brainDisconnect(){BRAIN.on=false;BSTATE='off';brainStore();brainPill();brainSay('فُصل العقل الخارجي. المحرّك المحلّي يعمل وحده الآن.');logAccess('فصل العقل الخارجي');}

/* إجابة مع شارة مصدرها */
function addMsgSrc(t,src){
  const c=$('#chat'),e=document.createElement('div');e.className='msg ai';
  const b=document.createElement('div');
  b.style.cssText='font-size:11px;font-weight:800;opacity:.75;margin-bottom:4px';
  b.textContent=src;e.appendChild(b);
  const s=document.createElement('div');s.textContent=t;e.appendChild(s);
  c.appendChild(e);c.scrollTop=c.scrollHeight;return e;
}

/* يستبدل ask() الأصلية — نفس السلوك تماماً حين لا يوجد عقل مربوط */
function ask(q){
  const i=$('#askIn');q=q||i.value.trim();if(!q)return;
  i.value='';logAccess('سؤال: '+q.slice(0,40));addMsg(q,'me');
  const local=()=>{const a=answer(q);CHAT.push({q,a,r:S.role});if(CHAT.length>30)CHAT.shift();return a;};
  if(!(BRAIN.on&&BRAIN.url)){setTimeout(()=>addMsg(local(),'ai'),300);return;}
  if(BBUSY){setTimeout(()=>addMsg(local(),'ai'),300);return;}
  BBUSY=true;
  const node=addMsgSrc('…','🧠 عقل خارجي');
  brainCall(q).then(a=>{
    node.lastChild.textContent=a;
    CHAT.push({q,a,r:S.role});if(CHAT.length>30)CHAT.shift();
  }).catch(e=>{
    BSTATE='fail';brainPill();
    node.firstChild.textContent='⚙️ محرّك محلّي (تعذّر الوصول للعقل الخارجي)';
    node.lastChild.textContent=local();
  }).finally(()=>{BBUSY=false;$('#chat').scrollTop=$('#chat').scrollHeight;});
}
