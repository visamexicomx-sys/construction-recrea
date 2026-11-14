(function(){
  function ev(name,p){if(typeof gtag==='function')gtag('event',name,p||{});}
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;
    var h=a.getAttribute('href')||'';
    if(h.indexOf('wa.me/')>-1||h.indexOf('api.whatsapp.com')>-1)ev('whatsapp_click',{link_url:h,link_text:(a.textContent||'').trim().slice(0,60)});
    else if(h.indexOf('tel:')===0)ev('phone_click',{link_url:h});
    else if(h.indexOf('mailto:')===0)ev('email_click',{link_url:h});
  },true);
  var CRM='https://recrea.v.frappe.cloud/api/method/frappe.website.doctype.web_form.web_form.accept';
  function val(f,n){var x=f.querySelector('[name="'+n+'"]');return x&&x.value?String(x.value).trim():'';}
  function toCRM(f){
    try{
      if(val(f,'_honey'))return;
      var name=val(f,'name'),phone=val(f,'phone'),email=val(f,'email');
      if(!name||!(phone||email))return;
      var extra=[['Tipo',val(f,'project_type')],['Ubicación',val(f,'location')],['Servicio',val(f,'service_type')]].filter(function(x){return x[1];}).map(function(x){return x[0]+': '+x[1];});
      var msg=val(f,'message');if(extra.length)msg=(msg?msg+'\n':'')+extra.join('\n');
      var h1=document.querySelector('h1');
      var d={doctype:'Lead',web_form_name:'solicitud-web',first_name:name.slice(0,140),mobile_no:phone.slice(0,40),email_id:email.slice(0,140),
        utm_source:'Sitio web',custom_message:msg.slice(0,2000),custom_service:(h1?h1.textContent.trim():document.title).slice(0,140),
        custom_zone:location.pathname.replace(/^\/|\/$/g,'').slice(0,140),custom_project_size:(val(f,'size')||val(f,'area')).slice(0,140),
        custom_site_lang:(document.documentElement.lang||'').slice(0,10),custom_page_url:location.href.split('#')[0].slice(0,140),
        custom_utm:((location.search||'')+' | ref: '+(document.referrer||'')).slice(0,500)};
      if(!d.email_id)delete d.email_id;
      fetch(CRM,{method:'POST',mode:'no-cors',keepalive:true,headers:{'Content-Type':'application/x-www-form-urlencoded'},
        body:'web_form=solicitud-web&data='+encodeURIComponent(JSON.stringify(d))});
    }catch(err){}
  }
  var PRIV={es:['Al enviar acepta el ','aviso de privacidad','/aviso-de-privacidad/'],en:['By sending you accept the ','privacy notice','/privacy-notice/'],
    ru:['Отправляя форму, вы принимаете ','политику конфиденциальности','/privacy-notice/'],de:['Mit dem Absenden akzeptieren Sie den ','Datenschutzhinweis','/privacy-notice/'],
    fr:['En envoyant, vous acceptez la ','politique de confidentialité','/privacy-notice/'],zh:['提交即表示您同意','隐私声明','/privacy-notice/']};
  function consent(){
    var t=PRIV[(document.documentElement.lang||'es').slice(0,2)]||PRIV.en;
    document.querySelectorAll('form.contact-form').forEach(function(f){
      if(f.querySelector('[data-priv]'))return;
      var p=document.createElement('p');p.className='small text-muted mt-2 mb-0 text-center';p.setAttribute('data-priv','1');
      p.appendChild(document.createTextNode(t[0]));var a=document.createElement('a');a.href=t[2];a.textContent=t[1];p.appendChild(a);
      f.appendChild(p);
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',consent);else consent();
  document.addEventListener('submit',function(e){
    var f=e.target;if(f&&f.tagName==='FORM'){ev('generate_lead',{form_action:f.getAttribute('action')||''});if(/contact-form/.test(f.className))toCRM(f);}
  },true);
})();
/* Instagram card: shows once the visitor reaches the 3rd screen (scroll > 2 viewports); dismiss hides it for 7 days. Not on the homepages. */
(function(){
  var p=location.pathname;
  if(/^\/((en|es|de|ru|fr|zh|mx)\/)?(index\.html)?$/.test(p)||/^\/pt\/home-portugues\/?/.test(p))return;
  var URL='https://www.instagram.com/recrea_arquitectura',K='ig_card_hide',shown=false;
  try{var t=+localStorage.getItem(K);if(t&&Date.now()-t<7*864e5)return;}catch(e){}
  var L=(document.documentElement.lang||'en').slice(0,2);
  var T={en:['See our projects on Instagram','Villas, condos and renovations from the Riviera Maya: before and after, site progress and finished homes.','Follow @recrea_arquitectura'],
         es:['Vea nuestras obras en Instagram','Villas, departamentos y remodelaciones en la Riviera Maya: antes y después, avance de obra y casas terminadas.','Seguir @recrea_arquitectura'],
         de:['Unsere Projekte auf Instagram','Villen, Apartments und Renovierungen an der Riviera Maya: vorher und nachher, Baufortschritt, fertige Häuser.','@recrea_arquitectura folgen'],
         fr:['Nos chantiers sur Instagram','Villas, appartements et rénovations sur la Riviera Maya : avant/après, avancement et maisons livrées.','Suivre @recrea_arquitectura'],
         ru:['Наши объекты в Instagram','Виллы, квартиры и ремонты на Ривьере-Майя: до и после, ход стройки и готовые дома.','Подписаться @recrea_arquitectura'],
         zh:['在 Instagram 上看我们的项目','里维埃拉玛雅的别墅、公寓与翻新：前后对比、施工进度与完工作品。','关注 @recrea_arquitectura'],
         pt:['Veja nossas obras no Instagram','Villas, apartamentos e reformas na Riviera Maya: antes e depois, andamento e casas prontas.','Seguir @recrea_arquitectura']}[L]||null;
  T=T||['See our projects on Instagram','Villas, condos and renovations from the Riviera Maya.','Follow @recrea_arquitectura'];
  function show(){
    if(shown)return;shown=true;
    var d=document.createElement('div');d.id='ig-card';d.setAttribute('role','dialog');d.setAttribute('aria-label',T[0]);
    d.style.cssText='position:fixed;right:16px;bottom:16px;z-index:1080;max-width:340px;width:calc(100% - 32px);background:#fff;color:#222;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.25);padding:16px 16px 14px;font-size:14px;line-height:1.4;transform:translateY(20px);opacity:0;transition:all .35s ease';
    d.innerHTML='<button type="button" aria-label="Close" style="position:absolute;top:6px;right:10px;border:0;background:none;font-size:22px;line-height:1;color:#888;cursor:pointer">&times;</button>'+
      '<div style="display:flex;gap:12px;align-items:center;margin-bottom:8px"><span style="flex:0 0 44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 30% 107%,#fdf497 0%,#fd5949 45%,#d6249f 60%,#285AEB 90%)">'+
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4zM17.3 5.5a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4zM12 2c-2.7 0-3 0-4.1.1-1 0-1.8.2-2.4.5-.7.3-1.2.6-1.8 1.2S2.9 5 2.6 5.6c-.3.6-.5 1.4-.5 2.4C2 9 2 9.3 2 12s0 3 .1 4.1c0 1 .2 1.8.5 2.4.3.7.6 1.2 1.2 1.8s1.1.9 1.8 1.2c.6.3 1.4.5 2.4.5 1 .1 1.4.1 4.1.1s3 0 4.1-.1c1 0 1.8-.2 2.4-.5.7-.3 1.2-.6 1.8-1.2s.9-1.1 1.2-1.8c.3-.6.5-1.4.5-2.4.1-1 .1-1.4.1-4.1s0-3-.1-4.1c0-1-.2-1.8-.5-2.4-.3-.7-.6-1.2-1.2-1.8S19 2.9 18.4 2.6c-.6-.3-1.4-.5-2.4-.5C15 2 14.7 2 12 2zm0 1.8c2.7 0 3 0 4 .1.9 0 1.5.2 1.8.3.5.2.8.4 1.1.7.4.4.6.7.7 1.1.1.3.3.9.3 1.8.1 1 .1 1.4.1 4s0 3-.1 4c0 .9-.2 1.5-.3 1.8-.2.5-.4.8-.7 1.1-.4.4-.7.6-1.1.7-.3.1-.9.3-1.8.3-1 .1-1.4.1-4 .1s-3 0-4-.1c-.9 0-1.5-.2-1.8-.3-.5-.2-.8-.4-1.1-.7-.4-.4-.6-.7-.7-1.1-.1-.3-.3-.9-.3-1.8-.1-1-.1-1.4-.1-4s0-3 .1-4c0-.9.2-1.5.3-1.8.2-.5.4-.8.7-1.1.4-.4.7-.6 1.1-.7.3-.1.9-.3 1.8-.3 1-.1 1.3-.1 4-.1z"/></svg></span>'+
      '<strong style="font-size:15px;padding-right:18px">'+T[0]+'</strong></div><p style="margin:0 0 12px;color:#555">'+T[1]+'</p>'+
      '<a href="'+URL+'" target="_blank" rel="noopener" style="display:block;text-align:center;padding:10px 12px;border-radius:10px;color:#fff;font-weight:600;text-decoration:none;background:linear-gradient(90deg,#f58529,#dd2a7b,#8134af)">'+T[2]+'</a>';
    document.body.appendChild(d);
    requestAnimationFrame(function(){d.style.transform='none';d.style.opacity='1';});
    d.querySelector('button').onclick=function(){try{localStorage.setItem(K,Date.now());}catch(e){}d.remove();if(typeof gtag==='function')gtag('event','instagram_card_close');};
    d.querySelector('a').onclick=function(){try{localStorage.setItem(K,Date.now());}catch(e){}if(typeof gtag==='function')gtag('event','instagram_click',{link_url:URL,source:'ig_card'});};
    if(typeof gtag==='function')gtag('event','instagram_card_view');
  }
  function onScroll(){if(window.scrollY>window.innerHeight*2){show();window.removeEventListener('scroll',onScroll);}}
  window.addEventListener('scroll',onScroll,{passive:true});
})();
