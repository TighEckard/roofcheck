/* Bedrock Roof site script. 1) Cookieless first-party visit stats (same format as the Riside tracker), 2) quote form, 3) city headline. */
(function(){
var SB='https://yhsxxblilclylzgejehk.supabase.co',KEY='sb_publishable_9BiONVmj8Ht4k7lBsxGkkA_Yajbl8Rj',P='/roofing';
var nav=navigator,ua=nav.userAgent||'',w=window,d=document;
function ga(n,p){try{if(w.gtag)w.gtag('event',String(n).replace(/[^a-z0-9_]+/gi,'_').slice(0,40),p||{})}catch(e){}}
w.RTga=ga;
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
if(/[?&]notrack/.test(location.search)){ls('no_track','1')}
d.addEventListener('click',function(x){var a=x.target.closest&&x.target.closest('[data-optout]');if(a){x.preventDefault();ls('no_track','1');a.textContent='Tracking is off on this device.'}});
if(w.TRK&&!ls('no_track')&&!ls('t_notice')&&!(nav.doNotTrack==='1'||nav.globalPrivacyControl)){w.addEventListener('DOMContentLoaded',function(){var b=d.createElement('div');b.className='tnote';b.setAttribute('role','region');b.setAttribute('aria-label','Analytics notice');b.innerHTML='Analytics &amp; recordings on. <a href="/privacy/">Privacy</a> &middot; <a href="/privacy/?notrack" data-optout>Opt out</a> <button type="button" data-ok aria-label="Close">OK</button>';d.body.appendChild(b);var y0=w.pageYOffset;w.addEventListener('scroll',function sc(){if(Math.abs(w.pageYOffset-y0)>120){ls('t_notice','1');if(b.parentNode)b.remove();w.removeEventListener('scroll',sc)}},{passive:true});d.addEventListener('focusin',function(e){if(e.target.closest&&e.target.closest('[data-form]')&&b.parentNode)b.remove()});b.querySelector('[data-ok]').onclick=function(){ls('t_notice','1');b.remove()};b.querySelector('[data-optout]').addEventListener('click',function(){ls('t_notice','1');setTimeout(function(){b.remove()},800)})})}

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
d.addEventListener('click',function(x){var a=x.target.closest&&x.target.closest('a');if(!a)return;var hr=a.getAttribute('href')||'';if(/^tel:/.test(hr)){ev('call:'+hr);ga('phone_click',{link_url:hr})}else if(/^mailto:/.test(hr)){ev('email:'+hr);ga('email_click',{link_url:hr})}else if(/get-quotes/.test(hr)||/btn/.test(a.className)){ga('quote_button_click',{link_text:(a.textContent||'').trim().slice(0,60),page:location.pathname})}},true);
d.addEventListener('visibilitychange',function(){if(d.visibilityState==='hidden'){if(vis){shown+=Date.now()-start;vis=false}leave();shown=0}else if(!vis){vis=true;start=Date.now()}});
w.addEventListener('pagehide',flush);
w.RT.ev=function(n){ev(n);flush();ga(n)};
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
var need=(f.querySelector('input[name=need]:checked')||{}).value||'';var prop=(f.querySelector('input[name=prop]:checked')||{}).value||'home';if(prop!=='home')need=(prop==='commercial'?'COMMERCIAL ':'MULTIFAMILY/HOA ')+need;
var nm=v('n'),ph=v('p').replace(/\D/g,'').replace(/^1(?=\d{10}$)/,''),zip=v('a').replace(/\D/g,''),note=v('m');
var bad=[];if(nm.length<2)bad.push('your name');if(ph.length!==10)bad.push('a 10-digit mobile number');if(zip.length!==5)bad.push('a 5-digit ZIP code');
if(bad.length){er.textContent='Please enter '+bad.join(', ')+'.';er.hidden=false;if(RT.ev)RT.ev('form:invalid '+bad.length);return}
er.hidden=true;if(RT.ev)RT.ev('form:submit_attempt');b.disabled=true;b.textContent='Sending...';
var mail=fetch('https://formsubmit.co/ajax/hello@bedrockroof.com',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({_subject:'New Bedrock Roof lead: '+need+' '+zip,_template:'table',_captcha:'false',Name:nm,Phone:ph,ZIP:zip,Need:need,Note:note,Page:location.pathname,Source:RT.src})}).then(function(r){if(!r.ok)throw 0;return r}).catch(function(){if(RT.ev)RT.ev('form:email_failed');throw 0});
var db=fetch(U,{method:'POST',headers:{apikey:K,'Content-Type':'application/json',Prefer:'return=minimal'},
body:JSON.stringify({name:(nm+' | ZIP '+zip+' | '+need+(note?' | '+note:'')).slice(0,100),email:ph+'@roofing.lead',slot:'roofing',source:(RT.src+'|'+(RT.vid||'').slice(0,12)+'|'+location.pathname).slice(0,79)})}).then(function(r){if(!r.ok)throw 0;return r});
Promise.all([db.then(function(){return 1},function(){return 0}),mail.then(function(){return 1},function(){return 0})]).then(function(ok){if(!ok[0]&&!ok[1])throw 0;return {ok:true}}).then(function(r){if(!r.ok)throw 0;if(RT.ev)RT.ev('form:submitted');if(window.RTga)window.RTga('generate_lead',{page:location.pathname,need:need});f.hidden=true;box.hidden=false;box.scrollIntoView({behavior:'smooth',block:'center'})})
.catch(function(){if(RT.ev)RT.ev('form:submit_failed');b.disabled=false;b.textContent='Get my free quote';er.textContent='Something went wrong. Please try again.';er.hidden=false})});
});
var h=document.querySelector('[data-city]');if(!h)return;
function set(c){if(c&&/^[\p{L}\s.'-]{2,40}$/u.test(c))h.textContent='Need a new roof in '+c+'? Get a free quote from a local roofer.'}
var c=null;try{c=sessionStorage.getItem('h_city')}catch(e){}if(c){set(c);return}
try{fetch('https://ipwho.is/?fields=success,country_code,city').then(function(r){return r.json()}).then(function(j){if(j&&j.success&&j.country_code==='US'&&j.city){try{sessionStorage.setItem('h_city',j.city)}catch(e){}set(j.city)}}).catch(function(){})}catch(e){}
})();

(function(){var b=document.querySelector('[data-mbar]');if(!b)return;var f=document.getElementById('quote');
if(/^\/get-quotes\//.test(location.pathname)){b.remove();return}
if(f){b.setAttribute('href','#quote');b.addEventListener('click',function(e){e.preventDefault();f.scrollIntoView({behavior:'smooth',block:'start'});var i=f.querySelector('input[name=n]');if(i)setTimeout(function(){i.focus({preventScroll:true})},500)});
if('IntersectionObserver' in window){new IntersectionObserver(function(es){es.forEach(function(e){b.classList.toggle('off',e.isIntersecting)})}).observe(f)}}
b.addEventListener('click',function(){if(window.RT&&window.RT.ev)window.RT.ev('mbar:click');if(window.RTga)window.RTga('quote_button_click',{link_text:'sticky bar',page:location.pathname})});})();

(function(){var f=document.getElementById('quote');if(!f)return;document.querySelectorAll('.top .btn,.cta .btn').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();f.scrollIntoView({behavior:'smooth',block:'start'});var i=f.querySelector('input[name=n]');if(i)setTimeout(function(){i.focus({preventScroll:true})},500)})})})();
