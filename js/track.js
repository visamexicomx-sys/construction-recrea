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
