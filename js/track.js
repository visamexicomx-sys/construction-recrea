(function(){
  function ev(name,p){if(typeof gtag==='function')gtag('event',name,p||{});}
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;
    var h=a.getAttribute('href')||'';
    if(h.indexOf('wa.me/')>-1||h.indexOf('api.whatsapp.com')>-1)ev('whatsapp_click',{link_url:h,link_text:(a.textContent||'').trim().slice(0,60)});
    else if(h.indexOf('tel:')===0)ev('phone_click',{link_url:h});
    else if(h.indexOf('mailto:')===0)ev('email_click',{link_url:h});
  },true);
  document.addEventListener('submit',function(e){
    var f=e.target;if(f&&f.tagName==='FORM')ev('generate_lead',{form_action:f.getAttribute('action')||''});
  },true);
})();
