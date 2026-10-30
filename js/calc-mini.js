(function(){
  function money(n){return '$'+(Math.round(n/100)*100).toLocaleString('en-US');}
  document.querySelectorAll('[data-calc]').forEach(function(box){
    var spec;try{spec=JSON.parse(box.getAttribute('data-calc'));}catch(e){return;}
    var out=box.querySelector('[data-out]');
    function run(){
      var lo=0,hi=0,open=false;
      (spec.lines||[]).forEach(function(l){
        var el=box.querySelector('[name="'+l.from+'"]');if(!el)return;
        var q=parseFloat((box.querySelector('[name="'+l.qty+'"]')||{}).value||1)||0;
        if(el.type==='checkbox'){if(!el.checked)return;var o=l.opts[0];}
        else var o=l.opts[el.type==='hidden'?0:(parseInt(el.value,10)||0)];if(!o)return;
        if(o.tiers){var t=o.tiers.filter(function(t){return q<=t[0];})[0];if(!t){open=true;return;}lo+=t[1];hi+=t[2];return;}
        var m=o.pct?q/100:(o.fixed?1:q);
        lo+=o.min*m;if(o.max==null)open=true;else hi+=o.max*m;
      });
      if(!lo&&open){out.textContent=spec.ask;return;}
      out.textContent=money(lo)+(open?'+':' – '+money(hi))+' MXN';
    }
    box.addEventListener('input',run);box.addEventListener('change',run);run();
  });
})();
