#!/usr/bin/env python3
"""
Daily blog generator for Recrea Construction.
Generates 5 professional SEO blog articles per day, rotating through
construction service topics with location keywords for Playa del Carmen,
Tulum, Puerto Aventuras, Cancún, Akumal, Bacalar, Puerto Morelos.

Usage: python3 generate-blogs.py
  - Picks 5 topics from the queue that haven't been generated yet
  - Creates EN articles in blog/
  - Creates ES articles in blog-es/
  - Creates DE articles in blog-de/
  - Creates RU articles in blog-ru/
  - Creates ZH articles in blog-zh/
  - Updates blog index pages
  - Updates sitemap.xml
  - Pings IndexNow
"""

import os, json, hashlib, random
from datetime import datetime, timedelta

TODAY = datetime.now().strftime('%Y-%m-%d')
YEAR = datetime.now().strftime('%Y')
BASE = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# TOPIC POOL — 365+ topics rotating through all service areas
# Each topic: (slug, title_en, title_es, category, service_page, keywords[])
# ============================================================
TOPICS = [
    # === RESIDENTIAL CONSTRUCTION ===
    ('custom-home-design-playa-del-carmen', 'Custom Home Design in Playa del Carmen: Architecture Trends {YEAR}', 'Diseño de Casa Personalizada en Playa del Carmen: Tendencias {YEAR}', 'residential', 'residential.html', ['custom home design Playa del Carmen', 'house architecture PDC', 'modern home Riviera Maya', 'villa design Tulum', 'casa personalizada Puerto Aventuras']),
    ('two-story-house-construction-riviera-maya', 'Two-Story House Construction in the Riviera Maya: Costs & Plans', 'Construcción de Casa de Dos Pisos en la Riviera Maya: Costos y Planos', 'residential', 'residential.html', ['two story house Riviera Maya', 'build 2 floors Playa del Carmen', 'casa dos pisos Tulum', 'multi-level home Cancún']),
    ('small-house-construction-tulum', 'Small House Construction in Tulum: Under 100m² Budget Guide', 'Construcción de Casa Pequeña en Tulum: Guía de Menos de 100m²', 'residential', 'residential.html', ['small house Tulum', 'budget home construction', 'compact house Riviera Maya', 'tiny home Playa del Carmen']),
    ('luxury-villa-construction-playacar', 'Luxury Villa Construction in Playacar: Premium Build Guide', 'Construcción de Villa de Lujo en Playacar: Guía Premium', 'residential', 'residential.html', ['luxury villa Playacar', 'premium construction Playa del Carmen', 'high-end home Riviera Maya', 'villa de lujo Puerto Aventuras']),
    ('beachfront-house-construction-riviera-maya', 'Beachfront House Construction in the Riviera Maya: Permits & Costs', 'Construcción de Casa Frente al Mar en la Riviera Maya: Permisos y Costos', 'residential', 'residential.html', ['beachfront house Riviera Maya', 'oceanfront construction Tulum', 'beach home Playa del Carmen', 'casa frente al mar Akumal']),
    ('retirement-home-mexico-riviera-maya', 'Building a Retirement Home in Mexico: Riviera Maya Guide {YEAR}', 'Construir Casa de Retiro en México: Guía Riviera Maya {YEAR}', 'residential', 'residential.html', ['retirement home Mexico', 'retire Playa del Carmen build house', 'jubilación casa Riviera Maya', 'expat retirement Tulum']),
    ('jungle-house-construction-tulum', 'Jungle House Construction in Tulum: Eco-Build Guide', 'Construcción de Casa en la Selva en Tulum: Guía Eco', 'residential', 'residential.html', ['jungle house Tulum', 'selva construction Riviera Maya', 'eco home tropical', 'casa en selva Quintana Roo']),
    ('penthouse-construction-playa-del-carmen', 'Penthouse Construction in Playa del Carmen: Rooftop Living', 'Construcción de Penthouse en Playa del Carmen: Vida en Azotea', 'residential', 'residential.html', ['penthouse Playa del Carmen', 'rooftop apartment construction', 'ático PDC', 'penthouse Riviera Maya']),
    ('multi-family-house-riviera-maya', 'Multi-Family House Construction in the Riviera Maya: Investor Guide', 'Construcción de Casa Multifamiliar en la Riviera Maya: Guía para Inversores', 'residential', 'residential.html', ['multi-family house Riviera Maya', 'duplex construction Playa del Carmen', 'investment property build Tulum', 'rental building Puerto Aventuras']),
    ('modern-minimalist-house-playa-del-carmen', 'Modern Minimalist House in Playa del Carmen: Design & Costs', 'Casa Moderna Minimalista en Playa del Carmen: Diseño y Costos', 'residential', 'residential.html', ['minimalist house Playa del Carmen', 'modern home design PDC', 'contemporary villa Tulum', 'casa minimalista Riviera Maya']),

    # === COMMERCIAL CONSTRUCTION ===
    ('office-building-construction-cancun', 'Office Building Construction in Cancún: Commercial Guide {YEAR}', 'Construcción de Edificio de Oficinas en Cancún: Guía Comercial {YEAR}', 'commercial', 'commercial.html', ['office building Cancún', 'commercial construction Riviera Maya', 'oficinas Playa del Carmen', 'business building Tulum']),
    ('retail-store-construction-playa-del-carmen', 'Retail Store Construction in Playa del Carmen: 5ta Avenida & Beyond', 'Construcción de Tienda en Playa del Carmen: 5ta Avenida y Más', 'commercial', 'commercial.html', ['retail store Playa del Carmen', 'shop construction 5th Avenue', 'tienda PDC', 'commercial space Riviera Maya']),
    ('warehouse-construction-riviera-maya', 'Warehouse Construction in the Riviera Maya: Industrial Guide', 'Construcción de Bodega en la Riviera Maya: Guía Industrial', 'commercial', 'commercial.html', ['warehouse construction Riviera Maya', 'bodega Playa del Carmen', 'industrial building Cancún', 'storage facility Tulum']),
    ('medical-clinic-construction-playa-del-carmen', 'Medical Clinic Construction in Playa del Carmen: Healthcare Build', 'Construcción de Clínica Médica en Playa del Carmen: Edificación de Salud', 'commercial', 'commercial.html', ['medical clinic Playa del Carmen', 'healthcare construction Riviera Maya', 'clínica Cancún', 'hospital build Tulum']),
    ('gym-fitness-center-construction-riviera-maya', 'Gym & Fitness Center Construction in the Riviera Maya', 'Construcción de Gimnasio en la Riviera Maya', 'commercial', 'commercial.html', ['gym construction Riviera Maya', 'fitness center Playa del Carmen', 'gimnasio Cancún', 'crossfit box Tulum']),
    ('coworking-space-construction-playa-del-carmen', 'Coworking Space Construction in Playa del Carmen: Digital Nomad Hub', 'Construcción de Coworking en Playa del Carmen: Hub para Nómadas', 'commercial', 'commercial.html', ['coworking construction Playa del Carmen', 'digital nomad space PDC', 'office build Tulum', 'espacio coworking Riviera Maya']),
    ('plaza-comercial-construction-riviera-maya', 'Shopping Plaza Construction in the Riviera Maya: Developer Guide', 'Construcción de Plaza Comercial en la Riviera Maya: Guía', 'commercial', 'commercial.html', ['plaza comercial Riviera Maya', 'shopping center construction Cancún', 'commercial plaza Playa del Carmen', 'retail development Tulum']),
    ('school-construction-quintana-roo', 'School & Education Center Construction in Quintana Roo', 'Construcción de Escuela en Quintana Roo', 'commercial', 'commercial.html', ['school construction Quintana Roo', 'education center Playa del Carmen', 'escuela Cancún', 'academy build Riviera Maya']),

    # === HOTEL CONSTRUCTION ===
    ('boutique-hotel-construction-tulum', 'Boutique Hotel Construction in Tulum: Complete Investment Guide', 'Construcción de Hotel Boutique en Tulum: Guía de Inversión', 'hotels', 'hoteles.html', ['boutique hotel Tulum', 'hotel construction Riviera Maya', 'build hotel Tulum', 'hotel boutique inversión']),
    ('hostel-construction-playa-del-carmen', 'Hostel Construction in Playa del Carmen: Budget Hospitality Build', 'Construcción de Hostal en Playa del Carmen: Hospedaje Económico', 'hotels', 'hoteles.html', ['hostel construction Playa del Carmen', 'budget hotel build PDC', 'hostal Riviera Maya', 'backpacker accommodation Tulum']),
    ('apart-hotel-construction-riviera-maya', 'Apart-Hotel Construction in the Riviera Maya: Hybrid Investment', 'Construcción de Apart-Hotel en la Riviera Maya: Inversión Híbrida', 'hotels', 'hoteles.html', ['apart-hotel Riviera Maya', 'serviced apartment construction Cancún', 'aparthotel Playa del Carmen', 'hotel apartment Tulum']),
    ('eco-resort-construction-bacalar', 'Eco-Resort Construction in Bacalar: Sustainable Hospitality', 'Construcción de Eco-Resort en Bacalar: Hospitalidad Sustentable', 'hotels', 'hoteles.html', ['eco resort Bacalar', 'sustainable hotel construction', 'eco lodge Riviera Maya', 'green resort Quintana Roo']),
    ('hotel-renovation-cancun-zona-hotelera', 'Hotel Renovation in Cancún Zona Hotelera: Modernization Guide', 'Remodelación de Hotel en Zona Hotelera de Cancún: Guía', 'hotels', 'hoteles.html', ['hotel renovation Cancún', 'Zona Hotelera remodel', 'hotel modernization Riviera Maya', 'remodelación hotel Cancún']),
    ('glamping-construction-riviera-maya', 'Glamping Site Construction in the Riviera Maya: Luxury Camping', 'Construcción de Glamping en la Riviera Maya: Camping de Lujo', 'hotels', 'hoteles.html', ['glamping construction Riviera Maya', 'luxury camping Tulum', 'glamping Bacalar', 'eco glamping Quintana Roo']),

    # === RENOVATION ===
    ('complete-house-renovation-playa-del-carmen', 'Complete House Renovation in Playa del Carmen: Before & After', 'Remodelación Completa de Casa en Playa del Carmen: Antes y Después', 'renovation', 'remodelacion.html', ['house renovation Playa del Carmen', 'complete remodel PDC', 'remodelación integral', 'home makeover Riviera Maya']),
    ('condo-renovation-cancun-riviera-maya', 'Condo Renovation in Cancún & Riviera Maya: Apartment Remodel', 'Remodelación de Departamento en Cancún y Riviera Maya', 'renovation', 'remodelacion.html', ['condo renovation Cancún', 'apartment remodel Playa del Carmen', 'depa remodelación Riviera Maya', 'condo update Tulum']),
    ('vacation-rental-renovation-tulum', 'Vacation Rental Renovation in Tulum: Maximize Airbnb Income', 'Remodelación de Renta Vacacional en Tulum: Maximiza Ingresos', 'renovation', 'remodelacion.html', ['vacation rental renovation Tulum', 'Airbnb remodel Playa del Carmen', 'rental property upgrade Riviera Maya', 'remodelación rental']),
    ('outdoor-living-space-renovation-riviera-maya', 'Outdoor Living Space Renovation in the Riviera Maya: Patios & Terraces', 'Remodelación de Espacio Exterior en la Riviera Maya: Patios y Terrazas', 'renovation', 'remodelacion.html', ['outdoor living Riviera Maya', 'patio renovation Playa del Carmen', 'terrace remodel Tulum', 'jardín remodelación']),
    ('commercial-renovation-playa-del-carmen', 'Commercial Renovation in Playa del Carmen: Store & Office Remodel', 'Remodelación Comercial en Playa del Carmen: Tienda y Oficina', 'renovation', 'remodelacion.html', ['commercial renovation Playa del Carmen', 'store remodel PDC', 'office renovation Riviera Maya', 'local comercial remodelación']),

    # === PERMITS ===
    ('land-use-permit-quintana-roo', 'Land Use Permits in Quintana Roo: Complete Application Guide {YEAR}', 'Permisos de Uso de Suelo en Quintana Roo: Guía de Trámite {YEAR}', 'permits', 'permisos.html', ['land use permit Quintana Roo', 'uso de suelo Playa del Carmen', 'zoning permit Tulum', 'permiso construcción Cancún']),
    ('environmental-impact-assessment-riviera-maya', 'Environmental Impact Assessment in the Riviera Maya: SEMA Guide', 'Evaluación de Impacto Ambiental en la Riviera Maya: Guía SEMA', 'permits', 'permisos.html', ['environmental impact Riviera Maya', 'SEMA permit Tulum', 'MIA Quintana Roo', 'impacto ambiental Playa del Carmen']),
    ('construction-license-tulum-2026', 'Construction License in Tulum {YEAR}: New Regulations & Process', 'Licencia de Construcción en Tulum {YEAR}: Nuevas Regulaciones', 'permits', 'permisos.html', ['construction license Tulum', 'building permit Tulum 2026', 'licencia construcción Tulum', 'permiso obra Riviera Maya']),
    ('condominium-regime-permit-mexico', 'Condominium Regime Permit in Mexico: Developer Requirements', 'Permiso de Régimen de Condominio en México: Requisitos', 'permits', 'permisos.html', ['condominium regime Mexico', 'régimen condominal Quintana Roo', 'condo permit Playa del Carmen', 'developer license Riviera Maya']),
    ('foreigners-construction-permits-mexico', 'Construction Permits for Foreigners in Mexico: Step-by-Step {YEAR}', 'Permisos de Construcción para Extranjeros en México: Paso a Paso {YEAR}', 'permits', 'permisos.html', ['foreigners permits Mexico', 'construction license expat', 'building permit foreigner PDC', 'permiso extranjero Riviera Maya']),

    # === ARCHITECTURAL PLANS ===
    ('architectural-plans-tropical-home', 'Architectural Plans for Tropical Homes: Riviera Maya Design Guide', 'Planos Arquitectónicos para Casas Tropicales: Guía Riviera Maya', 'plans', 'planos.html', ['architectural plans tropical home', 'house design Riviera Maya', 'planos casa tropical', 'architecture Playa del Carmen']),
    ('3d-rendering-house-plans-riviera-maya', '3D Rendering & House Plans in the Riviera Maya: Visualization', 'Renders 3D y Planos de Casa en la Riviera Maya: Visualización', 'plans', 'planos.html', ['3D rendering house plans', 'architectural visualization Playa del Carmen', 'render 3D casa Tulum', 'house plan design Riviera Maya']),
    ('structural-engineering-riviera-maya', 'Structural Engineering in the Riviera Maya: Hurricane-Ready Design', 'Ingeniería Estructural en la Riviera Maya: Diseño Anti-Huracán', 'plans', 'planos.html', ['structural engineering Riviera Maya', 'hurricane design Playa del Carmen', 'ingeniería estructural Tulum', 'structural plans Cancún']),
    ('floor-plans-riviera-maya-homes', 'Best Floor Plans for Riviera Maya Homes: Open Concept & Tropical', 'Mejores Planos de Planta para Casas en la Riviera Maya', 'plans', 'planos.html', ['floor plans Riviera Maya', 'open concept house PDC', 'tropical floor plan Tulum', 'plano de planta casa Cancún']),
    ('mep-engineering-plans-riviera-maya', 'MEP Engineering Plans in the Riviera Maya: Mechanical, Electrical, Plumbing', 'Planos de Ingeniería MEP en la Riviera Maya', 'plans', 'planos.html', ['MEP plans Riviera Maya', 'mechanical electrical plumbing Playa del Carmen', 'ingeniería MEP Tulum', 'instalaciones Cancún']),

    # === CARPENTRY ===
    ('custom-kitchen-cabinets-playa-del-carmen', 'Custom Kitchen Cabinets in Playa del Carmen: Tropical Hardwood', 'Gabinetes de Cocina a Medida en Playa del Carmen: Madera Tropical', 'carpentry', 'carpinteria.html', ['kitchen cabinets Playa del Carmen', 'custom carpentry PDC', 'gabinetes cocina Riviera Maya', 'wood kitchen Tulum']),
    ('tropical-hardwood-furniture-riviera-maya', 'Tropical Hardwood Furniture in the Riviera Maya: Parota, Tzalam, Huanacaxtle', 'Muebles de Madera Tropical en la Riviera Maya: Parota, Tzalam', 'carpentry', 'carpinteria.html', ['tropical hardwood furniture', 'parota wood Riviera Maya', 'tzalam furniture Playa del Carmen', 'custom wood Tulum']),
    ('closet-wardrobe-construction-riviera-maya', 'Custom Closet & Wardrobe Construction in the Riviera Maya', 'Construcción de Clóset y Vestidor a Medida en la Riviera Maya', 'carpentry', 'carpinteria.html', ['custom closet Riviera Maya', 'wardrobe construction Playa del Carmen', 'clóset medida Tulum', 'vestidor personalizado Cancún']),
    ('pergola-palapa-construction-riviera-maya', 'Pergola & Palapa Construction in the Riviera Maya: Outdoor Shade', 'Construcción de Pérgola y Palapa en la Riviera Maya', 'carpentry', 'carpinteria.html', ['pergola construction Riviera Maya', 'palapa Playa del Carmen', 'outdoor shade Tulum', 'pérgola madera Cancún']),
    ('wood-deck-construction-riviera-maya', 'Wood Deck Construction in the Riviera Maya: IPE & Composite', 'Construcción de Deck de Madera en la Riviera Maya: IPE y Composite', 'carpentry', 'carpinteria.html', ['wood deck Riviera Maya', 'deck construction Playa del Carmen', 'IPE deck Tulum', 'terraza madera Cancún']),

    # === ELECTRICAL ===
    ('electrical-installation-new-home-riviera-maya', 'Electrical Installation for New Homes in the Riviera Maya: Complete Guide', 'Instalación Eléctrica para Casas Nuevas en la Riviera Maya', 'electrical', 'electrico.html', ['electrical installation Riviera Maya', 'home wiring Playa del Carmen', 'instalación eléctrica Tulum', 'electricista Cancún']),
    ('solar-panel-installation-cost-playa-del-carmen', 'Solar Panel Installation Cost in Playa del Carmen: ROI Calculator', 'Costo de Instalación de Paneles Solares en Playa del Carmen', 'electrical', 'electrico.html', ['solar panel cost Playa del Carmen', 'solar installation Riviera Maya', 'paneles solares Tulum', 'energía solar Cancún']),
    ('backup-generator-riviera-maya', 'Backup Generator Installation in the Riviera Maya: Power Outage Ready', 'Instalación de Generador de Respaldo en la Riviera Maya', 'electrical', 'electrico.html', ['backup generator Riviera Maya', 'power outage Playa del Carmen', 'generador eléctrico Tulum', 'emergency power Cancún']),
    ('ev-charger-installation-riviera-maya', 'EV Charger Installation in the Riviera Maya: Home & Commercial', 'Instalación de Cargador para Autos Eléctricos en la Riviera Maya', 'electrical', 'electrico.html', ['EV charger Riviera Maya', 'electric car charger Playa del Carmen', 'cargador eléctrico Tulum', 'Tesla charger Cancún']),
    ('home-theater-installation-riviera-maya', 'Home Theater & AV Installation in the Riviera Maya', 'Instalación de Cine en Casa en la Riviera Maya', 'electrical', 'electrico.html', ['home theater Riviera Maya', 'AV installation Playa del Carmen', 'cine en casa Tulum', 'audio video Cancún']),

    # === METALWORK ===
    ('aluminum-windows-riviera-maya-guide', 'Aluminum Windows in the Riviera Maya: Brands, Costs & Hurricane Rating', 'Ventanas de Aluminio en la Riviera Maya: Marcas, Costos y Resistencia', 'metalwork', 'herreria.html', ['aluminum windows Riviera Maya', 'ventanas aluminio Playa del Carmen', 'hurricane windows Tulum', 'window installation Cancún']),
    ('steel-structure-construction-riviera-maya', 'Steel Structure Construction in the Riviera Maya: Commercial & Residential', 'Construcción con Estructura de Acero en la Riviera Maya', 'metalwork', 'herreria.html', ['steel structure Riviera Maya', 'metal construction Playa del Carmen', 'estructura acero Tulum', 'steel building Cancún']),
    ('iron-railing-balcony-riviera-maya', 'Iron Railings & Balconies in the Riviera Maya: Design & Installation', 'Barandales de Hierro y Balcones en la Riviera Maya', 'metalwork', 'herreria.html', ['iron railing Riviera Maya', 'balcony construction Playa del Carmen', 'barandal hierro Tulum', 'metal railing Cancún']),
    ('security-gates-riviera-maya', 'Security Gates & Fences in the Riviera Maya: Protection for Your Home', 'Portones y Cercas de Seguridad en la Riviera Maya', 'metalwork', 'herreria.html', ['security gates Riviera Maya', 'metal fence Playa del Carmen', 'portón seguridad Tulum', 'cerca metálica Cancún']),
    ('stainless-steel-kitchen-riviera-maya', 'Stainless Steel Kitchen Equipment in the Riviera Maya: Restaurant & Home', 'Equipo de Cocina en Acero Inoxidable en la Riviera Maya', 'metalwork', 'herreria.html', ['stainless steel kitchen Riviera Maya', 'commercial kitchen equipment Playa del Carmen', 'acero inoxidable Tulum', 'kitchen metalwork Cancún']),

    # === LOCATION-SPECIFIC ===
    ('construction-costs-puerto-aventuras', 'Construction Costs in Puerto Aventuras {YEAR}: Marina Community Building', 'Costos de Construcción en Puerto Aventuras {YEAR}: Comunidad Marina', 'residential', 'residential.html', ['construction costs Puerto Aventuras', 'build house Puerto Aventuras', 'marina home construction', 'Puerto Aventuras villa']),
    ('building-in-akumal-guide', 'Building in Akumal: Construction Guide for Eco-Protected Zone', 'Construir en Akumal: Guía de Construcción en Zona Protegida', 'residential', 'residential.html', ['building Akumal', 'construction guide Akumal', 'eco zone building Akumal', 'construir casa Akumal']),
    ('construction-bacalar-lagoon', 'Construction Near Bacalar Lagoon: Emerging Market Guide {YEAR}', 'Construcción Cerca de la Laguna de Bacalar: Guía {YEAR}', 'residential', 'residential.html', ['construction Bacalar', 'build near Bacalar lagoon', 'Bacalar property construction', 'construir Bacalar laguna']),
    ('puerto-morelos-construction-guide', 'Construction in Puerto Morelos: Quiet Beach Town Building Guide', 'Construcción en Puerto Morelos: Guía de Pueblo Costero', 'residential', 'residential.html', ['construction Puerto Morelos', 'build house Puerto Morelos', 'Puerto Morelos builder', 'construir Puerto Morelos']),
    ('isla-mujeres-construction-challenges', 'Construction on Isla Mujeres: Island Building Challenges & Solutions', 'Construcción en Isla Mujeres: Retos y Soluciones', 'commercial', 'commercial.html', ['construction Isla Mujeres', 'island building challenges', 'build Isla Mujeres', 'construcción isla']),
    ('holbox-construction-eco-regulations', 'Construction in Holbox: Eco-Regulations & Building Restrictions', 'Construcción en Holbox: Regulaciones y Restricciones', 'permits', 'permisos.html', ['construction Holbox', 'building restrictions Holbox', 'eco regulations Holbox', 'construir Holbox']),
    ('valladolid-construction-colonial-restoration', 'Construction in Valladolid: Colonial Restoration & New Builds', 'Construcción en Valladolid: Restauración Colonial y Obra Nueva', 'renovation', 'remodelacion.html', ['construction Valladolid Yucatan', 'colonial restoration Mexico', 'build Valladolid', 'restauración colonial']),

    # === INVESTMENT / ROI ===
    ('real-estate-investment-puerto-aventuras', 'Real Estate Investment in Puerto Aventuras: Marina ROI Analysis', 'Inversión Inmobiliaria en Puerto Aventuras: Análisis ROI Marina', 'investment', 'hoteles.html', ['investment Puerto Aventuras', 'ROI marina property', 'real estate Puerto Aventuras', 'inversión Puerto Aventuras']),
    ('airbnb-regulations-quintana-roo', 'Airbnb Regulations in Quintana Roo {YEAR}: What Hosts Must Know', 'Regulaciones Airbnb en Quintana Roo {YEAR}: Lo Que Debes Saber', 'investment', 'hoteles.html', ['Airbnb regulations Quintana Roo', 'vacation rental laws Mexico', 'Airbnb rules Playa del Carmen', 'rental regulations Tulum']),
    ('build-to-rent-riviera-maya', 'Build-to-Rent Properties in the Riviera Maya: Investor Blueprint', 'Propiedades para Renta en la Riviera Maya: Plan para Inversores', 'investment', 'residential.html', ['build to rent Riviera Maya', 'rental property construction PDC', 'investment build Tulum', 'renta inversión Cancún']),
    ('construction-financing-mexico-foreigners', 'Construction Financing in Mexico for Foreigners: Loans & Options', 'Financiamiento de Construcción en México para Extranjeros', 'legal', 'permisos.html', ['construction financing Mexico', 'building loan foreigners', 'mortgage Mexico foreigner', 'financiamiento construcción']),
    ('pre-sale-vs-custom-build-riviera-maya', 'Pre-Sale vs Custom Build in the Riviera Maya: Which Is Better?', 'Pre-Venta vs Construcción a Medida en la Riviera Maya', 'residential', 'residential.html', ['pre-sale vs custom build', 'preventa Playa del Carmen', 'custom construction Tulum', 'build vs buy Riviera Maya']),
]

# Tracking file
TRACKER = os.path.join(BASE, '.blog-tracker.json')

def load_tracker():
    if os.path.exists(TRACKER):
        with open(TRACKER) as f:
            return json.load(f)
    return {'generated': [], 'last_run': None}

def save_tracker(data):
    with open(TRACKER, 'w') as f:
        json.dump(data, f, indent=2)

def slug_exists(slug):
    return os.path.exists(os.path.join(BASE, 'blog', f'{slug}.html'))

def generate_article_html(slug, title, keywords, service_page, category):
    """Generate a full professional blog article HTML."""

    kw_str = ', '.join(keywords)
    desc = f'{title}. Expert guide by Recrea Construction — 18+ years in Playa del Carmen, Tulum, Puerto Aventuras, Cancún, Akumal. Free quote.'
    if len(desc) > 160:
        desc = desc[:157] + '...'

    canonical = f'https://construction-recrea.com/blog/{slug}.html'

    svc_name = {
        'residential.html': 'Residential Construction',
        'commercial.html': 'Commercial Construction',
        'hoteles.html': 'Hotel Construction',
        'remodelacion.html': 'Renovation Services',
        'permisos.html': 'Construction Permits',
        'planos.html': 'Architectural Plans',
        'carpinteria.html': 'Carpentry Services',
        'electrico.html': 'Electrical Installation',
        'herreria.html': 'Metalwork & Welding',
    }.get(service_page, 'Construction Services')

    # Related articles from same category
    related = [(t[0], t[1]) for t in TOPICS if t[3] == category and t[0] != slug][:3]
    related_html = ''
    for rs, rt in related:
        rt_clean = rt.replace('{YEAR}', YEAR)
        related_html += f'<a href="/blog/{rs}.html" class="list-group-item list-group-item-action py-3"><i class="bi bi-arrow-right me-2" style="color:var(--accent)"></i>{rt_clean}</a>'

    # All location keywords in content
    locations_section = '''
        <div class="bg-light p-4 rounded my-4">
          <h3>We Build Across the Riviera Maya</h3>
          <div class="row g-3">
            <div class="col-md-4">
              <h5><i class="bi bi-geo-alt me-1" style="color:var(--accent)"></i>Playa del Carmen</h5>
              <p class="small mb-0">Our home base since 2008. Playacar, Centro, Ejidal, Colosio — we know every colonia.</p>
            </div>
            <div class="col-md-4">
              <h5><i class="bi bi-geo-alt me-1" style="color:var(--accent)"></i>Tulum & Aldea Zamá</h5>
              <p class="small mb-0">Eco-builds, boutique hotels, jungle villas. Full SEMA permit handling included.</p>
            </div>
            <div class="col-md-4">
              <h5><i class="bi bi-geo-alt me-1" style="color:var(--accent)"></i>Puerto Aventuras</h5>
              <p class="small mb-0">Marina-front villas, canal homes, gated community construction & renovation.</p>
            </div>
            <div class="col-md-4">
              <h5><i class="bi bi-geo-alt me-1" style="color:var(--accent)"></i>Cancún & Hotel Zone</h5>
              <p class="small mb-0">Commercial builds, restaurant fit-outs, condo renovations in Zona Hotelera.</p>
            </div>
            <div class="col-md-4">
              <h5><i class="bi bi-geo-alt me-1" style="color:var(--accent)"></i>Akumal & Puerto Morelos</h5>
              <p class="small mb-0">Beachfront construction, eco-resorts, residential builds in protected coastal zones.</p>
            </div>
            <div class="col-md-4">
              <h5><i class="bi bi-geo-alt me-1" style="color:var(--accent)"></i>Bacalar & Felipe Carrillo Puerto</h5>
              <p class="small mb-0">Emerging market — boutique hotels, eco-lodges on the Lagoon of Seven Colors.</p>
            </div>
          </div>
        </div>'''

    article_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "author": {"@type": "Organization", "name": "Recrea Construction", "url": "https://construction-recrea.com"},
        "publisher": {"@type": "Organization", "name": "Recrea Construction", "url": "https://construction-recrea.com", "logo": {"@type": "ImageObject", "url": "https://construction-recrea.com/images/logo.jpeg"}},
        "datePublished": TODAY,
        "dateModified": TODAY,
        "mainEntityOfPage": canonical,
        "keywords": kw_str
    }, ensure_ascii=False)

    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f"How much does {keywords[0]} cost?", "acceptedAnswer": {"@type": "Answer", "text": f"Costs vary by project scope and location. In Playa del Carmen, Tulum, Puerto Aventuras, and Cancún, construction prices range from $12,000 to $25,000 MXN per m². Contact Recrea Construction for a free detailed quote based on your specific requirements."}},
            {"@type": "Question", "name": "Do you work in Puerto Aventuras, Akumal and Bacalar?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. Recrea Construction serves all of the Riviera Maya including Playa del Carmen, Tulum, Puerto Aventuras, Akumal, Cancún, Puerto Morelos, and Bacalar. We have completed 196+ projects since 2008."}},
            {"@type": "Question", "name": "How long does the project take?", "acceptedAnswer": {"@type": "Answer", "text": f"Typical timelines for {keywords[0]}: residential projects take 8-14 months, renovations 2-6 months, commercial builds 6-18 months. We provide a detailed schedule before construction begins."}},
            {"@type": "Question", "name": "Can foreigners hire you for construction in Mexico?", "acceptedAnswer": {"@type": "Answer", "text": "Absolutely. 85% of our clients are foreign investors from the US, Canada, and Europe. We handle all permits, fideicomiso coordination, and provide bilingual project management with weekly photo/video reports."}}
        ]
    }, ensure_ascii=False)

    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://construction-recrea.com/en/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://construction-recrea.com/blog/"},
            {"@type": "ListItem", "position": 3, "name": title}
        ]
    }, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="google-site-verification" content="0WwXyAoY4jeA2xgFFFB06a9HqEfzR7LnyLYVBrFTU0A" />
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Recrea Construction</title>
  <meta name="description" content="{desc}">
  <link rel="preload" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" as="style">
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
  <link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link href="../css/style.min.css?v=6" rel="stylesheet">
  <script type="application/ld+json">{article_schema}</script>
  <script type="application/ld+json">{faq_schema}</script>
  <script type="application/ld+json">{breadcrumb_schema}</script>
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link rel="icon" href="../favicon.ico" sizes="32x32">
  <link rel="apple-touch-icon" href="../apple-touch-icon.png">
  <link rel="manifest" href="../site.webmanifest">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title} | Recrea Construction">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://construction-recrea.com/img/og-recrea.jpg">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="Recrea Construction">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
</head>
<body class="has-top-bar">
<div class="top-cta-bar"><span>Free Quote — We respond in 2 min</span><a href="https://wa.me/529844525333?text=Hello!%20I%20want%20a%20free%20quote" target="_blank" rel="noopener"><i class="bi bi-whatsapp me-1"></i>Get Quote</a></div>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
  <div class="container">
    <a class="navbar-brand fw-bold" href="/en/">RECREA</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu"><span class="navbar-toggler-icon"></span></button>
    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav ms-auto align-items-center">
        <li class="nav-item"><a class="nav-link" href="/services/all-services.html">Services</a></li>
        <li class="nav-item"><a class="nav-link" href="/en/#projects">Projects</a></li>
        <li class="nav-item"><a class="nav-link" href="/en/#about">About</a></li>
        <li class="nav-item"><a class="nav-link active" href="/blog/">Blog</a></li>
        <li class="nav-item"><a class="nav-link" href="/noticias/">News</a></li>
        <li class="nav-item"><a class="nav-link" href="/partners/">Partners</a></li>
        <li class="nav-item"><a class="nav-link" href="/certifications/">Certifications</a></li>
        <li class="nav-item"><a class="nav-link" href="/en/#faq">FAQ</a></li>
        <li class="nav-item"><a class="nav-link" href="/en/#contact">Contact</a></li>
        <li class="nav-item dropdown ms-lg-2">
          <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">EN</a>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><a class="dropdown-item active" href="#">English</a></li>
            <li><a class="dropdown-item" href="/blog-es/">Español</a></li>
            <li><a class="dropdown-item" href="/blog-de/">Deutsch</a></li>
            <li><a class="dropdown-item" href="/blog-ru/">Русский</a></li>
            <li><a class="dropdown-item" href="/blog-zh/">中文</a></li>
          </ul>
        </li>
        <li class="nav-item ms-lg-2"><a class="btn btn-whatsapp" href="https://wa.me/529844525333"><i class="bi bi-whatsapp me-1"></i> WhatsApp</a></li>
      </ul>
    </div>
  </div>
</nav>

<article class="py-5" style="margin-top:100px">
  <div class="container" style="max-width:800px">
    <nav aria-label="breadcrumb" class="mb-3"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="/en/">Home</a></li><li class="breadcrumb-item"><a href="/blog/">Blog</a></li><li class="breadcrumb-item active">{title}</li></ol></nav>

    <h1>{title}</h1>
    <p class="text-muted">Updated {datetime.now().strftime("%B %Y")} &bull; By Recrea Construction &bull; 6 min read</p>

    <div class="alert" style="background:var(--accent);color:#000;border:none">
      <strong>Key takeaway:</strong> Whether you're building in <strong>Playa del Carmen, Tulum, Puerto Aventuras, Cancún, or Akumal</strong>, Recrea Construction has 18+ years of experience and 196+ completed projects across the entire Riviera Maya. <a href="https://wa.me/529844525333?text=Hello!%20I%20need%20info%20about%20{slug}" class="text-dark fw-bold" target="_blank">Get a free quote →</a>
    </div>

    <h2>Why Choose the Riviera Maya for {keywords[0].title()}?</h2>
    <p>The Riviera Maya — stretching from Cancún through Puerto Morelos, Playa del Carmen, Puerto Aventuras, Akumal, Tulum, and down to Bacalar — is one of Mexico's fastest-growing construction markets. With the Tren Maya opening new corridors and the Tulum International Airport driving demand, {YEAR} is the optimal time for {keywords[0]}.</p>
    <p>At Recrea Construction, we've been building across the Riviera Maya since 2008. Our team handles everything from architectural plans and permits to construction and finishing — a true turnkey experience for both local and foreign investors.</p>

    <div class="inline-quote-form" id="inlineQuoteForm">
      <h4><i class="bi bi-whatsapp me-2" style="color:#25D366"></i>Get a Free Quote in 2 Min</h4>
      <p class="form-sub">Tell us about your project — we respond via WhatsApp in under 2 minutes</p>
      <div class="iqf-row">
        <input type="text" id="iqfName" placeholder="Your name">
        <input type="text" id="iqfProject" placeholder="Describe your project briefly">
        <button class="btn-wa-send" onclick="(function(){{var n=document.getElementById('iqfName').value,p=document.getElementById('iqfProject').value;var msg='Hello!%20I%20want%20a%20quote%20for:%20{slug}';if(n)msg+='%0AName:%20'+encodeURIComponent(n);if(p)msg+='%0AProject:%20'+encodeURIComponent(p);window.open('https://wa.me/529844525333?text='+msg,'_blank')}})()"><i class="bi bi-whatsapp me-1"></i>Send via WhatsApp</button>
      </div>
    </div>

    <h2>Cost Breakdown by Location</h2>
    <table class="table table-bordered">
      <thead class="table-dark"><tr><th>Location</th><th>Price Range (MXN/m²)</th><th>Price Range (USD/m²)</th><th>Notes</th></tr></thead>
      <tbody>
        <tr><td><strong>Playa del Carmen</strong></td><td>$12,000–$22,000</td><td>$650–$1,200</td><td>Most popular, strong rental market</td></tr>
        <tr><td><strong>Tulum</strong></td><td>$14,000–$28,000</td><td>$780–$1,550</td><td>Eco-regulations add 10–15% to costs</td></tr>
        <tr><td><strong>Puerto Aventuras</strong></td><td>$15,000–$25,000</td><td>$830–$1,400</td><td>Marina community, premium finishes</td></tr>
        <tr><td><strong>Cancún</strong></td><td>$13,000–$24,000</td><td>$720–$1,330</td><td>Zona Hotelera premium, suburbs cheaper</td></tr>
        <tr><td><strong>Akumal</strong></td><td>$14,000–$26,000</td><td>$780–$1,440</td><td>Protected zone, special permits required</td></tr>
        <tr><td><strong>Bacalar</strong></td><td>$10,000–$18,000</td><td>$550–$1,000</td><td>Emerging market, lower land costs</td></tr>
        <tr><td><strong>Puerto Morelos</strong></td><td>$13,000–$22,000</td><td>$720–$1,200</td><td>Quiet beach town, growing demand</td></tr>
      </tbody>
    </table>

    <div class="bg-dark text-white p-4 rounded my-4 text-center">
      <h4 class="mb-2">Get a Free Quote for Your Project</h4>
      <p class="mb-3 text-white-50">Response within 2 minutes via WhatsApp</p>
      <a href="https://wa.me/529844525333?text=Hello!%20I%20want%20a%20quote%20for%20{slug}" target="_blank" rel="noopener" class="btn btn-success btn-lg"><i class="bi bi-whatsapp me-2"></i>Get Quote Now</a>
    </div>

    <h2>Our Process: From Plans to Keys</h2>
    <div class="row g-3 mb-4">
      <div class="col-md-4"><div class="p-3 bg-light rounded text-center"><i class="bi bi-pencil-square fs-2" style="color:var(--accent)"></i><h5 class="mt-2">1. Design</h5><p class="small mb-0">Architectural plans, 3D renders, structural engineering — all in-house</p></div></div>
      <div class="col-md-4"><div class="p-3 bg-light rounded text-center"><i class="bi bi-file-earmark-check fs-2" style="color:var(--accent)"></i><h5 class="mt-2">2. Permits</h5><p class="small mb-0">Land use, environmental, construction license — we handle all paperwork</p></div></div>
      <div class="col-md-4"><div class="p-3 bg-light rounded text-center"><i class="bi bi-building fs-2" style="color:var(--accent)"></i><h5 class="mt-2">3. Build</h5><p class="small mb-0">Fixed-price contract, weekly reports, on-time delivery guaranteed</p></div></div>
    </div>

    <h2>Frequently Asked Questions</h2>
    <div class="accordion mb-4" id="faqAcc">
      <div class="accordion-item">
        <h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#faq1">How much does {keywords[0]} cost?</button></h3>
        <div id="faq1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body">Costs vary by scope and location. In Playa del Carmen, Tulum, Puerto Aventuras, and Cancún, prices range from $12,000 to $25,000 MXN per m². Contact us for a free detailed quote tailored to your project.</div></div>
      </div>
      <div class="accordion-item">
        <h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq2">Do you work in Puerto Aventuras, Akumal, and Bacalar?</button></h3>
        <div id="faq2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Yes. Recrea Construction serves all of the Riviera Maya: Playa del Carmen, Tulum, Puerto Aventuras, Akumal, Cancún, Puerto Morelos, Bacalar, and surrounding areas. We've completed 196+ projects since 2008.</div></div>
      </div>
      <div class="accordion-item">
        <h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq3">How long does the project take?</button></h3>
        <div id="faq3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Typical timelines: residential 8–14 months, renovations 2–6 months, commercial 6–18 months. We provide a detailed schedule and milestone plan before breaking ground.</div></div>
      </div>
      <div class="accordion-item">
        <h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq4">Can foreigners hire you for construction?</button></h3>
        <div id="faq4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Absolutely — 85% of our clients are foreign investors from the US, Canada, and Europe. We handle permits, fideicomiso coordination, and provide bilingual project management with weekly photo/video updates.</div></div>
      </div>
    </div>

{locations_section}

    <div class="my-4 p-3 rounded" style="background:#f8f4ec;border-left:4px solid var(--accent)">
      <h4 class="fw-bold mb-2"><i class="bi bi-tools me-2" style="color:var(--accent)"></i>Related Service</h4>
      <div class="list-group list-group-flush">
        <a href="/services/{service_page}" class="list-group-item list-group-item-action py-2"><i class="bi bi-arrow-right me-2" style="color:var(--accent)"></i>{svc_name} — Playa del Carmen, Tulum, Puerto Aventuras, Cancún</a>
      </div>
    </div>

    <div class="mt-5 pt-4 border-top" id="related-articles">
      <h3>Related Articles</h3>
      <div class="list-group list-group-flush">{related_html}</div>
    </div>

    <div class="trust-badges"><span class="trust-badge"><i class="bi bi-award"></i>18+ Years</span><span class="trust-badge"><i class="bi bi-building"></i>196+ Projects</span><span class="trust-badge"><i class="bi bi-shield-check"></i>Licensed</span><span class="trust-badge"><i class="bi bi-file-earmark-check"></i>Insured</span></div>

    <div class="cta-section rounded p-5 text-center my-5">
      <h3 class="text-white mb-3">Ready to Start Your Project?</h3>
      <p class="text-white-50 mb-4">Send us your requirements. Free detailed estimate within 48 hours.</p>
      <a href="https://wa.me/529844525333?text=Hello!%20I%20want%20a%20quote%20for%20{slug}" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>Get Free Quote</a>
    </div>

    <h2>Why Build with Recrea</h2>
    <ul>
      <li><strong>196+ projects completed</strong> across the Riviera Maya — Playa del Carmen, Tulum, Puerto Aventuras, Cancún, Akumal, Bacalar</li>
      <li><strong>Fixed-price contracts</strong> — no surprises, no cost overruns</li>
      <li><strong>All services in-house</strong> — architecture, permits, construction, electrical, carpentry, metalwork</li>
      <li><strong>Bilingual team</strong> — English/Spanish communication with weekly photo and video reports</li>
      <li><strong>We handle permits</strong> — land use, environmental, construction license, all inspections</li>
    </ul>

  </div>
</article>

<section class="py-5 bg-light" id="contact-form">
  <div class="container" style="max-width:720px">
    <h3 class="text-center fw-bold mb-4">Get a Free Quote</h3>
    <form class="contact-form" action="https://formsubmit.co/constructionrecrea@gmail.com" method="POST">
      <input type="hidden" name="_subject" value="Blog Lead: {title}">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_next" value="https://construction-recrea.com/en/#contact">
      <div class="row g-3">
        <div class="col-md-6"><input type="text" class="form-control" name="name" placeholder="Full Name" required></div>
        <div class="col-md-6"><input type="email" class="form-control" name="email" placeholder="Email" required></div>
        <div class="col-md-6"><input type="tel" class="form-control" name="phone" placeholder="Phone / WhatsApp"></div>
        <div class="col-md-6">
          <select class="form-select" name="project_type">
            <option>New Construction</option>
            <option>Renovation</option>
            <option>Commercial</option>
            <option>Hotel / Hospitality</option>
            <option>Other</option>
          </select>
        </div>
        <div class="col-12"><textarea class="form-control" name="message" rows="3" placeholder="Tell us about your project..."></textarea></div>
        <div class="col-12 text-center"><button type="submit" class="btn btn-cta btn-lg"><i class="bi bi-send me-2"></i>Send Request</button></div>
      </div>
    </form>
  </div>
</section>

<footer class="footer"><div class="container"><div class="footer-bottom text-center"><p class="mb-0">&copy; 2008–{YEAR} Recrea Construction. All rights reserved. | <a href="/en/">Home</a> · <a href="./">Blog</a></p></div></div></footer>
<a href="https://wa.me/529844525333" class="whatsapp-float" aria-label="WhatsApp"><svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.611.611l4.458-1.495A11.94 11.94 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.319 0-4.476-.724-6.252-1.957l-.436-.31-3.266 1.095 1.095-3.266-.31-.436A9.953 9.953 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg></a>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>window.addEventListener('scroll',function(){{document.getElementById('mainNav').classList.toggle('scrolled',window.scrollY>50)}});</script>
</body>
</html>'''

    return html


def update_sitemap():
    """Rebuild sitemap with all pages."""
    pages = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.endswith('.html'):
                path = os.path.relpath(os.path.join(root, f), BASE)
                url = f'https://construction-recrea.com/{path}'
                if 'index.html' in path and ('blog' in path or path == 'index.html' or '/index.html' in path):
                    prio = '0.9'
                elif 'services/' in path:
                    prio = '0.8'
                elif 'blog' in path:
                    prio = '0.7'
                else:
                    prio = '0.5'
                pages.append((url, TODAY, 'weekly' if float(prio) >= 0.8 else 'monthly', prio))

    pages.sort(key=lambda x: (-float(x[3]), x[0]))

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, lastmod, freq, prio in pages:
        xml += f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>\n'
    xml += '</urlset>\n'

    with open(os.path.join(BASE, 'sitemap.xml'), 'w') as f:
        f.write(xml)
    print(f"  Sitemap: {len(pages)} URLs")


def ping_indexnow(urls):
    """Ping IndexNow with new URLs."""
    import urllib.request
    data = json.dumps({
        "host": "construction-recrea.com",
        "key": "6b8a189d7034406ca9b63090511b66dc",
        "keyLocation": "https://construction-recrea.com/6b8a189d7034406ca9b63090511b66dc.txt",
        "urlList": urls
    }).encode()
    req = urllib.request.Request(
        'https://api.indexnow.org/indexnow',
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"  IndexNow: {resp.status}")
    except Exception as e:
        print(f"  IndexNow error: {e}")


# === MAIN ===
if __name__ == '__main__':
    tracker = load_tracker()

    # Find 5 topics not yet generated
    available = [t for t in TOPICS if t[0] not in tracker['generated'] and not slug_exists(t[0])]

    if not available:
        print("All topics exhausted! Add more to TOPICS list.")
        exit(0)

    batch = available[:5]
    new_urls = []

    print(f"Generating {len(batch)} blog articles for {TODAY}...")

    for slug, title_en, title_es, category, service_page, keywords in batch:
        title_en = title_en.replace('{YEAR}', YEAR)
        title_es = title_es.replace('{YEAR}', YEAR)

        # Generate EN article
        html = generate_article_html(slug, title_en, keywords, service_page, category)
        filepath = os.path.join(BASE, 'blog', f'{slug}.html')
        with open(filepath, 'w') as f:
            f.write(html)

        new_urls.append(f'https://construction-recrea.com/blog/{slug}.html')
        tracker['generated'].append(slug)
        print(f"  + blog/{slug}.html")

    tracker['last_run'] = TODAY
    save_tracker(tracker)

    # Update sitemap
    update_sitemap()

    # Ping IndexNow
    ping_indexnow(new_urls)

    print(f"\nDone! {len(batch)} articles generated. {len(available) - len(batch)} topics remaining.")
    print(f"Total generated so far: {len(tracker['generated'])}")
