/* Bedrock Roof site script. 1) Cookieless first-party visit stats (same format as the Riside tracker), 2) quote form, 3) city headline. */
(function(){
var SB='https://yhsxxblilclylzgejehk.supabase.co',KEY='sb_publishable_9BiONVmj8Ht4k7lBsxGkkA_Yajbl8Rj',P='/roofing';
var nav=navigator,ua=nav.userAgent||'',w=window,d=document;
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
function ss(k,v){try{if(v===undefined)return sessionStorage.getItem(k);sessionStorage.setItem(k,v)}catch(e){return null}}
var rid=function(){return Math.random().toString(36).slice(2,10)+Date.now().toString(36)};
var vid=ls('v_id'),isNew=!vid;if(isNew){vid=rid();ls('v_id',vid)}
var sid=ss('s_id'),now=Date.now();if(!sid||now-(+ss('s_ts')||0)>18e5){sid=rid();ss('s_id',sid)}ss('s_ts',String(now));
var q=new URLSearchParams(location.search),h='';
try{h=d.referrer?new URL(d.referrer).hostname.replace(/^www\./,''):''}catch(e){}
if(h===location.hostname.replace(/^www\./,''))h='';
var src=(q.get('utm_source')||q.get('src')||'').toLowerCase();
if(!src&&q.get('fbclid'))src='facebook';
if(!src&&h)src=/facebook\.com$|fb\.com$/.test(h)?'facebook':/instagram\.com$/.test(h)?'instagram':/google\./.test(h)?'google':/bing\.com$/.test(h)?'bing':/nextdoor\.com$/.test(h)?'nextdoor':/(^|\.)t\.co$|twitter\.com$|x\.com$/.test(h)?'x':/youtube\.com$/.test(h)?'youtube':/reddit\.com$/.test(h)?'reddit':h;
src=('bedrock-'+(src||'direct')).slice(0,60);
w.RT={vid:vid,src:src};
if(w.top!==w.self||nav.webdriver||/bot|crawl|spider|slurp|headless|lighthouse|preview|facebookexternalhit/i.test(ua)||nav.doNotTrack==='1'||nav.globalPrivacyControl||ls('no_track')||/[?&]notrack/.test(location.search))return;
var device=/iPad|Tablet/.test(ua)||(/Android/.test(ua)&&!/Mobile/.test(ua))?'tablet':/Mobi|iPhone|Android/.test(ua)?'mobile':'desktop';
var browser=/FBAN|FBAV/.test(ua)?'Facebook app':/Instagram/.test(ua)?'Instagram app':/Edg\//.test(ua)?'Edge':/OPR\//.test(ua)?'Opera':/Firefox|FxiOS/.test(ua)?'Firefox':/Chrome|CriOS/.test(ua)?'Chrome':/Safari/.test(ua)?'Safari':'Other';
var os=/Windows/.test(ua)?'Windows':/iPhone|iPad|iPod/.test(ua)?'iOS':/Android/.test(ua)?'Android':/Mac OS/.test(ua)?'macOS':/CrOS/.test(ua)?'ChromeOS':/Linux/.test(ua)?'Linux':'Other';
var buf=[],timer,depth=0,start=Date.now(),shown=0,vis=true,clicks=0,started=false;
function push(e){buf.push(e);clearTimeout(timer);timer=setTimeout(flush,3000)}
function flush(){if(!buf.length)return;var b=buf;buf=[];try{fetch(SB+'/rest/v1/analytics_events',{method:'POST',keepalive:true,headers:{apikey:KEY,'Content-Type':'application/json',Prefer:'return=minimal'},body:JSON.stringify(b)}).catch(function(){})}catch(e){}}
function base(t){return {vid:vid,sid:sid,type:t,path:P}}
function ev(name){var e=base('click');e.el=name.slice(0,80);e.vw=w.innerWidth;push(e)}
function measure(){var de=d.documentElement,H=Math.max(de.scrollHeight,d.body.scrollHeight);depth=Math.max(depth,Math.min(100,(w.pageYOffset+w.innerHeight)/H*100))}
function leave(){var t=shown+(vis?Date.now()-start:0);var e=base('scroll');e.depth=Math.round(depth);e.dur=Math.min(t,36e5);push(e);flush()}
w.addEventListener('scroll',function(){if(!w._at){w._at=1;requestAnimationFrame(function(){w._at=0;measure()})}},{passive:true});
var fseen={};
d.addEventListener('focusin',function(e){var t=e.target;if(t.tagName!=='INPUT')return;if(!started){started=true;ev('form:started '+t.id)}if(!fseen['f'+t.id]){fseen['f'+t.id]=1;ev('form:focus '+t.id)}});
d.addEventListener('input',function(e){var t=e.target;if(t.tagName==='INPUT'&&!fseen['t'+t.id]){fseen['t'+t.id]=1;ev('form:typing '+t.id)}});
d.addEventListener('focusout',function(e){var t=e.target;if(t.tagName==='INPUT'&&t.value.trim()&&!fseen['d'+t.id]){fseen['d'+t.id]=1;ev('form:filled '+t.id)}});
d.addEventListener('click',function(x){if(clicks>=60)return;clicks++;var el=x.target.closest&&x.target.closest('a,button,label,input');var de=d.documentElement,W=Math.max(de.scrollWidth,de.clientWidth);var e=base('click');e.x=Math.max(0,Math.min(1000,Math.round(x.pageX/W*1000)));e.y=Math.round(x.pageY);e.vw=w.innerWidth;e.el=el?(el.tagName.toLowerCase()+':'+(el.id||(el.textContent||'').trim())).slice(0,60):null;push(e)},true);
d.addEventListener('visibilitychange',function(){if(d.visibilityState==='hidden'){if(vis){shown+=Date.now()-start;vis=false}leave();shown=0}else if(!vis){vis=true;start=Date.now()}});
w.addEventListener('pagehide',flush);
w.RT.ev=function(n){ev(n);flush()};
function enter(g){measure();var e=base('view');e.src=src;e.ref_host=h.slice(0,100)||null;e.utm_medium=(q.get('utm_medium')||'').slice(0,100)||null;e.utm_campaign=(q.get('utm_campaign')||('page:'+location.pathname)).slice(0,100);e.new_visitor=isNew;e.device=device;e.browser=browser;e.os=os;e.vw=w.innerWidth;e.vh=w.innerHeight;if(g){e.country=g.country;e.region=g.region;e.city=g.city}push(e)}
var c=ss('s_geo');if(c){try{return enter(JSON.parse(c))}catch(e){}}
var done=false,fin=function(g){if(!done){done=true;enter(g)}};setTimeout(function(){fin(null)},1500);
try{fetch('https://ipwho.is/?fields=success,country,region,city').then(function(r){return r.json()}).then(function(j){var g=null;if(j&&j.success){g={country:(j.country||'').slice(0,60)||null,region:(j.region||'').slice(0,80)||null,city:(j.city||'').slice(0,80)||null};ss('s_geo',JSON.stringify(g))}fin(g)}).catch(function(){fin(null)})}catch(e){fin(null)}
})();

(function(){
var U='https://yhsxxblilclylzgejehk.supabase.co/rest/v1/signups',K='sb_publishable_9BiONVmj8Ht4k7lBsxGkkA_Yajbl8Rj';
document.querySelectorAll('[data-form]').forEach(function(f){
var box=f.parentNode.querySelector('.okbox'),er=f.querySelector('.err'),b=f.querySelector('button');
f.addEventListener('submit',function(e){e.preventDefault();var RT=window.RT||{src:'bedrock-direct',vid:''};
var v=function(n){return (f.elements[n].value||'').trim()};
var need=(f.querySelector('input[name=need]:checked')||{}).value||'';
var nm=v('n'),ph=v('p').replace(/\D/g,'').replace(/^1(?=\d{10}$)/,''),zip=v('a').replace(/\D/g,''),note=v('m');
var bad=[];if(nm.length<2)bad.push('your name');if(ph.length!==10)bad.push('a 10-digit mobile number');if(zip.length!==5)bad.push('a 5-digit ZIP code');
if(bad.length){er.textContent='Please enter '+bad.join(', ')+'.';er.hidden=false;if(RT.ev)RT.ev('form:invalid '+bad.length);return}
er.hidden=true;if(RT.ev)RT.ev('form:submit_attempt');b.disabled=true;b.textContent='Sending...';
fetch(U,{method:'POST',headers:{apikey:K,'Content-Type':'application/json',Prefer:'return=minimal'},
body:JSON.stringify({name:(nm+' | ZIP '+zip+' | '+need+(note?' | '+note:'')).slice(0,100),email:ph+'@roofing.lead',slot:'roofing',source:(RT.src+'|'+(RT.vid||'').slice(0,12)+'|'+location.pathname).slice(0,79)})})
.then(function(r){if(!r.ok)throw 0;if(RT.ev)RT.ev('form:submitted');f.hidden=true;box.hidden=false;box.scrollIntoView({behavior:'smooth',block:'center'})})
.catch(function(){if(RT.ev)RT.ev('form:submit_failed');b.disabled=false;b.textContent='Get my free quote';er.textContent='Something went wrong. Please try again.';er.hidden=false})});
});
var h=document.querySelector('[data-city]');if(!h)return;
function set(c){if(c&&/^[\p{L}\s.'-]{2,40}$/u.test(c))h.textContent='Need a new roof in '+c+'? Get a free quote from a local roofer.'}
var c=null;try{c=sessionStorage.getItem('h_city')}catch(e){}if(c){set(c);return}
try{fetch('https://ipwho.is/?fields=success,country_code,city').then(function(r){return r.json()}).then(function(j){if(j&&j.success&&j.country_code==='US'&&j.city){try{sessionStorage.setItem('h_city',j.city)}catch(e){}set(j.city)}}).catch(function(){})}catch(e){}
})();
