#!/usr/bin/env python3
"""Fourth depth pass, batch 2 of 3: the French tail, 25 pages (2026-08-15).

All at 1-4 impressions. Written in French rather than translated: the register of
a French construction text is not the register of a Spanish one, and a machine
pass through either produces something a French reader recognises instantly as
not written for them.
"""
import os, re

OPEN, CLOSE = '<div data-depth="2026-08">', '</div><!--/depth-->'


def sec(h, p):
    return '<h2 class="mt-4">%s</h2>\n<p>%s</p>\n' % (h, p)


def tbl(head, rows):
    return ('<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr>'
            + ''.join('<th>%s</th>' % h for h in head) + '</tr></thead><tbody>\n'
            + '\n'.join('<tr>' + ''.join('<td>%s</td>' % c for c in r) + '</tr>' for r in rows)
            + '\n</tbody></table></div>\n')


B = {

'blog-fr/assurances-garanties-construction.html':
 sec('Trois couvertures que l\'on confond souvent',
     'La tous risques chantier, qui couvre l\'ouvrage pendant les travaux. La responsabilité civile du constructeur, '
     'qui couvre les dommages aux tiers. Et la couverture des ouvriers. Ce sont trois choses distinctes, et le contrat '
     'doit les nommer séparément, avec des attestations en cours de validité que vous puissiez consulter avant le début '
     'du chantier.')
 + sec('La garantie des vices cachés',
     'Elle doit être écrite : ce qu\'elle couvre, pour combien de temps, et comment la déclarer. Une « garantie » sans '
     'durée ni périmètre n\'en est pas une. Et aucun constructeur sérieux ne garantit une structure coulée par un autre '
     'sans l\'avoir vérifiée — point important si vous reprenez un chantier commencé.')
 + sec('Ce qui fait aboutir une réclamation',
     'Photos datées de l\'avancement, résultats d\'essais, journal de chantier et procès-verbal de réception avec '
     'réserves. Ce dossier est ce qui soutient une réclamation ; sans lui, la discussion se réduit à une parole contre '
     'une autre.'),

'blog-fr/calculateur-roi-airbnb-tulum-playa.html':
 sec('Calculez sur les coûts réels, pas sur le brut',
     'Entre les réservations brutes et ce qui vous revient, l\'écart est plus large que la plupart des projections. La '
     'gestion prend 15% à 30% du brut, le ménage se facture par séjour, les commissions de plateforme sont prélevées '
     'avant versement, la climatisation tourne en continu pendant les séjours, et s\'ajoutent piscine, jardin, '
     'réapprovisionnement, assurance et une réserve d\'entretien que ce climat rend obligatoire.')
 + sec('Le segment le plus encombré',
     'Les petits appartements vendus sur une projection de rendement sont ceux qui se concurrencent le plus. Quand des '
     'dizaines de biens quasi identiques visent le même voyageur, l\'ajustement n\'apparaît pas d\'abord dans les prix '
     'de vente mais dans le taux d\'occupation et les remises. Demandez toujours quelle occupation suppose la '
     'projection qu\'on vous présente, puis comparez avec ce que réalisent réellement des annonces comparables.')
 + sec('Construire pour la location, pas pour soi',
     'Eau chaude suffisante en pleine occupation, climatisation dimensionnée pour le nombre réel de voyageurs, surfaces '
     'qui supportent la rotation, assez d\'assises pour la capacité annoncée, rangement pour le linge. Cela se décide '
     'au programme, pas après les premiers commentaires.'),

'blog-fr/casita-maison-invites-revenus-locatifs.html':
 sec('Vérifier la densité avant de dessiner',
     'La bescheinigung d\'usage du sol indique combien de logements la parcelle autorise, ainsi que l\'emprise au sol et '
     'la surface constructible. Une casita constituant un logement indépendant avec sa propre cuisine n\'est pas '
     'automatiquement permise, et dans un lotissement fermé le règlement intérieur l\'interdit souvent, quelle que soit '
     'la position de la municipalité.')
 + sec('Pourquoi le coût au m² est plus bas',
     'Ce qui coûte cher dans une maison, ce sont la cuisine, les salles de bains, les réseaux et la viabilisation. Une '
     'casita partage la parcelle, les raccordements et souvent la piscine : le coût marginal de 40 à 60 m² est bien '
     'inférieur à celui d\'une construction isolée de même surface.')
 + sec('Le calcul honnête de la location',
     'Le rendement sur l\'extension dépasse en général celui de la maison principale. Ce qu\'il vous en coûte, c\'est '
     'de l\'intimité et de la gestion : des voyageurs sur votre terrain, des ménages entre séjours, et la conformité — '
     'accès séparé, sécurité, enregistrement et fiscalité. À décider avant de bâtir.'),

'blog-fr/checklist-saison-cyclonique-mexique.html':
 sec('Avant la saison : ce qui doit être fait en juin',
     'Élaguer les arbres susceptibles de tomber sur la toiture. Vérifier volets ou vitrage anti-impact et les fermer '
     'une fois entièrement, pour s\'assurer qu\'ils fonctionnent. Nettoyer tous les évacuations et gouttières. '
     'Photographier la propriété et stocker les images hors site : c\'est votre dossier auprès de l\'assureur. Et '
     'relire la police sur deux points — la couverture de la submersion marine et le montant de la franchise, qui est '
     'en général un pourcentage de la valeur assurée.')
 + sec('Quand une tempête est nommée',
     'Sécuriser ou rentrer mobilier de jardin, parasols et tout ce qui est mobile. Baisser le niveau de la piscine sans '
     'la vider. Couper le gaz. Protéger les ouvertures. Sauvegarder les documents importants. Si vous n\'êtes pas au '
     'Mexique, cela suppose quelqu\'un sur place avec les clés et l\'autorisation d\'agir — accord à prendre en amont, '
     'pas quand la tempête porte déjà un nom.')
 + sec('Après : l\'ordre correct',
     'Documenter d\'abord, réparer provisoirement ensuite. Les mesures conservatoires sont généralement remboursables, '
     'mais seulement si l\'état initial a été consigné. Contrôler toiture et évacuations avant la pluie suivante, pas '
     'lorsque l\'humidité devient visible.'),

'blog-fr/climatisation-ventilation-riviera-maya.html':
 sec('Le bon dimensionnement fait baisser la facture',
     'Un appareil surdimensionné refroidit vite, s\'arrête, et laisse l\'air humide faute de déshumidifier : la maison '
     'paraît froide et collante, et la consommation grimpe à cause des cycles. Sous-dimensionné, il tourne sans arrêt. '
     'Le calcul se fait sur la surface, l\'orientation, la hauteur, le vitrage, l\'isolation et l\'occupation réelle — '
     'pas sur une règle générale au mètre carré.')
 + sec('Inverter, gainable ou split',
     'Les appareils inverter modulent au lieu de démarrer et s\'arrêter : consommation nettement inférieure et '
     'température stable, ce qui les rentabilise dans un climat où la climatisation fonctionne presque toute l\'année. '
     'Le split par zone permet de ne refroidir que l\'utile. Le gainable donne un meilleur rendu, à condition de '
     'concevoir les reprises d\'air — omission fréquente qui laisse des chambres jamais climatisées.')
 + sec('Le condensat, cause n°1 de sinistre',
     'Si l\'évacuation des condensats se bouche, l\'eau trouve le faux plafond. Pente correcte, regard accessible et '
     'nettoyage régulier : dix minutes d\'entretien contre un plafond taché et un chantier de reprise.'),

'blog-fr/construction-restaurant-bar-riviera-maya.html':
 sec('Ce sont les réseaux qui font le projet',
     'Extraction dimensionnée pour la cuisine réelle, bac à graisses conforme, alimentation gaz avec sécurités, '
     'puissance électrique et tableau adaptés aux équipements, eau chaude en quantité, et évacuation qui respecte le '
     'traitement des eaux exigé dans la région. Les finitions se voient ; ce sont les réseaux qui décident si '
     'l\'établissement ouvre à la date prévue.')
 + sec('La date d\'ouverture est le budget',
     'Chaque semaine de retard a un coût que l\'exploitant chiffre précisément. D\'où : commandes longues passées avant '
     'la démolition, corps d\'état séquencés pour se chevaucher là où c\'est possible, et administration du centre '
     'commercial ou bailleur associé avant l\'arrivée des équipes.')
 + sec('Autorisations et protection civile',
     'Usage du sol compatible avec l\'activité, licence de construction ou d\'aménagement, avis de protection civile, '
     'et exigences sanitaires propres à la restauration. En galerie commerciale, ajoutez l\'accord de l\'administration, '
     'qui exige souvent plans, assurances et horaires avant toute intervention.'),

'blog-fr/construction-villa-luxe-playacar.html':
 sec('Playacar impose son propre règlement',
     'Comité de conception qui examine le projet avant la municipalité, reculs et hauteurs plus stricts, palette de '
     'matériaux et de couleurs, horaires de chantier, contrôle d\'accès pour le personnel et les véhicules, délai '
     'maximal avec dépôt de garantie. Tout cela est opposable et modifie autant la conception que le budget. À vérifier '
     'avant de dessiner.')
 + sec('Ce qui distingue une villa de luxe d\'une grande maison',
     'Pas les mètres carrés : la spécification et les réseaux. Menuiseries structurelles à contrôle solaire, '
     'ébénisterie sur mesure en bois denses, quincaillerie inox partout en extérieur, éclairage par couches avec '
     'scénarios, climatisation dimensionnée sur charge réelle et silencieuse, piscine à débordement avec équipement '
     'surdimensionné, et un back-office invisible : local technique, buanderie, stockage, accès de service.')
 + sec('Coûts 2026', 'Par m² construit à Playacar, hors mobilier et paysagisme.')
 + tbl(['Niveau', 'Ce que cela implique', 'Coût par m²'],
       [['Haut résidentiel', 'Bonnes finitions locales', '$25,000 – $32,000 MXN'],
        ['Luxe', 'Spécification importée, sur mesure', '$32,000 – $48,000 MXN'],
        ['Villa d\'auteur', 'Matériaux singuliers', 'À partir de $48,000 MXN']]),

'blog-fr/construire-maison-retraite-riviera-maya.html':
 sec('Concevoir pour la personne que vous serez dans vingt ans',
     'Plain-pied, ou au minimum une chambre et une salle de bains complète au rez-de-chaussée. Passages libres de 90 cm. '
     'Douche sans ressaut avec espace de rotation. Aucune marche isolée, ni dedans ni à l\'entrée. Couloirs praticables '
     'avec un déambulateur. Et, si la maison a un étage, une gaine d\'ascenseur laissée en placard : la créer maintenant '
     'coûte peu, la percer plus tard suppose de couper des dalles.')
 + sec('Ce qui compte plus que le plan : les charges',
     'Un budget de retraite est fixe ; la facture d\'électricité ici ne l\'est pas. Orientation, ventilation traversante, '
     'verre à contrôle solaire, isolation et climatisation bien dimensionnée décident si la maison coûte peu ou beaucoup '
     'à maintenir confortable. Le solaire modifie encore ce calcul. Ce sont des décisions de chantier, impossibles à '
     'rattraper au même prix ensuite.')
 + sec('Questions pratiques à trancher avant',
     'Distance à un hôpital que vous utiliseriez réellement, et à un aéroport international pour les visites. Le '
     'quartier vit-il à l\'année ou se vide-t-il hors saison. Couverture santé décidée en amont. Et qui entretient la '
     'maison si vous voyagez plusieurs mois : sous ce climat, une maison inoccupée se dégrade vite.'),

'blog-fr/cout-de-la-vie-playa-del-carmen-2026.html':
 sec('Le poste qui surprend : l\'électricité',
     'Les tarifs de la CFE sont progressifs, et franchir la tranche haute change la facture brutalement. Une maison '
     'climatisée pendant l\'été caribéen, avec pompe de piscine, vit exactement à cette limite. C\'est la plus grande '
     'variable du budget domestique ici, et celle que les choix de construction améliorent le plus.')
 + sec('Ce que coûte l\'entretien d\'une maison, pas son achat',
     'Au-delà de l\'électricité : eau, gaz, internet, taxe foncière, assurance, entretien de piscine, jardin, et une '
     'réserve d\'entretien que ce climat rend non négociable. Si le bien est loué, ajoutez gestion et ménages.')
 + tbl(['Poste', 'Fourchette mensuelle', 'Remarque'],
       [['Électricité', '$2,500 – $10,000 MXN', 'Les tranches pénalisent la clim'],
        ['Eau', '$200 – $800 MXN', 'Faible selon les standards européens'],
        ['Gaz', '$500 – $1,500 MXN', 'Citerne de GPL'],
        ['Internet', '$500 – $1,200 MXN', 'Fibre où elle existe'],
        ['Piscine', '$1,500 – $4,000 MXN', 'Service hebdomadaire'],
        ['Jardin', '$2,000 – $6,000 MXN', 'La pousse surprend les nouveaux venus']]),

'blog-fr/cout-entretien-maison-mexique.html':
 sec('Ce que ce climat fait à une maison inoccupée',
     'L\'humidité trouve chaque espace fermé et non ventilé et le transforme en moisissure. La climatisation à '
     'l\'arrêt pendant des mois laisse cela se propager ; laissée en marche sans surveillance, un condensat bouché '
     'inonde un plafond. La chimie de la piscine s\'effondre en quelques jours sans entretien. Le sel corrode la '
     'quincaillerie en continu. Rien de spectaculaire au premier mois ; tout devient coûteux au sixième.')
 + sec('Le calendrier qui compte vraiment',
     'Hebdomadaire : piscine, jardin, et une visite avec photos. Mensuel : faire couler chaque robinet et tirer chaque '
     'chasse pour garder les siphons pleins, vérifier les condensats, tester la pompe. Trimestriel : filtres et '
     'batteries de climatisation, quincaillerie, joints. Annuel : étanchéité avant les pluies, évacuations, contrôle '
     'électrique, entretien des pompes.')
 + tbl(['Service', 'Fréquence', 'Coût 2026'],
       [['Piscine', 'Hebdomadaire', '$1,500 – $4,000 MXN/mois'],
        ['Jardin', 'Hebdo ou bimensuel', '$2,000 – $6,000 MXN/mois'],
        ['Visite avec rapport photo', 'Hebdomadaire', '$1,500 – $3,500 MXN/mois'],
        ['Entretien climatisation', 'Trimestriel', '$800 – $2,000 MXN/appareil']]),

'blog-fr/delais-construction-riviera-maya.html':
 sec('La réponse honnête, en deux parties',
     'Sept à onze mois de chantier pour une maison de 150 à 200 m², une fois le permis obtenu. Mais l\'horloge qui '
     'compte démarre plus tôt : vérifications du terrain, conception, études et dossier de permis ajoutent deux à six '
     'mois, davantage lorsqu\'un dossier environnemental s\'applique. De la décision aux clés, comptez douze à '
     'vingt-quatre mois en incluant l\'achat du terrain.')
 + sec('Ce qui retarde réellement',
     'Le dossier environnemental à Tulum et près des zones protégées. Les fondations, quand l\'étude de sol révèle des '
     'cavités — ou quand il n\'y a pas eu d\'étude et que la découverte se fait en pleine excavation. Les pluies de '
     'septembre-octobre, surtout pour terrassements et coulages. Les finitions importées commandées trop tard, retard '
     'le plus fréquent et le plus évitable. Et les avenants décidés après la structure.')
 + tbl(['Étape', 'Durée typique', 'Remarque'],
       [['Études et conception', '6 – 12 semaines', 'Étude de sol comprise'],
        ['Permis et DRO', '3 – 10 semaines', 'Plus long avec dossier environnemental'],
        ['Fondations', '4 – 8 semaines', 'Excavation en roche'],
        ['Structure et dalles', '8 – 14 semaines', ''],
        ['Réseaux et enveloppe', '6 – 12 semaines', ''],
        ['Finitions et réception', '10 – 16 semaines', '']]),

'blog-fr/domotique-maison-connectee-riviera-maya.html':
 sec('Ce qui vaut vraiment la peine ici',
     'Le pilotage de la climatisation par zone, là où se trouve la dépense réelle ; l\'éclairage par scénarios ; le '
     'portail et le contrôle d\'accès ; l\'arrosage automatique sectorisé ; caméras et détecteurs d\'ouverture ; et la '
     'détection de fuite d\'eau, qui dans une maison inoccupée plusieurs mois vaut plus que tout le reste de la liste.')
 + sec('Câbler maintenant, équiper plus tard',
     'Les appareils se remplacent tous les quelques années ; les fourreaux non. Prévoyez le câblage réseau aux points '
     'clés, la place au tableau, l\'alimentation aux accès et l\'emplacement des détecteurs. Vous pourrez alors changer '
     'de technologie sans rouvrir les murs — précisément là où part le budget quand on domotise après coup.')
 + sec('Internet, coupures et réalité locale',
     'Un système entièrement dépendant du cloud cesse de fonctionner quand internet ou le courant tombe, et les deux '
     'arrivent ici. Choisissez des équipements conservant un contrôle local, et prévoyez un onduleur pour le routeur et '
     'les accès.'),

'blog-fr/etrangers-construire-maison-mexique.html':
 sec('La propriété d\'abord, la construction ensuite',
     'Dans la zone côtière restreinte, un étranger détient via une fiducie bancaire (fideicomiso) ou une société '
     'mexicaine. Ce n\'est ni un bail ni un montage fragile : c\'est le mécanisme standard depuis des décennies, et '
     'vous conservez l\'usage, la location, la vente et la transmission. Le vrai risque d\'un achat au Mexique n\'est '
     'presque jamais la fiducie : c\'est le titre, le statut du terrain et les documents derrière.')
 + sec('Les permis ne dépendent pas de votre nationalité',
     'Ils s\'attachent au bien et au projet. Le dossier est déposé par le propriétaire ou par le DRO en son nom. Ce qui '
     'change pour un étranger, c\'est la logistique : procuration si vous ne pouvez être présent, documents traduits et '
     'apostillés le cas échéant, et un interlocuteur qui répond dans votre langue.')
 + sec('Construire à distance, concrètement',
     'Prix ferme sur devis par poste, paiements liés à des jalons vérifiables, rapports hebdomadaires avec photos '
     'datées, visioconférence aux étapes qui seront recouvertes, et validation écrite de chaque avenant. Rien '
     'd\'accepté oralement sur le chantier ne devient une facture.'),

'blog-fr/fideicomiso-etrangers-acheter-mexique.html':
 sec('Ce qu\'est réellement la fiducie',
     'Une banque mexicaine détient le titre en qualité de fiduciaire ; vous êtes bénéficiaire et conservez tous les '
     'droits pratiques : occuper, rénover, louer, vendre, transmettre. La banque ne peut ni vendre ni grever le bien. '
     'Le dispositif existe parce que la Constitution restreint la propriété étrangère directe à environ 50 km des '
     'côtes — et toutes les villes balnéaires de cette côte sont dans cette zone.')
 + sec('Coûts, durée et succession',
     'Une mise en place à la signature, puis des frais annuels de fiducie tant que vous détenez le bien. Le contrat '
     'court sur 50 ans et se renouvelle : c\'est une formalité administrative, pas une renégociation. Les bénéficiaires '
     'substitués que vous désignez héritent directement des droits, ce qui évite la procédure successorale mexicaine — '
     'avantage largement sous-estimé.')
 + tbl(['Poste', 'Nature', 'Ordre de grandeur'],
       [['Mise en place', 'Permis, banque, notaire', '$1,500 – $3,000 USD'],
        ['Frais annuels', 'Fiduciaire', '$500 – $900 USD/an'],
        ['Frais d\'acquisition', 'Droits, notaire, registre', '5% – 8% du prix'],
        ['Durée', 'Renouvelable', '50 ans']]),

'blog-fr/gestion-locative-riviera-maya.html':
 sec('Ce qu\'une gestion sérieuse doit inclure',
     'Accueil et communication voyageurs, ménages entre séjours avec contrôle qualité, blanchisserie, réapprovisionnement, '
     'maintenance de premier niveau avec plafond de dépense autorisé par écrit, entretien piscine et jardin coordonné, '
     'et un reporting mensuel lisible : occupation, revenu brut, prélèvements, net.')
 + sec('Comment se rémunère la gestion, et ce qui doit alerter',
     'Un pourcentage du brut, de 15% à 30% selon l\'étendue du service. Méfiez-vous d\'une commission prélevée sur les '
     'réparations : elle incite à réparer davantage. Demandez des devis tiers pour tout travail significatif, et une '
     'clause de sortie raisonnable.')
 + sec('Ce que la gestion ne remplace pas',
     'Un bien mal conçu pour la location reste mal noté quel que soit le gestionnaire : eau chaude insuffisante, '
     'climatisation sous-dimensionnée, matériaux qui ne supportent pas la rotation. La gestion optimise ce qui existe ; '
     'elle ne corrige pas une erreur de programme.'),

'blog-fr/maison-connectee-sous-tropiques.html':
 sec('L\'humidité et le sel avant la technologie',
     'Sous ce climat, les équipements électroniques exposés vieillissent vite : boîtiers extérieurs mal étanches, '
     'contacts oxydés, capteurs saturés d\'humidité. Choisissez du matériel avec un indice de protection réel pour '
     'l\'extérieur, placez les organes sensibles à l\'abri, et prévoyez une ventilation du coffret technique.')
 + sec('Les fonctions utiles, dans l\'ordre',
     'Détection de fuite d\'eau. Pilotage de la climatisation par zone. Contrôle d\'accès et portail. Éclairage par '
     'scénarios. Arrosage sectorisé. Caméras. C\'est l\'ordre du retour sur investissement dans une maison qui reste '
     'parfois vide plusieurs mois.')
 + sec('Prévoir maintenant ce qui coûtera cher plus tard',
     'Fourreaux et câblage réseau, place au tableau, alimentations aux accès, et un onduleur pour routeur et portail. '
     'Les appareils changeront ; l\'infrastructure, non.'),

'blog-fr/maison-deux-etages-riviera-maya.html':
 sec('Quand deux niveaux se justifient',
     'Terrain restreint avec envie de jardin ou de piscine, recherche de vues, ou emprise au sol limitée alors que la '
     'hauteur est permise. À l\'inverse, si vous envisagez de vieillir dans la maison sans prévoir d\'ascenseur, si le '
     'terrain permet un plain-pied confortable, ou si le budget est juste, un seul niveau est plus rationnel.')
 + sec('Ce qui renchérit l\'étage',
     'Dalle intermédiaire et son ferraillage, poteaux et poutres dimensionnés pour la charge, escalier — de 18 000 à '
     '55 000 MXN selon le type —, remontées de réseaux, et souvent des fondations plus robustes. Le mètre carré à '
     'l\'étage coûte à peu près comme au rez-de-chaussée, mais l\'ensemble monte parce que la structure travaille plus.')
 + sec('Le détail que presque personne ne prévoit',
     'Laisser la gaine d\'un futur ascenseur, utilisée entre-temps en placard. Peu coûteux pendant le chantier, cela '
     'évite de couper des dalles plus tard.'),

'blog-fr/marche-immobilier-tulum-2026.html':
 sec('Ce que l\'aéroport a changé, et ce qui a suivi',
     'L\'accès a changé, et l\'accès change un marché : arrivées directes plus nombreuses, saison plus longue, '
     'clientèle plus large. C\'est réel. Ce qui a suivi, c\'est une vague de construction, largement composée de petits '
     'appartements visant exactement le même acheteur locatif, commercialisés avec des projections écrites pour vendre '
     'des lots plutôt que pour décrire le marché.')
 + sec('Où l\'offre a dépassé la demande',
     'Les petites unités en résidence dense, vendues sur le rendement, constituent le segment le plus encombré. '
     'L\'ajustement se lit d\'abord dans l\'occupation et les remises, pas dans les prix affichés. Les villas privées '
     'avec extérieur réel et intimité relèvent d\'un autre marché, bien moins concurrentiel.')
 + sec('Évaluer sans se raconter d\'histoires',
     'Demandez l\'hypothèse d\'occupation de toute projection et confrontez-la aux annonces comparables. Retranchez les '
     'charges complètes : gestion 15% à 30% du brut, ménages, électricité avec climatisation, piscine, jardin, '
     'assurance, réserve d\'entretien de 1% à 2% de la valeur par an.'),

'blog-fr/meilleures-zones-construire-playa-del-carmen.html':
 sec('Ce qui distingue réellement les quartiers',
     'La distance à pied de la Quinta et de la plage, le bruit nocturne, le niveau d\'inondation lors des fortes '
     'pluies, la maturité des services, et la présence d\'une population à l\'année plutôt que saisonnière. Deux '
     'quartiers identiques un après-midi de février se comportent très différemment en septembre.')
 + sec('Lotissement fermé ou quartier ouvert',
     'Le lotissement apporte sécurité, entretien des communs et un cadre préservé, au prix d\'un règlement qui '
     'contraint votre projet : reculs, hauteurs, matériaux, horaires de chantier, délais. Le quartier ouvert laisse plus '
     'de liberté de conception et vous confie l\'entretien de tout ce qui est à vous.')
 + sec('Ce qu\'il faut vérifier avant d\'acheter, quel que soit le quartier',
     'Usage du sol et densité, emprise et surface constructible, hauteur, et si une partie du terrain touche une zone '
     'protégée ou fédérale. Puis relevé topographique et étude de sol. Ces vérifications coûtent une fraction de ce que '
     'coûte une mauvaise parcelle.'),

'blog-fr/panneaux-solaires-riviera-maya.html':
 sec('Ici, l\'économie se mesure contre la climatisation',
     'Les tarifs de la CFE sont progressifs et franchir la tranche haute change la facture d\'un coup. Une maison '
     'climatisée avec pompe de piscine vit à cette frontière, et c\'est là qu\'un système bien dimensionné modifie le '
     'plus le budget annuel. Dimensionnez sur douze mois de consommation réelle, pas sur la surface de toiture '
     'disponible.')
 + sec('Le comptage net, et ce qu\'il faut comprendre avant',
     'L\'excédent injecté est compensé, il ne vous est pas payé comme une vente d\'énergie, et le dispositif a ses '
     'règles et ses délais. Surdimensionner pour produire bien au-delà de sa consommation est rarement rentable. Couvrir '
     'correctement sa propre consommation, et prévoir l\'extension, l\'est.')
 + sec('Ce que ce climat impose au matériel',
     'Sel, humidité et poussière réduisent le rendement sans nettoyage ; la saison cyclonique impose une fixation '
     'calculée, pas simplement posée ; et l\'ombre pèse plus que l\'orientation — un palmier qui prend deux mètres peut '
     'coûter une part notable de production. Structures et visserie en inox ou aluminium, pas en acier galvanisé '
     'ordinaire.'),

'blog-fr/planning-construction-mois-par-mois.html':
 sec('Ce qui se passe réellement, mois par mois',
     'Les étapes se chevauchent : les réseaux commencent quand la structure finit, les finitions quand les réseaux sont '
     'testés. Le total est donc plus court que la somme. Ce qui ne se chevauche pas, c\'est le permis : rien de légitime '
     'ne commence avant.')
 + tbl(['Phase', 'Contenu', 'Durée typique'],
       [['Études et conception', 'Relevé, sol, architecture, structure', '6 – 12 semaines'],
        ['Permis et DRO', 'Dossier municipal', '3 – 10 semaines'],
        ['Terrassement et fondations', 'Excavation en roche, semelles', '4 – 8 semaines'],
        ['Structure et dalles', 'Poteaux, poutres, planchers', '8 – 14 semaines'],
        ['Réseaux et enveloppe', 'Électricité, plomberie, clim, étanchéité', '6 – 12 semaines'],
        ['Finitions et réception', 'Sols, menuiseries, réserves', '10 – 16 semaines']])
 + sec('Protéger le planning',
     'Étude de sol avant de figer la conception. Commandes longues passées dès l\'approbation du projet. Spécification '
     'arrêtée avant le coulage de la dalle. Paiements liés aux jalons pour que le calendrier ait une conséquence '
     'financière. Et un planning remis comme document daté, avec dépendances — pas comme une phrase dans une offre.'),

'blog-fr/playa-del-carmen-ou-tulum-construire-2026.html':
 sec('Deux logiques différentes, pas deux versions de la même',
     'Playa del Carmen : profondeur des corps d\'état et des fournisseurs, hôpitaux, écoles, aéroport à 45 minutes, et '
     'des délais de chantier plus courts parce que tout est disponible localement. Tulum : la marque la plus forte de '
     'la côte et l\'instruction la plus stricte — le dossier environnemental est une barrière réelle, et les barrières '
     'protègent ce qui est déjà autorisé.')
 + sec('Ce que cela change pour votre budget et votre calendrier',
     'Le coût de construction varie modérément entre les deux ; les délais d\'autorisation, beaucoup. À Tulum, prévoyez '
     'des mois pour l\'environnemental lorsqu\'il s\'applique, et un traitement des eaux plus exigeant en terrain '
     'karstique. À Playa, la contrainte est plutôt l\'impact viaire et le règlement de lotissement.')
 + sec('Et pour la location',
     'La concurrence diffère davantage que les coûts. Le petit appartement locatif est saturé à Tulum ; la villa privée '
     'avec extérieur réel se situe dans un marché nettement plus mince, des deux côtés.'),

'blog-fr/sols-finitions-climat-tropical.html':
 sec('Ce que ce climat inflige à un sol',
     'Humidité élevée toute l\'année, sable qui agit comme abrasif, sel en bord de mer, et eau qui entre depuis la '
     'terrasse à chaque forte pluie. Cela élimine des matériaux parfaitement valables en climat sec : bois tendres non '
     'traités, stratifiés bas de gamme qui gonflent par les chants, et toute finition suspendue à un vernis que '
     'personne ne renouvellera.')
 + sec('Ce qui fonctionne, pièce par pièce',
     'Grès cérame à faible absorption presque partout, en version antidérapante sur les terrasses. Chukum et béton lissé '
     'pour la continuité, avec joints de fractionnement bien placés. Pierre locale en extérieur, texturée là où l\'on '
     'marche mouillé. Bois durs tropicaux ou composite en terrasse, toujours sur lambourdes ventilées.')
 + sec('Le détail décisif : le joint',
     'Sur un sol continu, les joints de fractionnement évitent que la surface choisisse elle-même où fissurer. En grès '
     'cérame, le joint absorbe la dilatation d\'une terrasse au soleil. Et à la jonction intérieur-extérieur, larmier et '
     'pente empêchent l\'eau d\'entrer par vent de travers. La plupart des réclamations portent sur le joint ou la '
     'pente, pas sur le matériau.'),

'blog-fr/systemes-dessalement-riviera-maya.html':
 sec('Quand le dessalement a du sens, et quand il n\'en a pas',
     'Il en a lorsqu\'il n\'existe ni réseau ni puits exploitable, typiquement sur des parcelles isolées en bord de '
     'mer. Il n\'en a pas lorsqu\'un raccordement municipal est possible ou qu\'un puits est autorisé : l\'osmose '
     'inverse consomme de l\'énergie en continu, exige des membranes remplacées périodiquement et une maintenance '
     'sérieuse. Ce n\'est pas une commodité, c\'est une petite installation industrielle.')
 + sec('Ce que cela suppose réellement',
     'Prise d\'eau et prétraitement, pompage haute pression, membranes, poste de reminéralisation, et gestion du '
     'concentré rejeté — ce dernier point étant précisément celui que l\'autorité environnementale examine sur cette '
     'côte. Ajoutez l\'alimentation électrique dimensionnée et, en site isolé, un groupe de secours.')
 + sec('L\'alternative que l\'on oublie',
     'Récupération des eaux de pluie avec stockage suffisant. Sous ce régime de précipitations, une toiture de 100 m² '
     'rend de l\'ordre de 80 000 à 110 000 litres par an, ce qui couvre l\'essentiel des usages non potables. Souvent '
     'plus pertinent, et infiniment plus simple, qu\'une unité de dessalement.'),

'blog-fr/train-maya-impact-immobilier.html':
 sec('Ce qu\'une infrastructure change, et ce qu\'elle ne change pas',
     'Elle change l\'accessibilité, et l\'accessibilité déplace la demande vers des zones jusque-là périphériques. Elle '
     'ne transforme pas un terrain mal situé en bon terrain, et elle ne valide pas une projection de rendement. Les '
     'gains se concentrent là où l\'infrastructure raccourcit réellement un trajet que les gens font.')
 + sec('Comment l\'intégrer à une décision d\'achat',
     'Comme un facteur parmi d\'autres, après l\'usage du sol, la densité, la topographie, le sol et les services. Un '
     'terrain proche d\'une gare mais sans usage compatible avec votre projet reste inutilisable. Et acheter sur '
     'l\'annonce d\'un équipement futur revient à prendre un risque, pas à faire un plan.')
 + sec('Ce que nous observons sur nos chantiers',
     'Une demande de construction plus soutenue le long des axes améliorés, et une concurrence accrue pour la '
     'main-d\'œuvre qualifiée quand de grands travaux publics tournent en parallèle. Les deux se répercutent dans les '
     'délais plus que dans les prix unitaires.'),
}


def insert(path, block):
    s = open(path, encoding='utf-8').read()
    s = re.sub(re.escape(OPEN) + r'.*?' + re.escape(CLOSE), '', s, flags=re.S)
    payload = OPEN + '\n' + block + CLOSE + '\n'
    m = (re.search(r'\n[ \t]*<h2[^>]*>\s*(Questions fréquentes|FAQ)', s)
         or re.search(r'\n[ \t]*<div class="cta-section', s)
         or re.search(r'\n[ \t]*<section data-cluster=', s))
    at = (s.rfind('\n', 0, m.start() + 1) + 1) if m else s.rfind('<footer')
    s = s[:at] + payload + s[at:]
    open(path, 'w', encoding='utf-8').write(s)
    return s


def wc(html):
    body = re.sub(r'<[^>]+>', ' ', html[html.index('<h1'):html.index('<footer')])
    return len(body.split())


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    n = 0
    for path, block in B.items():
        if not os.path.exists(path):
            print('  missing:', path); continue
        before = wc(open(path, encoding='utf-8').read())
        after = wc(insert(path, block))
        n += 1
        print('%-58s %4d -> %4d' % (path, before, after))
    print('deepened:', n)
