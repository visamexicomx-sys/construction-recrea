#!/usr/bin/env python3
"""Taking over stalled, abandoned and half-finished construction projects.

Search volume is small — "unfinished house" 170/mo US, "how to fire a contractor"
170, "construction dispute" 210 (CPC $4.36), "obra abandonada" 30/mo MX. It is
built anyway, and near the top of the priority list, because of who searches it:
an owner whose builder has stopped answering the phone with a large sum already
paid. That person hires within days, and almost nothing on the Mexican Caribbean
addresses them in English.

Two pages, written separately rather than translated, because the two audiences
have different first problems. The English page is for an absentee owner who
cannot see the site and has to establish what actually exists. The Spanish page
is for someone who can stand on the site tomorrow and needs to know what to
secure, what to document and how the permit and the DRO are affected.

Both are deliberately honest about the two things owners least want to hear:
hidden work cannot be verified without opening it, and nobody can warrant
somebody else's structure without testing it first.
"""
import os, re, importlib.util

d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('gsc', os.path.join(d, 'gen-gsc-pages.py'))
gsc = importlib.util.module_from_spec(spec); spec.loader.exec_module(gsc)
spec2 = importlib.util.spec_from_file_location('kw1', os.path.join(d, 'gen-keyword-pages.py'))
kw1 = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(kw1)

EN = dict(lang='en',
  title='Finish a Stalled Construction Project in Mexico',
  desc='Your builder stopped, disappeared or ran out of money. What to do first, how the existing work is audited, what it costs to take over, and what can be warranted.',
  h1='Taking Over a Stalled or Abandoned Construction Project',
  lead='If your builder has stopped answering, the worst thing you can do is nothing — and the second worst is to hire the next person who offers to "just carry on". Here is the order that protects you.',
  secs=[
   ('First: stop paying, then document',
    'Stop all payments immediately, including any that are scheduled automatically. Then document what exists, before anything is moved, cleaned or continued: dated photographs of every area, a written inventory of materials on site, and copies of the contract, every payment receipt, the approved drawings and all correspondence. If a claim ever follows, this is the evidence, and it stops existing the moment someone starts working again. Do this even if you are certain you will never litigate — most owners are, and some of them are wrong.'),
   ('Second: secure the site',
    'An unattended site in this region loses materials, tools and sometimes installed fixtures within weeks. Change the locks, secure the perimeter, arrange somebody to check it, and photograph the inventory before you do. If services are connected, shut off water and gas. If there is an open excavation or an unfinished structure, the site is also a liability — the owner is the one who carries that, not the builder who left.'),
   ('Third: find out what is actually built',
    'This is the part that decides the budget. A technical audit compares what exists against what was paid for and against the approved drawings, and it tests what cannot be seen. Concrete strength can be tested in place. Reinforcement can be located and its cover measured without full demolition. Levels, verticality and dimensions can be checked against the plans. Embedded plumbing can be pressure-tested. What cannot be verified any other way — reinforcement detail inside a poured element, or services already buried — sometimes has to be opened in a small, chosen location. Owners resist that, and it is almost always cheaper than assuming.'),
   ('Fourth: check whether the permit is still alive',
    'A municipal construction licence has a validity period. A project stopped for a long stretch may need it renewed or the situation regularised before work can legally restart, and the municipality may want to see why the work stopped. Separately, the DRO who signed the file may have resigned from the project. A new DRO takes on responsibility for the whole thing, which means they will want testing and documentation before signing — reasonably so. Sorting the permit is not optional paperwork; restarting without it turns a construction problem into an administrative one.'),
   ('What it costs, and why it is not the same rate as new work',
    'Completion always costs less in absolute terms than the whole house, and more per square metre than the same work would have cost in a clean sequence. The reasons are real: unknown hidden work, materials and specifications chosen by someone else, coordination around what already exists, and the risk of later being blamed for defects that were built before we arrived. Any builder who quotes a takeover at their normal rate without an audit is either guessing or planning to renegotiate later.'),
   ('The warranty question, answered honestly',
    'We warrant our own work in full. We cannot warrant a structure someone else poured without verifying it, and verification has limits — some of it requires opening things up, and some of it can only be assessed rather than proven. What we do is state, in writing and before starting, exactly which elements are covered, which have been tested and accepted, and which remain outside the warranty. That document is worth more to you than a broad promise from anyone willing to give one.'),
  ],
  table=('Stage', 'What happens', 'Typical cost',
   [('Technical audit and report', 'Site survey, testing, comparison to drawings', '$25,000 – $80,000 MXN'),
    ('Permit and DRO regularisation', 'Renewal, new DRO, documentation', 'Per municipality'),
    ('Completion works', 'Line-item budget for what remains', 'Quoted after audit'),
    ('Corrective works', 'Fixing what was built wrong', 'Separate line items'),
    ('Takeover premium', 'Unknowns, coordination, risk', 'Typically 10% – 25% over new-build rates')]),
  faq=[('My contractor disappeared with my money. What do I do first?',
        'Stop all payments, document the site with dated photographs before anything is touched, gather your contract and every receipt, and secure the property. Then get a technical audit of what exists. Legal action, if you pursue it, is a separate track from getting the house finished — and it needs that same evidence.'),
       ('Will you take over another builder\'s project?',
        'Yes, after an audit. We do not quote a takeover without establishing what exists, because a number produced without that is fiction and both of us would find out in month two.'),
       ('Can you warrant the work that was already built?',
        'Only what we can verify, and we will tell you in writing which elements those are. Everything we build ourselves carries our full warranty. Anyone who warrants an unverified structure they did not pour is telling you what you want to hear.'),
       ('Is the construction permit still valid if work stopped a year ago?',
        'It may not be. Licences have validity periods and a long stoppage often means renewal or regularisation, sometimes with a new DRO who will require testing before signing. We establish that before quoting, because restarting illegally makes everything worse.'),
       ('Is it cheaper to finish or to demolish and start again?',
        'Almost always cheaper to finish — but not always. When the structure was built without a soils study on poor ground, or the reinforcement is inadequate and widespread, correction can exceed replacement. It is a conclusion of the audit, not an opinion formed on a walk-through.')],
  links=[('/concierge-construction-riviera-maya/', 'Concierge construction service'),
         ('/remote-construction-management-mexico/', 'Managing a build from abroad'),
         ('/home-inspection-mexico/', 'Technical inspection before buying'),
         ('/general-contractor-riviera-maya/', 'General contractor in the Riviera Maya')])

ES = dict(
  title='Terminar una Obra Abandonada o a Medio Construir',
  desc='Su constructor se fue o la obra se detuvo: qué hacer primero, cómo se audita lo construido, qué pasa con la licencia y el DRO, y cuánto cuesta retomarla.',
  h1='Terminar una Obra Abandonada o Detenida',
  lead='Retomar la obra de otro es un trabajo distinto a construir. Lo primero no es cotizar: es saber qué hay realmente construido y en qué estado quedó el expediente.',
  secs=[
   ('Lo primero: detener pagos y documentar',
    'Suspenda cualquier pago pendiente. Después documente lo que existe antes de mover, limpiar o continuar nada: fotografías fechadas de cada área, inventario escrito del material en sitio, y copias del contrato, los recibos, los planos autorizados y toda la comunicación. Si más adelante hay una reclamación, esa evidencia es lo único que la sostiene, y desaparece en cuanto alguien vuelve a trabajar. Hágalo incluso si está seguro de que no va a demandar.'),
   ('Asegurar el predio',
    'Una obra sola pierde material, herramienta y hasta piezas ya instaladas en cuestión de semanas. Cambie cerraduras, cierre el perímetro y consiga quien la revise, fotografiando el inventario antes. Cierre agua y gas si están conectados. Y recuerde que una excavación abierta o una estructura sin terminar es una responsabilidad del propietario, no de quien se fue.'),
   ('La auditoría técnica: lo que decide el presupuesto',
    'Se compara lo construido contra los planos autorizados y contra lo que ya se pagó, y se verifica lo que no está a la vista. La resistencia del concreto se puede ensayar en sitio. El acero se localiza y se mide su recubrimiento sin demoler todo. Niveles, plomos y dimensiones se contrastan con el proyecto. La instalación hidráulica se prueba a presión. Lo que no se puede verificar de otra forma —el armado dentro de un elemento ya colado, instalaciones ya ahogadas— a veces se abre en un punto elegido. Es incómodo y sale mucho más barato que suponer.'),
   ('Licencia, DRO y expediente',
    'La licencia municipal tiene vigencia. Una obra detenida mucho tiempo puede requerir renovación o regularización antes de reanudar, y el municipio puede preguntar por qué se detuvo. Además, el DRO que firmó pudo haber renunciado al proyecto: el que entre asume la responsabilidad de todo lo anterior, así que va a pedir pruebas y documentación antes de firmar, y hace bien. Reanudar sin resolver esto convierte un problema de obra en un problema administrativo.'),
   ('Por qué retomar cuesta distinto',
    'Terminar cuesta menos en total que la casa completa, y más por metro cuadrado que si esa misma obra se hubiera hecho en secuencia limpia. Las razones son reales: trabajo oculto desconocido, materiales y especificaciones que eligió otro, coordinación alrededor de lo que ya existe, y el riesgo de que después se nos atribuyan defectos anteriores a nuestra llegada. Quien cotice retomar una obra a su precio normal y sin auditoría, está adivinando o piensa renegociar después.'),
   ('Garantía: lo que sí y lo que no',
    'Garantizamos por completo lo que hacemos nosotros. No podemos garantizar una estructura que coló otro sin verificarla, y la verificación tiene límites. Lo que sí hacemos es dejar por escrito, antes de empezar, qué elementos quedan cubiertos, cuáles se probaron y aceptaron, y cuáles quedan fuera. Ese documento vale más que una garantía amplia de quien esté dispuesto a darla sin haber probado nada.'),
  ],
  table=('Etapa', 'Qué incluye', 'Costo orientativo',
   [('Auditoría técnica con informe', 'Levantamiento, ensayos, cotejo con planos', '$25,000 – $80,000 MXN'),
    ('Regularización de licencia y DRO', 'Renovación, nuevo DRO, documentación', 'Según municipio'),
    ('Obra de terminación', 'Presupuesto por partidas de lo que falta', 'Se cotiza tras la auditoría'),
    ('Trabajos correctivos', 'Reparar lo que quedó mal ejecutado', 'Partidas independientes'),
    ('Sobrecosto por retomar', 'Incertidumbre, coordinación, riesgo', 'Del 10% al 25% sobre obra nueva')]),
  faq=[('Mi constructor abandonó la obra, ¿qué hago primero?',
        'Suspenda pagos, documente el sitio con fotos fechadas antes de tocar nada, reúna contrato y recibos, y asegure el predio. Después, auditoría técnica de lo construido. La vía legal, si decide seguirla, corre aparte de terminar la casa y se apoya en esa misma evidencia.'),
       ('¿Retoman obras empezadas por otro constructor?',
        'Sí, después de auditar. No cotizamos una obra retomada sin establecer qué existe realmente: un número sin eso es ficción y ambos lo descubriríamos al segundo mes.'),
       ('¿Garantizan lo que ya estaba construido?',
        'Solo lo que podamos verificar, y lo dejamos por escrito elemento por elemento. Todo lo que construimos nosotros lleva garantía completa. Quien garantice sin haber probado nada le está diciendo lo que quiere oír.'),
       ('¿Sigue vigente mi licencia de construcción?',
        'Puede que no. Las licencias tienen vigencia y una interrupción larga suele implicar renovación o regularización, a veces con un DRO nuevo que pedirá pruebas antes de firmar. Lo revisamos antes de cotizar.'),
       ('¿Conviene terminar o demoler y empezar de nuevo?',
        'Casi siempre conviene terminar, pero no siempre. Si se construyó sin estudio de suelos sobre terreno malo, o el armado es insuficiente de forma generalizada, corregir puede costar más que reponer. Eso lo concluye la auditoría, no una visita.')],
  links=[('/supervision-de-obra/', 'Supervisión de obra'),
         ('/contrato-de-obra/', 'Contrato de obra: cláusulas clave'),
         ('/mecanica-de-suelos/', 'Mecánica de suelos'),
         ('/permisos-licencias-construccion-riviera-maya/', 'Permisos y licencias')])


if __name__ == '__main__':
    os.chdir(d)
    en_slug = 'finish-stalled-construction-project-mexico'
    os.makedirs(en_slug, exist_ok=True)
    html = gsc.build(en_slug, EN, 'en')
    open(os.path.join(en_slug, 'index.html'), 'w', encoding='utf-8').write(html)
    w = len(re.sub(r'<[^>]+>', ' ', html[html.index('<h1>'):html.index('<footer')]).split())
    print('%-46s T%2d D%3d words %4d' % (en_slug + '/', len(EN['title']), len(EN['desc']), w))

    es_slug = 'terminar-obra-abandonada-riviera-maya'
    os.makedirs(es_slug, exist_ok=True)
    src = open(kw1.TPL, encoding='utf-8').read()
    html2 = kw1.build(es_slug, ES, src)
    open(os.path.join(es_slug, 'index.html'), 'w', encoding='utf-8').write(html2)
    w2 = len(re.sub(r'<[^>]+>', ' ', html2[html2.index('<h1>'):html2.index('<footer')]).split())
    print('%-46s T%2d D%3d words %4d' % (es_slug + '/', len(ES['title']), len(ES['desc']), w2))

    a = re.sub(r'<[^>]+>', ' ', html[html.index('<h1>'):html.index('<footer')]).lower().split()
    b = re.sub(r'<[^>]+>', ' ', html2[html2.index('<h1>'):html2.index('<footer')]).lower().split()
    sa = set(tuple(a[i:i + 6]) for i in range(len(a) - 5))
    sb = set(tuple(b[i:i + 6]) for i in range(len(b) - 5))
    print('cross-language overlap: %.3f (expected ~0, they are not translations)' % (len(sa & sb) / len(sa | sb)))
