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
  /* After formsubmit emails the lead, it redirects (_next) to WhatsApp with the lead pre-filled, so it lands in Recrea's chat. */
  var WA='529844525333';
  var WT={es:['Hola Recrea, acabo de enviar una solicitud desde su sitio web:','Nombre','Teléfono','Email','Tipo','Ubicación','Tamaño (m²)','Mensaje','Página'],
    en:['Hi Recrea, I just sent a request from your website:','Name','Phone','Email','Type','Location','Size (m²)','Message','Page'],
    ru:['Здравствуйте, Recrea! Я отправил заявку с вашего сайта:','Имя','Телефон','Email','Тип','Локация','Площадь (м²)','Сообщение','Страница'],
    de:['Hallo Recrea, ich habe gerade eine Anfrage über Ihre Website gesendet:','Name','Telefon','E-Mail','Art','Ort','Fläche (m²)','Nachricht','Seite'],
    fr:['Bonjour Recrea, je viens d\'envoyer une demande depuis votre site :','Nom','Téléphone','E-mail','Type','Lieu','Surface (m²)','Message','Page'],
    zh:['您好 Recrea，我刚通过网站提交了需求：','姓名','电话','邮箱','类型','地点','面积 (m²)','留言','页面']};
  function toWA(f){
    try{
      if(val(f,'_honey')||!val(f,'name'))return;
      var t=WT[(document.documentElement.lang||'es').slice(0,2)]||WT.en;
      var rows=[[1,'name'],[2,'phone'],[3,'email'],[4,'project_type'],[5,'location'],[6,'size'],[7,'message']].map(function(r){var v=val(f,r[1])||(r[1]==='project_type'?val(f,'service_type'):r[1]==='size'?val(f,'area'):'');return v?t[r[0]]+': '+v.slice(0,600):'';}).filter(Boolean);
      var h1=document.querySelector('h1');
      rows.push(t[8]+': '+(h1?h1.textContent.trim().slice(0,90)+' — ':'')+location.href.split(/[?#]/)[0]);
      var url='https://wa.me/'+WA+'?text='+encodeURIComponent(t[0]+'\n\n'+rows.join('\n'));
      var n=f.querySelector('input[name="_next"]');
      if(!n){n=document.createElement('input');n.type='hidden';n.name='_next';f.appendChild(n);}
      n.value=url;ev('whatsapp_lead_redirect',{page:location.pathname});
    }catch(err){}
  }
  document.addEventListener('submit',function(e){
    var f=e.target;if(f&&f.tagName==='FORM'){ev('generate_lead',{form_action:f.getAttribute('action')||''});if(/contact-form/.test(f.className)){toCRM(f);toWA(f);}}
  },true);
})();
/* Round Instagram button next to the WhatsApp and email floats, on every page. */
(function(){
  var URL='https://www.instagram.com/recrea_arquitectura',m=window.innerWidth<=480;
  var n=(document.querySelector('.whatsapp-float')?1:0)+(document.querySelector('.email-float')?1:0);
  var a=document.createElement('a');a.href=URL;a.target='_blank';a.rel='noopener';a.className='ig-float';a.setAttribute('aria-label','Instagram @recrea_arquitectura');
  var s=m?50:62;
  a.style.cssText='position:fixed;bottom:'+(m?16:26)+'px;right:'+((m?16:26)+n*(m?60:70))+'px;width:'+s+'px;height:'+s+'px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;text-decoration:none;z-index:9998;transition:transform .3s;background:radial-gradient(circle at 30% 107%,#fdf497 0%,#fd5949 45%,#d6249f 60%,#285AEB 90%);box-shadow:0 4px 15px rgba(214,36,159,.4)';
  a.innerHTML='<svg width="'+(m?22:28)+'" height="'+(m?22:28)+'" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1.1.4 2.2.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1.1.4-2.2.4-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1.1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1.1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 4.7a5.1 5.1 0 1 0 0 10.2 5.1 5.1 0 0 0 0-10.2zm0 8.4a3.3 3.3 0 1 1 0-6.6 3.3 3.3 0 0 1 0 6.6zm5.3-9.8a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4z"/></svg>';
  a.onmouseenter=function(){a.style.transform='scale(1.1)';};a.onmouseleave=function(){a.style.transform='';};
  a.onclick=function(){if(typeof gtag==='function')gtag('event','instagram_click',{link_url:URL,source:'ig_float'});};
  function add(){document.body.appendChild(a);}
  document.body?add():document.addEventListener('DOMContentLoaded',add);
})();
