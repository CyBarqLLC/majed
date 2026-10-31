#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Majed Namous — static site generator.

Run:  python3 build.py
Out:  index.html, aqsa.html, monolith.html, contact.html,
      the same four under en/, robots.txt, sitemap.xml

Everything editable lives in sections 1 and 2 below.
"""

import hashlib
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://majednamous.com"
YEAR = date.today().year

# ============================================================
# 1. SITE CONFIG — edit here
# ============================================================

SITE = {
    # The site name is identical in both languages, by request.
    "site_name": "Majed Namous ماجد ناموس",
    "tagline": "في عمارة البنيان، وتوثيق أثر الإنسان.",
    # Paste a form endpoint here (Formspree, Basin, your own handler…).
    # While it is empty the contact form never claims a message was sent.
    "form_endpoint": "",
    "phone": "+962777452266",
    "phone_display": "+962 7 7745 2266",
    "whatsapp": "https://wa.me/962777452266",
    "email": "info@majednamous.com",
    "athar_url": "https://atharwaqf.com",
    "interview_url": "https://youtu.be/xKitnoafCLU?si=AU4Ggjp1C2CEM-Ni",
}

# Works, chronological. Image basenames live in assets/img as
# <img>-400.webp / -640.webp / -1000.webp / -1000.jpg
WORKS = [
    {"img": "work-2007", "year": "2007",
     "alt_ar": "فناء داخلي بجدران مزيّنة بالأبلق وبِركة ماء في الوسط",
     "alt_en": "Interior courtyard with ablaq stonework and a central water basin"},
    {"img": "work-2012", "year": "2012",
     "alt_ar": "هيكل عقود حجرية قيد الإنشاء",
     "alt_en": "Arched structural frames under construction"},
    {"img": "work-2013", "year": "2013",
     "alt_ar": "مبنى بقبّة بيضاء وسط أرض مزروعة حديثًا",
     "alt_en": "White-domed building set in a newly planted landscape"},
    {"img": "work-2015", "year": "2015",
     "alt_ar": "رواق خشبي مسقوف مع نافورة حجرية",
     "alt_en": "Timber-roofed veranda with a stone fountain"},
    {"img": "work-2016", "year": "2016",
     "alt_ar": "قاعة حجرية معقودة مفروشة بالسجاد والمجالس",
     "alt_en": "Vaulted stone hall furnished with rugs and low seating"},
    {"img": "work-2017", "year": "2017",
     "alt_ar": "عربة قطار تاريخية مُعاد تأهيلها ليلًا",
     "alt_en": "Restored historic railway carriage at night"},
    {"img": "work-2018-b", "year": "2018",
     "alt_ar": "مدخل حجري يطلّ على مصلّى مضاء ليلًا",
     "alt_en": "Stone portal opening onto a lit prayer hall at night"},
    {"img": "work-2018", "year": "2018",
     "alt_ar": "رواق حجري معقود مضاء ليلًا",
     "alt_en": "Vaulted stone arcade lit at night"},
    {"img": "work-2020", "year": "2020",
     "alt_ar": "كوخ خشبي مثلّث الواجهة مضاء ليلًا وأمامه فناء حجري",
     "alt_en": "A-frame timber cottage lit at night, with a stone forecourt"},
    {"img": "work-2023", "year": "2023",
     "alt_ar": "كوخ بواجهة زجاجية جمالونية تحيط بها الجنائن والمتسلّقات ليلًا",
     "alt_en": "Gabled glass-fronted cottage framed by climbing plants at night"},
    {"img": "work-2023-b", "year": "2023",
     "alt_ar": "ممرّ بين الأكواخ بعد المطر، والضوء ينعكس على الأرض",
     "alt_en": "Path between the cottages after rain, light reflected on the ground"},
    {"img": "work-2024", "year": "2024",
     "alt_ar": "صالة بيضاء بسقف جمالوني ونافذة عالية تطلّ على السهل",
     "alt_en": "White living space under a gable, its tall window opening onto the plain"},
    # 2026 — the house with the arcades and the stone block majlis, Amman
    {"img": "work-2026-a", "year": "2026",
     "alt_ar": "فناء البيت عند الغروب، ومقاعد الكتل الحجرية في المقدّمة",
     "alt_en": "The courtyard at sunset, the stone block seats in the foreground"},
    {"img": "work-2026-b", "year": "2026",
     "alt_ar": "مجلس داخلي بثلاثة عقود يكسوها السجاد، وسقف من الخشب والقصب",
     "alt_en": "An interior majlis with three carpeted arches under a timber and reed ceiling"},
    {"img": "work-2026-c", "year": "2026",
     "alt_ar": "المجلس الداخلي بفوانيسه النحاسية وعقوده المكسوّة بالسجاد",
     "alt_en": "The interior majlis with its brass lanterns and carpeted arches"},
    {"img": "work-2026-d", "year": "2026",
     "alt_ar": "محاريب للرفوف بإضاءة دافئة ليلًا، وإلى جانبها درابزين حديدي",
     "alt_en": "Arched shelf niches in warm light at night, beside an iron railing"},
    {"img": "work-2026-e", "year": "2026",
     "alt_ar": "رواق معقود تضيئه الفوانيس ليلًا، وفي آخره مرآة بإطار خشبي",
     "alt_en": "An arched gallery lit by lanterns at night, a timber-framed mirror at its end"},
    {"img": "work-2026-f", "year": "2026",
     "alt_ar": "شجرة زيتون أمام الدرج الخارجي، وحولها الجهنمية",
     "alt_en": "An olive tree before the outdoor stair, bougainvillea around it"},
    {"img": "work-2026-g", "year": "2026",
     "alt_ar": "عقد أبيض يُرى من بين أغصان الزيتون، وفي داخله رواق بالفوانيس",
     "alt_en": "A white arch seen through olive branches, a lantern-lit gallery inside"},
    {"img": "work-2026-h", "year": "2026",
     "alt_ar": "مظلّة خشبية فوق عقد المدخل، وفانوس حديدي على الجدار",
     "alt_en": "A timber canopy above the entrance arch, an iron lantern on the wall"},
    {"img": "work-2026-i", "year": "2026",
     "alt_ar": "رواق بسقف من الجسور الخشبية والقصب، تتقابل فيه العقود والمرآة",
     "alt_en": "A gallery under timber beams and reed, arches facing a mirror"},
    {"img": "work-2026-j", "year": "2026",
     "alt_ar": "واجهة معقودة بالفوانيس، وفوقها مظلّة خشبية ونباتات متسلّقة",
     "alt_en": "An arcaded front with lanterns, a timber awning and climbing plants"},
    {"img": "work-2026-k", "year": "2026",
     "alt_ar": "عريشة خشبية مسقوفة بالقصب فوق طاولة طويلة، وخلفها ثلاثة محاريب",
     "alt_en": "A reed-roofed timber pergola over a long table, three niches behind it"},
    {"img": "work-2026-l", "year": "2026",
     "alt_ar": "مغسلة على رفّ خشبي تحت مرآة معقودة، بإضاءة دافئة",
     "alt_en": "A basin on a timber shelf beneath an arched mirror, in warm light"},
]

# The latest work, opening the works section: a wide view and the
# maker in the place. (base, widths, w, h)
LEAD_IMG = {
    "home-facade": ([1600, 1200, 800], 1600, 900),
    "home-majed":  ([864, 600], 864, 1080),
}

# The hero horizon: two rows of 12 squares (<img>-400.webp), old and
# new work interleaved. hero-2026-* exist only as 400px squares.
HERO_ROWS = [
    ["work-2016", "hero-2026-d", "work-2007", "work-2026-b", "work-2018",
     "hero-2026-a", "work-2013", "work-2026-f", "work-2023", "work-2026-j",
     "work-2015", "work-2026-k"],
    ["work-2026-g", "work-2012", "hero-2026-b", "work-2017", "work-2026-d",
     "work-2018-b", "hero-2026-c", "work-2020", "work-2026-e", "work-2024",
     "work-2026-i", "work-2023-b"],
]

# Al-Aqsa car story images. Basenames live in assets/img as
# <img>-<w>.webp for every w listed, plus <img>-<w0>.jpg for the first.
AQSA_IMG = {
    "aqsa-model-a":  ([828, 800, 500], 828, 466),
    "aqsa-model-b":  ([1200, 800, 500], 1200, 675),
    "aqsa-chassis":  ([1032, 800, 500], 1032, 581),
    "aqsa-body":     ([1200, 800, 500], 1200, 900),
    "aqsa-stone":    ([719, 500], 719, 404),
    "aqsa-drive":    ([750, 500], 750, 500),
    "aqsa-indoor":   ([456], 456, 257),
    "aqsa-night":    ([1200, 800, 500], 1200, 675),
    "aqsa-dome":     ([1200, 800, 500], 1200, 800),
    "aqsa-court":    ([1200, 800, 500], 1200, 675),
    "aqsa-people-a": ([784, 500], 784, 441),
    "aqsa-people-b": ([482], 482, 271),
}

# The Stone Block Majlis project page. Same naming rule as above:
# <img>-<w>.webp for every w listed, plus <img>-<w0>.jpg for the first.
# The widths are the real pixel widths of the crops — never upscaled.
MONO_IMG = {
    # all from the 2026 shoot; block, sky, above and table are stills
    # from the film, cropped above its subtitles
    "mono-hero":   ([1600, 1100, 800], 1600, 900),
    "mono-hero-m": ([864], 864, 1080),
    "mono-above":  ([1600, 1200, 800], 1600, 900),
    "mono-block":  ([720, 500], 720, 900),
    "mono-seat":   ([800, 500], 800, 800),
    "mono-wall":   ([1200, 800], 1200, 900),
    "mono-table":  ([1200, 800], 1200, 800),
    "mono-sky":    ([600], 600, 900),
    "mono-court":  ([1600, 1200, 800], 1600, 900),
    "mono-front":  ([1600, 1200, 800], 1600, 900),
}

# The Emirati House (emirati.html). Same naming rule as above.
HOUSE_IMG = {
    "house-hero":       ([1600, 1100, 800], 1600, 900),
    "house-hero-m":     ([864], 864, 1080),
    "house-night":      ([1600, 1200, 800], 1600, 900),
    "house-arcade":     ([864, 600], 864, 1080),
    "house-canopy":     ([1200, 800], 1200, 900),
    "house-olive-arch": ([864, 600], 864, 1080),
    "house-gallery":    ([864, 600], 864, 1080),
    "house-corridor":   ([864, 600], 864, 1080),
    "house-door":       ([1200, 800], 1200, 900),
    "house-majlis":     ([1600, 1200, 800], 1600, 900),
    "house-majlis-b":   ([1200, 800], 1200, 900),
    "house-niches":     ([864, 600], 864, 1080),
    "house-olive":      ([1600, 1200, 800], 1600, 900),
    "house-above":      ([1200, 800], 1200, 900),
    "house-pergola":    ([1200, 800], 1200, 900),
    "house-basin":      ([864, 600], 864, 1080),
    "house-majed":      ([864, 600], 864, 1080),
    "house-reel":       ([864, 600], 864, 1080),
    "house-side":       ([1600, 1200, 800], 1600, 900),
    "house-entrance":   ([1200, 800], 1200, 900),
    "house-basin-arch": ([864, 600], 864, 1080),
    "house-carpet":     ([864, 600], 864, 1080),
    "house-kitchen":    ([864, 600], 864, 1080),
}
HOUSE_REEL = "https://www.instagram.com/reel/DerwBd5ItFg/"

# ============================================================
# 2. CONTENT — Arabic / English
#
# VOICE: first person. Majed speaks for himself — "أعمل"، "أسّست" —
# never in the third person.
#
# TYPOGRAPHY CONSTRAINT — read before editing Arabic headings:
# "Majed Arabic" is used for Arabic headings only (hero name, section
# titles, Athar title, contact title). That font draws a FINAL yaa (ـي)
# detached from the letter before it, so any heading word ending in ي
# renders as broken letters. Keep such wording in .meta / .lead /
# .prose, which use Thmanyah and join every letter correctly.
# ============================================================

AR = {
    "lang": "ar", "dir": "rtl", "other": "en", "other_label": "EN", "self_label": "AR",
    
    
    # An entry may carry a third element: the project pages listed
    # under it (a quiet sub-menu on desktop, nested rows on mobile).
    "nav": [("#top", "الرئيسية"),
            ("#works", "الأعمال", [("emirati.html", "البيت الإماراتي"),
                                   ("monolith.html", "مجلس الكتل الحجرية"),
                                   ("aqsa.html", "سيارة الأقصى")]),
            ("#about", "عن ماجد"), ("#athar", "أثر"),
            ("contact.html", "تواصل")],
    "nav_sub_label": "مشاريع من الأعمال",
    "skip": "تخطّي إلى المحتوى",
    "menu_open": "فتح القائمة",
    "home_href": "index.html", "contact_href": "contact.html",

    "hero_greet": "حيّاكم الله في مساحتي",
    "hero_name": "ماجد ناموس",
    "hero_lead": "أعيش بين العمارة والإعلام الوقفي، أبحث عن الأثر الذي يتركه الإنسان في المكان، وعن الحكاية التي تستحق أن تُروى.",
    "hero_cue": "الأعمال في الأسفل",

    "works_title": "الأعمال",
    "works_meta": "<span dir=\"ltr\">2007 - 2018</span>",
    "lead_facade_alt": "واجهة البيت البيضاء بعقودها الثلاثة ومظلّاتها الخشبية، وأمامها فناء من الرخام",
    "lead_majed_alt": "ماجد ناموس جالسًا إلى الطاولة تحت العريشة، وخلفه المحاريب المضاءة",
    "lead_majed_cap": "في المكان",

    "about_meta": "عن ماجد",
    "about_body": [
        "وُلدتُ في عمّان، وتنقّلتُ بين مدنٍ وبيئاتٍ مختلفة، وكانت لكل بيئةٍ منها إسهامها في نظرتي إلى المكان، وفي تكوين ذائقتي البصرية.",
        "منذ سنوات، وجدتُ في العمارة العربية والإسلامية لغةً تتجاوز البناء؛ ذاكرةً للمكان، وتعبيرًا عن هويته وثقافته. ومن هذا الشغف جاءت تجارب ومشاريع امتدت لأكثر من عقدين، استلهمتُ فيها روح العمارة العريقة وقدّمتها برؤية معاصرة تحترم أصلها.",
        "وبموازاة ذلك، ارتبط عملي بالإعلام الوقفي وتوثيق أثر المؤسسات ومبادراتها. وفي عام 2021 أسستُ مؤسسة أثر للإعلام الوقفي، لتكون مساحةً متخصصة في إبراز أثر الوقف، وتوثيق قصصه، وتقديمها بصورة تليق بما تصنعه هذه المؤسسات في مجتمعاتها.",
    ],
    "about_facts": [("المكان", "عمّان، الأردن"),
                    ("المجال", "عمارة وتصميم · إعلام وقفي")],
    "about_portrait_alt": "صورة شخصية لماجد ناموس",

    "athar_title": "مؤسسة أثر",
    "athar_meta": "للإعلام الوقفي - تأسست <span dir=\"ltr\">2021</span>",
    "athar_body": [
        "في عام 2021، أسستُ مؤسسة أثر للإعلام الوقفي وأتولى إدارتها، انطلاقًا من إيماني بأن أثر الوقف لا يكتمل بصناعته فحسب، بل بتوثيقه وحفظ حكايته وإيصالها.",
        "عملت المؤسسة منذ تأسيسها مع عدد من المؤسسات الوقفية، وأسهمت في توثيق مبادراتها ومشروعاتها وإبراز أثرها؛ بلغة إعلامية تمنح هذه الأعمال ما تستحقه من حضور.",
    ],
    "athar_cta": "زيارة موقع مؤسسة أثر",
    "athar_logo_alt": "شعار مؤسسة أثر",

    "film_meta": "مؤتمر المدينة المنورة للأوقاف - <span dir=\"ltr\">2022</span>",
    "film_title": "«أوقاف المدينة.. كيان وإحسان»",
    "film_body": [
        "أُقيم المؤتمر تحت رعاية صاحب السمو الملكي أمير منطقة المدينة المنورة، وعُرض فيه هذا الفيلم الوثائقي من إنتاج مؤسسة أثر للإعلام الوقفي.",
        "وفي المناسبة ذاتها، حظيتُ أنا وفريقي في المؤسسة بالشكر، تقديرًا لجهودها ومساهمتها في إنتاج العمل.",
    ],
    "film_play": "شاهد الفيلم",
    "film_alt": "لقطة من الفيلم الوثائقي «أوقاف المدينة.. كيان وإحسان»",

    "cottages_meta": "شارع الأردن - تأسست <span dir=\"ltr\">2023</span>",
    "cottages_title": "أكواخ الماجد",
    "cottages_body": [
        "في عام 2023، أنشأتُ أكواخ الماجد في شارع الأردن بمدينة عمّان، وتولّيت تصميمها وتنفيذها، من الفكرة الأولى وحتى تفاصيلها الأخيرة.",
        "كان اهتمامي أن تكون المساحات مدروسة وقريبة من الإنسان؛ تمنح من يدخلها شعورًا بالألفة والراحة، بعيدًا عن الطابع المعتاد لأماكن الإقامة المؤقتة. أردتُ لكل كوخ أن يحمل إحساس البيت وخصوصيته، وأن تكون العمارة فيه جزءًا هادئًا من التجربة، لا مجرد إطارٍ لها.",
    ],
    "cottages_logo_alt": "شعار أكواخ الماجد",

    "media_title": "لقاء",
    "media_meta": "قناة الجزيرة - <span dir=\"ltr\">2017</span>",
    "media_headline": "لقائي على قناة الجزيرة",
    "media_note": "اضغط للمشاهدة",
    "media_alt": "غلاف لقاء ماجد ناموس على قناة الجزيرة",
    "media_story": [
        "بعض الأماكن أبعد من أن تختزلها الصور، لأنها تحمل في الذاكرة معنى أكبر. والمسجد الأقصى واحدٌ منها.",
        "من هنا جاءت فكرة سيارة المسجد الأقصى؛ محاولة مختلفة لإحياء صورته بين الناس، وإبقاء حضوره حيًّا في ذاكرتهم ووجدانهم. وحول هذه الفكرة وقصتها، كان لقائي مع قناة الجزيرة.",
    ],
    "media_story_alt": "سيارة المسجد الأقصى: مجسّم على هيئة سيارة يحمل قبة الصخرة وأسوار المدينة",

    "aqsa_cta": "قصة سيارة المسجد الأقصى",
    "aqsa_page_title": "سيارة المسجد الأقصى - ماجد ناموس",
    "aqsa_desc": "قصة سيارة المسجد الأقصى: مبادرة شخصية لإبقاء صورة الأقصى حاضرة بين الناس.",
    "aqsa_eyebrow": "<span dir=\"ltr\">2017</span>",
    "aqsa_title": "سيارة المسجد الأقصى",
    "aqsa_sub": "فكرة مختلفة، هدفها أن تبقى صورة المسجد الأقصى حاضرة بين الناس.",
    "aqsa_hero_alt": "سيارة المسجد الأقصى بعد اكتمالها، وقبة الصخرة على مؤخرتها",

    "aqsa_h1": "الفكرة",
    "aqsa_p1": [
        "بدأت الفكرة من سؤال بسيط: كيف يمكن أن تبقى صورة المسجد الأقصى أمام الناس، لا في الصور فقط، بل كجزء من حياتهم اليومية؟",
        "من هنا فكرت أن أصنع شيئًا مختلفًا؛ أن أحمل صورة الأقصى على سيارة تتحرك بين الناس، يراها من يمشي في الشارع، ومن يقف بجانبها، ومن تصادفه في طريقه.",
        "اخترت السيارة لأنها تتحرك باستمرار وتصل إلى أماكن مختلفة. وهكذا أصبحت الفكرة واضحة بالنسبة لي: بدل أن تبقى صورة الأقصى ثابتة في مكان واحد، لماذا لا نجعلها هي التي تذهب إلى الناس؟",
        "كان هدفي بسيطًا: أن يراه الناس، ويتذكرونه، وتبقى صورته حاضرة في الذاكرة.",
    ],

    "aqsa_h2": "أول خطوة",
    "aqsa_p2": [
        "قبل أن أبدأ العمل على السيارة، صنعت مجسّمًا صغيرًا حتى أرى الفكرة أمامي بشكل حقيقي، وأعرف كيف يمكن توزيع القبة والأسوار والساحات على مساحة السيارة.",
        "كانت هذه أول خطوة لتحويل الفكرة من تصور في ذهني إلى شيء يمكن تنفيذه.",
        "بعد ذلك بدأ العمل على السيارة نفسها. تم تجريدها حتى الهيكل، ومن هذه النقطة بدأ البناء خطوة بخطوة.",
    ],
    "aqsa_cap_model": "المجسّم الأول: تصور مبدئي لتوزيع القبة والأسوار والساحات على السيارة.",
    "aqsa_cap_chassis": "نقطة البداية - السيارة بعد تجريدها حتى الهيكل.",
    "aqsa_alt_model_a": "مجسّم أبيض مصغّر يوضح توزيع المسجد والأسوار على هيئة سيارة",
    "aqsa_alt_model_b": "المجسّم الأبيض من الأعلى، وتظهر فيه الساحات وموضع المقود",
    "aqsa_alt_chassis": "هيكل سيارة مجرّد من جسمها في ساحة ورشة",

    "aqsa_h3": "حين بدأت الفكرة تأخذ شكلها",
    "aqsa_p3": [
        "من الهيكل بدأت السيارة تتغير تدريجيًا. تم بناء الجسم المعدني وقصّ القطع وتشكيلها ولحامها حتى أصبح لدينا الأساس الذي سيحمل بقية التفاصيل.",
        "ثم بدأت المرحلة التي احتاجت إلى أكبر قدر من الدقة: الأقواس، والعقود، والحجارة، والتفاصيل المعمارية الصغيرة.",
        "التحدي كان أن نحافظ قدر الإمكان على شكل هذه التفاصيل ونِسَبها، ولكن هذه المرة على جسم سيارة متحركة ومساحة محدودة جدًا.",
        "أشرفت على المشروع ونفذت معظم تفاصيله بنفسي، مع الاستعانة ببعض الفنيين في المراحل التي احتاجت إلى خبرة فنية متخصصة.",
    ],
    "aqsa_cap_body": "بناء الجسم المعدني على الهيكل قبل إضافة التفاصيل والكسوة الخارجية.",
    "aqsa_cap_stone": "العقود والأقواس أثناء تشكيلها وتركيبها قطعةً قطعة.",
    "aqsa_alt_body": "جسم معدني ملحوم فوق هيكل السيارة داخل ورشة",
    "aqsa_alt_stone": "ماجد ناموس يعمل على عقود حجرية مصغّرة",

    "aqsa_h4": "الفكرة أصبحت واقعًا",
    "aqsa_p4": [
        "بعد مراحل طويلة من العمل، وصلت السيارة إلى شكلها النهائي، بتفاصيل مستوحاة من قبة الصخرة والمسجد القبلي والأسوار والساحات والأشجار والمداخل.",
        "بالنسبة لي، لم تكن الفكرة أن أصنع سيارة غريبة أو ملفتة فقط. كنت أريد أن أصنع شيئًا يجعل الناس يلتفتون إلى صورة المسجد الأقصى من تلقاء أنفسهم، ويسألون عنه ويتأملون تفاصيله.",
        "وفي الليل تظهر السيارة بصورة مختلفة تمامًا؛ الإضاءة تكشف تفاصيل القبة والزخارف والكتابات والساحات التي ربما لا تظهر بنفس الوضوح خلال النهار.",
    ],
    "aqsa_cap_night": "التفاصيل ليلًا، حيث تكشف الإضاءة جانبًا آخر من العمل.",
    "aqsa_alt_drive": "السيارة بعد اكتمالها في ساحة مفتوحة وماجد ناموس خلف المقود",
    "aqsa_alt_indoor": "السيارة المكتملة داخل قاعة، وتظهر عليها قبة الصخرة والأسوار",
    "aqsa_alt_night": "المجسّم مضاءً ليلًا، وتظهر القبة والأسوار والأشجار",
    "aqsa_alt_dome": "قبة الصخرة في المجسّم ليلًا، وتظهر فسيفساؤها وكتاباتها",
    "aqsa_alt_court": "ساحات المجسّم ليلًا، وتظهر فيها الأروقة والمئذنة والأشجار",

    "aqsa_h5": "حين التقت الفكرة بالناس",
    "aqsa_p5": [
        "بعد خروج السيارة إلى الشارع بدأت أرى الجزء الأجمل من الفكرة: تفاعل الناس معها.",
        "كان البعض يتوقف لمشاهدتها، والبعض يقترب ليرى التفاصيل، وآخرون يلتقطون الصور. وكان الأطفال تحديدًا يقتربون منها بفضول ويحاولون اكتشاف كل جزء فيها.",
        "وقتها شعرت أن الفكرة حققت ما أردته منها.",
        "لأن القيمة لم تكن في بناء السيارة وحده، بل في أن تصبح سببًا للحظة يتوقف فيها شخص، ينظر إلى المسجد الأقصى، ويتذكره.",
    ],
    "aqsa_alt_people_a": "أطفال يتجمّعون أمام المجسّم المعروض خلف زجاج",
    "aqsa_alt_people_b": "المجسّم معروضًا في الشارع خلف واجهة زجاجية",

    "aqsa_end": "ما نريد له أن يدوم داخل الذاكرة، لا بد أن يدوم أمام العين.",
    "aqsa_link_media": "لقائي على قناة الجزيرة حول الفكرة",
    "aqsa_link_contact": "تواصل معي",
    "aqsa_zoom": "عرض الصورة بحجم أكبر",
    "aqsa_close": "إغلاق",
    "aqsa_prev": "الصورة السابقة",
    "aqsa_next": "الصورة التالية",

    # --- The Stone Block Majlis (monolith.html) ---
    # First person, short, no superlatives. No figures, stone types,
    # areas or costs: only what was actually provided about the project.
    "mono_page_title": "مجلس الكتل الحجرية - ماجد ناموس",
    "mono_desc": "مجلس الكتل الحجرية: مجلس خارجي في عمّان صمّمته ونفّذته من كتل حجرية منفردة، يقوم كل مقعد رئيسي فيه على كتلة واحدة.",
    "mono_place": "عمّان، الأردن",
    "mono_date": "سبتمبر 2026",
    "mono_title": "مجلس الكتل الحجرية",
    "mono_title_alt": "The Stone Block Majlis",
    "mono_title_alt_lang": "en",
    "mono_hero_alt": "مجلس خارجي من كتل حجرية حول طاولة حجرية مستديرة، وخلفه جدار بفتحة دائرية وأخرى للحطب، والتلال في الأفق",
    "mono_open": "مجلس خارجي صُمّمت مقاعده من كتل حجرية منفردة، ليكون الحجر جزءًا من تكوين الجلسة نفسها.",

    "mono_h1": "الفكرة",
    "mono_p1": [
        "في هذا المشروع بدأ التصميم من الحجر نفسه. لم أتعامل معه ككسوة تُضاف إلى المقعد، بل ككتلةٍ هي التي تصنع المقعد وتمنحه حضوره. ومن هنا جاء مفهوم المشروع كله: لكل مقعد رئيسي كتلة حجرية واحدة.",
    ],

    "mono_h2": "الكتلة الواحدة",
    "mono_p2": [
        "كل مقعد هنا قائم على كتلة حجرية واحدة، تحضر في المكان عنصرًا معماريًا قبل أن تكون قطعة أثاث. وتركت سطحها خشنًا، لأني أردت أن يبقى الحجر حجرًا حتى وهو مقعد.",
    ],
    "mono_block_alt": "مقعد حجري قائم على كتلة واحدة، وعليه وسائد قماشية",

    "mono_h3": "الحجر والمجلس",
    "mono_p3": [
        "الحجر والمجلس كلاهما مألوف في بيوتنا في الأردن: الأول نبني به، والثاني نجتمع فيه. ما فعلته هنا أنني جمعتهما في تكوين واحد. بقي المجلس كما نعرفه، مقاعد متقابلة حول طاولة للضيافة والحديث، لكنه هذه المرة يأتي من الحجر، ويعيش في الهواء الطلق.",
    ],
    "mono_sky_alt": "الجدار الحجري بفتحته الدائرية عند الغروب، وإلى جانبها الحطب",
    "mono_court": ("المجلس في الفناء",
                   "المجلس في فناء البيت عند الغروب، والكتل الحجرية في المقدّمة"),

    "mono_h4": "التكوين",
    "mono_p4": [
        "التكوين بسيط: مقاعد تتحلّق حول طاولة حجرية مستديرة، وخلفها جدار يحتضن الحطب. حولها حصى أحمر ونباتات، فيما يبقى الحجر هو العنصر الأكثر حضورًا في المشهد.",
    ],
    # key: (label, alt)
    "mono_plates": {
        "mono-above": ("المشهد من الأعلى",
                       "المجلس من الأعلى عند الغروب، والحديقة من حوله"),
        "mono-seat": ("الكتلة والنبات", "كتل حجرية للجلوس خلف شجيرة جهنمية مزهرة، والجدار من ورائها"),
        "mono-wall": ("الحجر والحطب", "تفصيل من الجدار: حجر خشن السطح، وفتحة مستطيلة مملوءة بالحطب"),
        "mono-table": ("طاولة الوسط", "الطاولة الحجرية المستديرة في وسط المجلس"),
        "mono-front": ("في الليل", "المجلس ليلًا: النار في الفتحة الدائرية، وعلى الطاولة دلّة القهوة"),
    },

    "mono_film_title": "الجلسة الحجرية",
    "mono_film_note": "جولة قصيرة في المجلس، أحكي فيها عن فكرته، وعن الحجر حين صار جلسة.",
    "mono_film_play": "شاهد الفيلم",
    "mono_film_alt": "ماجد ناموس يتحدّث عن مجلس الكتل الحجرية",

    "mono_h5": "بيانات المشروع",
    "mono_info": [
        ("الموقع", "عمّان، الأردن"),
        ("تاريخ الإنجاز", "سبتمبر 2026"),
        ("المجال", '<span lang="en" dir="ltr">Landscape / Outdoor Architecture / Stone</span>'),
        ("الفكرة", "مجلس خارجي من كتل حجرية منفردة، يقوم كل مقعد رئيسي فيه على كتلة واحدة."),
        ("التصميم والتنفيذ", "ماجد ناموس"),
        ("المشروع", '<a class="link" href="emirati.html"><span>البيت الإماراتي</span></a>'),
    ],
    "mono_link_house": "البيت الإماراتي",

    "mono_end": ["لا شيء هنا أكثر من حجرٍ وجلسة.", "وهذا ما أردته."],
    "mono_sign_latin": "Majed Namous",
    "mono_link_works": "بقية الأعمال",
    "mono_link_contact": "تواصل معي",


    # --- The Emirati House (emirati.html) --- first person, very short
    "house_page_title": "البيت الإماراتي - ماجد ناموس",
    "house_desc": "البيت الإماراتي: أول بيت إماراتي في الأردن.",
    "house_place": "عمّان، الأردن",
    "house_date": "<span dir=\"ltr\">2026</span>",
    "house_title": "البيت الإماراتي",
    "house_title_alt": "The Emirati House",
    "house_hero_alt": "واجهة البيت البيضاء بعقودها الثلاثة ومظلّاتها الخشبية، وأمامها فناء من الرخام",
    "house_open": "أول بيت إماراتي في الأردن. عقود بيضاء، وأروقة، ومجالس، وفناء حول شجرة زيتون.",
    "house_ch": [
        ("الواجهة", "واجهة بيضاء بثلاثة عقود ومظلّات من الخشب."),
        ("العقود والأروقة", "عقود في الأبواب والممرّات والمحاريب."),
        ("الداخل", "في المضافة جلسات على امتداد الجدران، وسجاد إيراني في أعماق مقوّسة، وسقف من الخشب والقصب."),
        ("الفناء", "فناء حول شجرة زيتون، وعريشة للجلسات."),
    ],
    # key: (label, alt)
    "house_plates": {
        "house-night": ("في المساء", "البيت ليلًا بعقوده المضاءة، وأمامه سيارة كلاسيكية على أرضية الرخام"),
        "house-arcade": ("الرواق", "رواق من العقود البيضاء تضيئه الفوانيس، وأمامه شجرة زيتون"),
        "house-canopy": ("المظلّة", "مظلّة خشبية فوق عقد المدخل، وفانوس حديدي على الجدار"),
        "house-olive-arch": ("من بين الزيتون", "عقد أبيض يُرى من بين أغصان الزيتون، وفي داخله رواق بالفوانيس"),
        "house-gallery": ("السقف", "رواق بسقف من الجسور الخشبية والقصب، تتقابل فيه العقود والمرآة"),
        "house-corridor": ("الممرّ", "ممرّ معقود تضيئه الفوانيس ليلًا، وفي آخره مرآة بإطار خشبي"),
        "house-door": ("الباب", "باب معقود بستارة بيضاء، وعلى جانبيه فوانيس مضاءة ليلًا"),
        "house-majlis": ("المضافة", "المضافة: جلسات على امتداد الجدار، وسجاد إيراني في ثلاثة أعماق مقوّسة، وسقف من الخشب والقصب"),
        "house-majlis-b": ("الفوانيس", "المضافة بفوانيسها النحاسية وجلساتها البيضاء ووسائدها الحمراء"),
        "house-side": ("الواجهة الجانبية", "واجهة البيت الجانبية بعقودها ومظلّاتها الخشبية، وأمامها شجرة زيتون في حوض دائري"),
        "house-entrance": ("المدخل ليلًا", "عقدا المدخل مضاءان ليلًا، والفوانيس على الجدار"),
        "house-basin-arch": ("تحت الدرج", "مغسلة داخل عقد تحت الدرج، يضيئها فانوس معلّق"),
        "house-carpet": ("السجاد الإيراني", "سجادة إيرانية في عمق مقوّس داخل جدار المضافة"),
        "house-kitchen": ("بين الزيتون", "المطبخ الخارجي والعريشة من بين أشجار الزيتون"),
        "house-niches": ("المحاريب", "محاريب للرفوف بإضاءة دافئة ليلًا، وإلى جانبها درابزين حديدي"),
        "house-olive": ("الزيتونة", "شجرة زيتون أمام الدرج الخارجي، وحولها الجهنمية"),
        "house-above": ("من الأعلى", "الفناء من الأعلى: شجرة الزيتون في حوضها، والعريشة والدرج"),
        "house-pergola": ("العريشة", "عريشة خشبية مسقوفة بالقصب فوق طاولة طويلة، وخلفها ثلاثة محاريب"),
        "house-basin": ("المغسلة", "مغسلة على رفّ خشبي تحت مرآة معقودة، بإضاءة دافئة"),
    },
    "house_reel_title": "جولة في البيت",
    "house_reel_note": "من داخل البيت وفنائه.",
    "house_reel_play": "شاهد المقطع",
    "house_reel_open": "فتح المقطع على إنستغرام",
    "house_reel_alt": "البيت الإماراتي ليلًا، غلاف المقطع",
    "house_reel_frame": "مقطع البيت الإماراتي على إنستغرام",
    "house_majlis_title": "مجلس الكتل الحجرية",
    "house_majlis_line": "جزء من البيت: مجلس خارجي من كتل حجرية.",
    "house_majlis_alt": "مجلس الكتل الحجرية في البيت الإماراتي: مقاعد من كتل حجرية حول طاولة مستديرة، وخلفها جدار بفتحة دائرية",
    "house_h_info": "بيانات المشروع",
    "house_info": [
        ("الموقع", "عمّان، الأردن"),
        ("السنة", "<span dir=\"ltr\">2026</span>"),
        ("الطابع", "عمارة إماراتية"),
        ("التصميم والتنفيذ", "ماجد ناموس"),
    ],
    "house_majed_alt": "ماجد ناموس جالسًا إلى الطاولة تحت العريشة، وخلفه المحاريب المضاءة",
    "house_majed_cap": "في المكان",
    "house_link_majlis": "مجلس الكتل الحجرية",
    "house_link_works": "بقية الأعمال",
    "house_link_contact": "تواصل معي",

    "contact_title": "تواصل",
    "contact_lead": "أسعد بتواصلكم حول المشاريع المعمارية، أو فرص التعاون في الإعلام الوقفي ومشاريع مؤسسة أثر.",
    "f_name": "الاسم الكريم",
    "f_name_ph": "ماجد أبو ناموس",
    "f_email": "البريد الإلكتروني",
    "f_email_ph": "info@majednamous.com",
    "f_subject": "موضوع التواصل",
    "f_subjects": ["مشروع معماري",
                   "تعاون مع مؤسسة أثر للإعلام الوقفي",
                   "إعلام وتوثيق",
                   "استفسار آخر"],
    "f_message": "رسالتك",
    "f_message_ph": "اكتب تفاصيل الاستفسار أو فكرة التعاون…",
    "f_submit": "إرسال الرسالة",
    "f_sending": "جارٍ الإرسال…",
    "f_ok": "شكرًا لتواصلك، وصلت رسالتك بنجاح.",
    "f_fail": "تعذّر الإرسال الآن. يمكنك مراسلتي مباشرة على info@majednamous.com",
    "f_unconfigured": "نموذج الإرسال غير موصول بخادم بعد، فلن تصل الرسالة من هنا. راسلني مباشرة على info@majednamous.com أو على الهاتف أدناه.",

    "footer_tag": "في عمارة البنيان، وتوثيق أثر الإنسان.",
    "footer_nav_title": "روابط",
    "footer_contact_title": "تواصل",
    "footer_rights": "جميع الحقوق محفوظة.",
    "footer_name": "ماجد ناموس",
}

EN = {
    "lang": "en", "dir": "ltr", "other": "ar", "other_label": "AR", "self_label": "EN",
    
    
    "nav": [("#top", "Home"),
            ("#works", "Works", [("emirati.html", "The Emirati House"),
                                 ("monolith.html", "The Stone Block Majlis"),
                                 ("aqsa.html", "The Al-Aqsa Car")]),
            ("#about", "About"), ("#athar", "Athar"),
            ("contact.html", "Contact")],
    "nav_sub_label": "Selected projects",
    "skip": "Skip to content",
    "menu_open": "Open menu",
    "home_href": "index.html", "contact_href": "contact.html",

    "hero_greet": "Welcome to my space",
    "hero_name": "Majed Namous",
    "hero_lead": "I live between architecture and waqf media, looking for the mark a person leaves on a place, and for the story worth telling.",
    "hero_cue": "Works below",

    "works_title": "Works",
    "lead_facade_alt": "The white front of the house, its three arches and timber canopies, a marble court before it",
    "lead_majed_alt": "Majed Namous seated at the table under the pergola, the lit niches behind him",
    "lead_majed_cap": "In the place",

    "about_meta": "About",
    "about_body": [
        "I was born in Amman, and have moved between different cities and settings. Each of them added something to how I read a place, and to the way my eye was formed.",
        "For years now I have found in Arab and Islamic architecture a language that goes past building: a memory of a place, and an expression of its identity and its culture. Out of that came work and projects spanning more than two decades, drawing on the spirit of that older architecture and presenting it in a contemporary reading that respects where it came from.",
        "Alongside this, my work has been tied to waqf media and to documenting the impact of institutions and their initiatives. In 2021 I founded Athar Foundation for Waqf Media, as a space dedicated to bringing the impact of waqf into view, documenting its stories, and presenting them in a way worthy of what these institutions do for their communities.",
    ],
    "about_facts": [("Based", "Amman, Jordan"),
                    ("Field", "Architecture &amp; design · Waqf media")],
    "about_portrait_alt": "Portrait of Majed Namous",

    "athar_title": "Athar Foundation",
    "athar_body": [
        "In 2021 I founded Athar Foundation for Waqf Media, and I run it. It came out of a conviction that the impact of an endowment is not complete in the making of it alone, but in documenting it, keeping its story, and carrying that story to people.",
        "Since then the foundation has worked with a number of endowment institutions, documenting their initiatives and projects and bringing their impact into view, in a media language that gives this work the presence it deserves.",
    ],
    "athar_cta": "Visit Athar Foundation",
    "athar_logo_alt": "Athar Foundation logo",

    "film_meta": "Madinah Waqf Conference - 2022",
    "film_title": "Awqaf of Madinah: Entity and Benevolence",
    "film_body": [
        "The conference was held under the patronage of His Royal Highness the Prince of the Madinah Region, and this documentary film, produced by Athar Foundation for Waqf Media, was screened there.",
        "On the same occasion, my team at the foundation and I were thanked, in recognition of the foundation's efforts and its part in producing the work.",
    ],
    "film_play": "Watch the film",
    "film_alt": "A still from the documentary film Awqaf of Madinah",

    "cottages_title": "Al Majed Cottages",
    "cottages_body": [
        "In 2023 I built Al Majed Cottages on Jordan Street in Amman, designing them and overseeing the work, from the first idea through to the last detail.",
        "What mattered to me was that the spaces be considered and close to the person in them - that anyone who walks in feels a familiarity and an ease far from the usual character of short-stay places. I wanted each cottage to carry the feeling and the privacy of a home, and the architecture to be a quiet part of the experience rather than merely a frame around it.",
    ],
    "cottages_logo_alt": "Al Majed Cottages logo",

    "media_title": "Conversation",
    "media_meta": "Al Jazeera - 2017",
    "media_headline": "My conversation on Al Jazeera",
    "media_note": "Watch the conversation",
    "media_alt": "Cover of Majed Namous's Al Jazeera interview",
    "media_story": [
        "Some places are more than a photograph can hold, because they carry a larger meaning in memory. Al-Aqsa is one of them.",
        "That is where the idea of the Al-Aqsa car came from: a different attempt to keep its image alive among people, and present in their memory and their hearts. My conversation with Al Jazeera was about that idea and its story.",
    ],
    "media_story_alt": "The Al-Aqsa car: a model in the form of a vehicle carrying the Dome of the Rock and the city walls",

    "aqsa_cta": "The story of the Al-Aqsa car",
    "aqsa_page_title": "The Al-Aqsa Car - Majed Namous",
    "aqsa_desc": "The story of the Al-Aqsa car: a personal initiative to keep the image of Al-Aqsa present among people.",
    "aqsa_eyebrow": "A personal initiative - 2017",
    "aqsa_title": "The Al-Aqsa Car",
    "aqsa_sub": "An idea that moves among people, so the image of Al-Aqsa stays in memory.",
    "aqsa_hero_alt": "The finished Al-Aqsa car, the Dome of the Rock rising at its rear",

    "aqsa_h1": "The idea",
    "aqsa_p1": [
        "Some places are not served by a picture on a wall, because what they hold in memory is wider than any frame. Al-Aqsa is one of them.",
        "That is where the idea came from: to move its image out of a fixed place and into something that travels among people and meets them in an ordinary day. I chose a car precisely because a car is among the things that pass in front of us without being noticed, so if it carries the image of Al-Aqsa, the passing itself becomes a reminder.",
        "I did not want a work to be seen once and be done with. I wanted a presence that returns on the road, and stays in memory.",
    ],

    "aqsa_h2": "From an idea to a beginning",
    "aqsa_p2": [
        "The work began with a small model I built first, so I could see the idea in front of me: where the dome would sit, how the walls and courtyards would be arranged across the length of one car, and where the driver would sit among all of it.",
        "The real beginning was an ordinary car, stripped back to its bare chassis - the ground everything else would be built on.",
    ],
    "aqsa_cap_model": "The first model: the dome, the walls and the courtyards set out across the car.",
    "aqsa_cap_chassis": "Point zero - the car stripped back to its chassis.",
    "aqsa_alt_model_a": "A small white model showing the mosque and walls laid out in the shape of a car",
    "aqsa_alt_model_b": "The white model seen from above, its courtyards and the driver position visible",
    "aqsa_alt_chassis": "A car stripped of its body, standing in a workshop yard",

    "aqsa_h3": "When the idea began to take shape",
    "aqsa_p3": [
        "From the bare chassis the body was built again: sheets cut, welded and shaped, until the mass that would carry the mosque stood straight.",
        "Then came the finer part - the arches and the stonework, carved and set one piece at a time. The hardest thing was keeping the architectural detail exact while it was being built on the body of a car rather than on solid ground.",
        "I oversaw the project and carried out most of its detail myself, calling on a few craftsmen for the work that needed specialised skill.",
    ],
    "aqsa_cap_body": "The metal body built onto the chassis, before the stonework.",
    "aqsa_cap_stone": "The arches carved and set one piece at a time.",
    "aqsa_alt_body": "A welded metal body over a car chassis inside a workshop",
    "aqsa_alt_stone": "Majed Namous working on small-scale stone arches",

    "aqsa_h4": "The idea became real",
    "aqsa_p4": [
        "The car was finished carrying the Dome of the Rock, the Qibli mosque, the walls and the courtyards - their stone, their ornament, their trees and their gateways.",
        "The point was never to change the shape of a car. It was to find a way for the image of Al-Aqsa to move among people and draw attention to itself, with no sign and no explanation.",
        "At night, when the detail is lit, the work reads more closely still: the mosaic on the dome, the inscriptions along its walls, the trees standing in the courtyards.",
    ],
    "aqsa_cap_night": "The detail at night, when light shows what daylight does not.",
    "aqsa_alt_drive": "The finished car in an open yard, Majed Namous at the wheel",
    "aqsa_alt_indoor": "The finished car indoors, the dome and the walls visible along it",
    "aqsa_alt_night": "The model lit at night, dome, walls and trees in view",
    "aqsa_alt_dome": "The Dome of the Rock on the model at night, its mosaic and inscriptions visible",
    "aqsa_alt_court": "The model courtyards at night, arcades, minaret and trees",

    "aqsa_h5": "When the idea met people",
    "aqsa_p5": [
        "When the car went out onto the road, people stopped at it. They came close to look at the detail and to take photographs, and the children were the most curious of them, nearest to the glass.",
        "That is where the idea felt complete, because its meaning was never in the car itself, but in what happens when it meets people.",
    ],
    "aqsa_alt_people_a": "Children gathered in front of the model displayed behind glass",
    "aqsa_alt_people_b": "The model displayed on the street behind a glass front",

    "aqsa_end": "What we want kept in memory has first to be kept in front of the eye.",
    "aqsa_link_media": "My conversation on Al Jazeera about the idea",
    "aqsa_link_contact": "Get in touch",
    "aqsa_zoom": "View larger",
    "aqsa_close": "Close",
    "aqsa_prev": "Previous image",
    "aqsa_next": "Next image",

    # --- The Stone Block Majlis (en/monolith.html) ---
    "mono_page_title": "The Stone Block Majlis - Majed Namous",
    "mono_desc": "The Stone Block Majlis: an outdoor majlis in Amman that I designed and built from single blocks of stone, where every main seat rests on one block.",
    "mono_place": "Amman, Jordan",
    "mono_date": "September 2026",
    "mono_title": "The Stone Block Majlis",
    "mono_title_alt": "مجلس الكتل الحجرية",
    "mono_title_alt_lang": "ar",
    "mono_hero_alt": "An outdoor majlis of stone blocks around a round stone table, a wall behind it with a round opening and a niche of firewood, hills on the horizon",
    "mono_open": "An outdoor majlis whose seats are designed from single blocks of stone, so that the stone is part of the seating itself.",

    "mono_h1": "The idea",
    "mono_p1": [
        "In this project the design began with the stone itself. I did not treat it as a finish added to the seat, but as the mass that makes the seat and gives it its presence. The whole concept follows from that: one block of stone for every main seat.",
    ],

    "mono_h2": "The single block",
    "mono_p2": [
        "Every seat here rests on a single block of stone, present in the space as an architectural element before it is a piece of furniture. I left its surface rough, because I wanted the stone to remain stone even as a seat.",
    ],
    "mono_block_alt": "A stone seat resting on a single block, with fabric cushions on it",

    "mono_h3": "Stone and the majlis",
    "mono_p3": [
        "Stone and the majlis are both familiar in our homes in Jordan: we build with one and gather in the other. What I did here was bring them together in one composition. The majlis stays as we know it, seats facing each other around a table for hospitality and conversation, but this time it comes from stone and lives in the open air.",
    ],
    "mono_sky_alt": "The stone wall and its round opening at dusk, firewood beside it",
    "mono_court": ("The majlis in the courtyard",
                   "The majlis in the courtyard of the house at sunset, the stone blocks in the foreground"),

    "mono_h4": "Composition",
    "mono_p4": [
        "The composition is simple: seats gathered around a round stone table, with a wall behind them that holds the firewood. Around them are red gravel and planting, while the stone remains the strongest presence in the scene.",
    ],
    "mono_plates": {
        "mono-above": ("From above",
                       "The majlis from above at dusk, the garden around it"),
        "mono-seat": ("Block and planting", "Stone seating blocks behind a flowering bougainvillea, the wall beyond"),
        "mono-wall": ("Stone and firewood", "A detail of the wall: rough-faced stone and a rectangular niche of firewood"),
        "mono-table": ("The central table", "The round stone table at the centre of the majlis"),
        "mono-front": ("At night", "The majlis at night: fire in the round opening, a coffee pot on the table"),
    },

    "mono_film_title": "The Stone Seating",
    "mono_film_note": "A short walk through the majlis, in which I talk about its idea, and about the stone once it became a place to sit.",
    "mono_film_play": "Watch the film",
    "mono_film_alt": "Majed Namous talks about the Stone Block Majlis",

    "mono_h5": "Project information",
    "mono_info": [
        ("Location", "Amman, Jordan"),
        ("Completed", "September 2026"),
        ("Field", "Landscape / Outdoor Architecture / Stone"),
        ("Concept", "An outdoor majlis of single stone blocks, with every main seat resting on one block."),
        ("Design and execution", "Majed Namous"),
        ("Project", '<a class="link" href="emirati.html"><span>The Emirati House</span></a>'),
    ],
    "mono_link_house": "The Emirati House",

    "mono_end": ["Nothing here is more than stone and a place to sit.", "That is what I wanted."],
    "mono_sign_latin": "Majed Namous",
    "mono_link_works": "Other works",
    "mono_link_contact": "Get in touch",


    # --- The Emirati House (en/emirati.html) ---
    "house_page_title": "The Emirati House - Majed Namous",
    "house_desc": "The Emirati House: the first Emirati house in Jordan.",
    "house_place": "Amman, Jordan",
    "house_date": "2026",
    "house_title": "The Emirati House",
    "house_title_alt": "البيت الإماراتي",
    "house_hero_alt": "The white front of the house, its three arches and timber canopies, a marble court before it",
    "house_open": "The first Emirati house in Jordan. White arches, galleries, majlis rooms, and a courtyard around an olive tree.",
    "house_ch": [
        ("The front", "A white front of three arches and timber canopies."),
        ("Arches and galleries", "Arches in the doors, the passages and the niches."),
        ("Inside", "In the guest room: seating along the walls, Iranian carpets set into arched recesses, and a ceiling of timber and reed."),
        ("The courtyard", "A courtyard around an olive tree, and a pergola for gathering."),
    ],
    "house_plates": {
        "house-night": ("Evening", "The house at night, its arches lit, a classic car on the marble court"),
        "house-arcade": ("The arcade", "An arcade of white arches lit by lanterns, an olive tree before it"),
        "house-canopy": ("The canopy", "A timber canopy above the entrance arch, an iron lantern on the wall"),
        "house-olive-arch": ("Through the olive", "A white arch seen through olive branches, a lantern-lit gallery inside"),
        "house-gallery": ("The ceiling", "A gallery under timber beams and reed, arches facing a mirror"),
        "house-corridor": ("The passage", "An arched passage lit by lanterns at night, a timber-framed mirror at its end"),
        "house-door": ("The door", "An arched door with a white curtain, lanterns lit on either side at night"),
        "house-majlis": ("The guest room", "The guest room: seating along the wall, Iranian carpets in three arched recesses, a ceiling of timber and reed"),
        "house-majlis-b": ("The lanterns", "The guest room with its brass lanterns, white seating and red cushions"),
        "house-side": ("The side front", "The side of the house, its arches and timber canopies, an olive tree in a round bed before it"),
        "house-entrance": ("The entrance at night", "The two entrance arches lit at night, lanterns on the wall"),
        "house-basin-arch": ("Under the stair", "A basin set in an arch beneath the stair, lit by a hanging lantern"),
        "house-carpet": ("Iranian carpet", "An Iranian carpet set into an arched recess in the guest room wall"),
        "house-kitchen": ("Through the olives", "The outdoor kitchen and pergola seen through the olive trees"),
        "house-niches": ("The niches", "Arched shelf niches in warm light at night, beside an iron railing"),
        "house-olive": ("The olive tree", "An olive tree before the outdoor stair, bougainvillea around it"),
        "house-above": ("From above", "The courtyard from above: the olive tree in its bed, the pergola and the stair"),
        "house-pergola": ("The pergola", "A reed-roofed timber pergola over a long table, three niches behind it"),
        "house-basin": ("The basin", "A basin on a timber shelf beneath an arched mirror, in warm light"),
    },
    "house_reel_title": "Around the house",
    "house_reel_note": "From inside the house and its courtyard.",
    "house_reel_play": "Watch the reel",
    "house_reel_open": "Open the reel on Instagram",
    "house_reel_alt": "The Emirati House at night, the reel cover",
    "house_reel_frame": "The Emirati House reel on Instagram",
    "house_majlis_title": "The Stone Block Majlis",
    "house_majlis_line": "Part of the house: an outdoor majlis of stone blocks.",
    "house_majlis_alt": "The Stone Block Majlis at the Emirati House: seats of stone blocks around a round table, a wall with a round opening behind",
    "house_h_info": "Project information",
    "house_info": [
        ("Location", "Amman, Jordan"),
        ("Year", "2026"),
        ("Character", "Emirati architecture"),
        ("Design and execution", "Majed Namous"),
    ],
    "house_majed_alt": "Majed Namous seated at the table under the pergola, the lit niches behind him",
    "house_majed_cap": "In the place",
    "house_link_majlis": "The Stone Block Majlis",
    "house_link_works": "Other works",
    "house_link_contact": "Get in touch",

    "contact_title": "Let\'s talk",
    "contact_lead": "I would be glad to hear from you about architectural projects, or about working together on waqf media and the work of Athar Foundation.",
    "f_name": "Your name",
    "f_name_ph": "Majed Abu Namous",
    "f_email": "Email",
    "f_email_ph": "info@majednamous.com",
    "f_subject": "Subject",
    "f_subjects": ["An architectural project",
                   "Working with Athar Foundation for Waqf Media",
                   "Media and documentation",
                   "Another enquiry"],
    "f_message": "Your message",
    "f_message_ph": "Tell me about the enquiry or the idea…",
    "f_submit": "Send message",
    "f_sending": "Sending…",
    "f_ok": "Thank you for reaching out. Your message came through.",
    "f_fail": "That could not be sent right now. You can email me directly at info@majednamous.com",
    "f_unconfigured": "This form is not connected to a server yet, so nothing is sent from here. Please email me directly at info@majednamous.com, or use the number below.",

    "footer_tag": "في عمارة البنيان، وتوثيق أثر الإنسان.",
    "footer_nav_title": "Links",
    "footer_contact_title": "Contact",
    "footer_rights": "All rights reserved.",
    "footer_name": "Majed Namous",
}

# ============================================================
# 3. Helpers
# ============================================================

# tightened viewBoxes so each mark fills its box (measured with getBBox)
VIEWBOX = {
    "logo.svg": "81 194 1084 611",
    "athar.svg": "48 86 671 541",
    "almajed-cottages.svg": "64 275 640 163",
}


def asset_ver(rel):
    """Short content hash, appended to css/js URLs so a rebuild never
    serves a stale file out of the browser cache."""
    try:
        with open(os.path.join(ROOT, rel), "rb") as f:
            return hashlib.md5(f.read()).hexdigest()[:8]
    except OSError:
        return "0"


def svg(name, optional=False):
    """Inline an SVG: strip the prolog, tighten the viewBox, allow recolouring.

    With optional=True a missing file returns "" instead of raising, so a
    mark can be dropped into assets/svg later and picked up on rebuild.
    """
    path = os.path.join(ROOT, "assets", "svg", name)
    if optional and not os.path.exists(path):
        print("   (note: assets/svg/%s not found — its mark is skipped)" % name)
        return ""
    with open(path, encoding="utf-8") as f:
        s = f.read()
    s = re.sub(r"<\?xml.*?\?>", "", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    if name in VIEWBOX:
        s = re.sub(r'viewBox="[^"]*"', 'viewBox="%s"' % VIEWBOX[name], s, count=1)
    s = s.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)
    return s.strip()


LOGO = svg("logo.svg")
LOGO_FOOTER = svg("logo-footer.svg")
ATHAR_MARK = svg("athar.svg")

PLAY_ICON = ('<svg class="play-glyph" viewBox="0 0 24 24" aria-hidden="true" '
             'focusable="false"><path d="M8.6 5.2 18.2 12 8.6 18.8Z"/></svg>')
COTTAGES_MARK = svg("almajed-cottages.svg", optional=True)

ARROW = ('<svg class="arrow" viewBox="0 0 12 12" fill="none" aria-hidden="true" '
         'focusable="false"><path d="M2.5 9.5 9.5 2.5M4 2.5h5.5V8" '
         'stroke="currentColor" stroke-width="1.1" stroke-linecap="square"/></svg>')


CARET = ('<svg viewBox="0 0 10 10" fill="none" aria-hidden="true" focusable="false">'
         '<path d="M2 3.6 5 6.6 8 3.6" stroke="currentColor" stroke-width="1.1"/></svg>')


def picture(base, alt, widths, sizes, loading="lazy", fetchpriority=None,
            w=None, h=None):
    big = widths[0]
    srcset = ", ".join("%s/%s-%d.webp %dw" % (A, base, n, n) for n in widths)
    attrs = 'loading="%s" decoding="async"' % loading
    if fetchpriority:
        attrs += ' fetchpriority="%s"' % fetchpriority
    if w and h:
        attrs += ' width="%d" height="%d"' % (w, h)
    return ('<picture>'
            '<source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            '<img src="{a}/{base}-{big}.jpg" alt="{alt}" {attrs}>'
            '</picture>').format(srcset=srcset, sizes=sizes, a=A, base=base,
                                 big=big, alt=alt, attrs=attrs)


def lead_pic(base, alt, sizes):
    widths, w, h = LEAD_IMG[base]
    return picture(base, alt, widths, sizes, w=w, h=h)


def words(text):
    """Wrap each word so the hero name can stagger in."""
    return " ".join('<span class="w">%s</span>' % w for w in text.split(" "))


# ============================================================
# 4. Partials
# ============================================================


PATHS = {
    "home": ("index.html", "en/index.html"),
    "contact": ("contact.html", "en/contact.html"),
    "aqsa": ("aqsa.html", "en/aqsa.html"),
    "monolith": ("monolith.html", "en/monolith.html"),
    "emirati": ("emirati.html", "en/emirati.html"),
}


def head(t, *, page, title, desc, canonical, theme="", css=None,
         theme_color="#d4d4d4", og_image="work-2016-1000.jpg", preload="",
         preload_display=True):
    """theme / css / theme_color / og_image / preload let one page carry
    its own art direction (see monolith()) without touching the others:
    with the defaults the output is byte-identical to before."""
    if page == "home":
        preload = ('\n  <link rel="preload" as="image" type="image/webp" '
                   'href="%s/work-2016-400.webp" fetchpriority="high">' % A)
    body_font = "%s/fonts/thmanyah-light.woff" % ASSETS
    display_font = "%s/fonts/majed-arabic.woff" % ASSETS
    preload_fonts = ('<link rel="preload" as="font" type="font/woff" href="%s" '
                     'crossorigin>' % body_font)
    if t["lang"] == "ar" and preload_display:
        preload_fonts += ('\n  <link rel="preload" as="font" type="font/woff" '
                          'href="%s" crossorigin>' % display_font)
    return """<!DOCTYPE html>
<html lang="{lang}" dir="{dir}" class="no-js{theme}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="ar" href="{base}/{ar_path}">
  <link rel="alternate" hreflang="en" href="{base}/{en_path}">
  <link rel="alternate" hreflang="x-default" href="{base}/{ar_path}">
  <meta name="theme-color" content="{theme_color}">
  <link rel="icon" href="{root}favicon.ico" sizes="32x32">
  <link rel="icon" href="{a}/favicon-512.png" type="image/png" sizes="512x512">
  <link rel="apple-touch-icon" href="{a}/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{ogsite}">
  <meta property="og:locale" content="{oglocale}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{base}/assets/img/{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  {preload_fonts}{preload}
  <link rel="stylesheet" href="{assets}/css/site.css?v={cssv}">{extra_css}
</head>
<body>
<a class="skip" href="#main">{skip}</a>
""".format(lang=t["lang"], dir=t["dir"], title=title, desc=desc, canonical=canonical,
           base=BASE_URL,
           ar_path=PATHS[page][0], en_path=PATHS[page][1],
           root=ROOTREL, a=A, assets=ASSETS, preload_fonts=preload_fonts,
           preload=preload,
           ogsite=SITE["site_name"],
           oglocale=("ar_JO" if t["lang"] == "ar" else "en_US"),
           cssv=asset_ver("assets/css/site.css"),
           theme=(" " + theme if theme else ""), theme_color=theme_color,
           og_image=og_image,
           extra_css=('\n  <link rel="stylesheet" href="%s/css/%s?v=%s">'
                      % (ASSETS, css, asset_ver("assets/css/" + css))
                      if css else ""),
           skip=t["skip"])


def navbar(t, page, alt_href):
    def cur(href):
        return ' aria-current="page"' if href == page + ".html" else ""

    def links(cls):
        """cls is "nav__link" for the bar and "" for the mobile menu."""
        out = []
        for item in t["nav"]:
            href, label = item[0], item[1]
            kids = item[2] if len(item) > 2 else []
            h = href
            if page != "home" and href.startswith("#"):
                h = t["home_href"] + href
            if not kids:
                out.append('<li><a class="%s" href="%s"%s>%s</a></li>'
                           % (cls, h, cur(href), label))
                continue
            sub = "".join('<li><a href="%s"%s>%s</a></li>' % (k, cur(k), kl)
                          for k, kl in kids)
            if cls:
                active = " is-current" if any(cur(k) for k, _ in kids) else ""
                out.append(
                    '<li class="nav__item--sub" data-sub>'
                    '<a class="{cls}{active}" href="{h}">{label}</a>'
                    '<button class="nav__caret" type="button" data-sub-toggle '
                    'aria-expanded="false" aria-controls="nav-sub" aria-label="{sl}">'
                    '{caret}</button>'
                    '<ul class="nav__sub" id="nav-sub">{sub}</ul></li>'.format(
                        cls=cls, active=active, h=h, label=label,
                        sl=t["nav_sub_label"], caret=CARET, sub=sub))
            else:
                out.append('<li><a href="%s">%s</a>'
                           '<ul class="nav__menu-sub">%s</ul></li>' % (h, label, sub))
        return "\n        ".join(out)

    lang_block = ('<div class="lang">'
                  '<span aria-current="true">{self}</span>'
                  '<span class="lang__sep" aria-hidden="true">/</span>'
                  '<a href="{alt}" lang="{other}" hreflang="{other}">{other_label}</a>'
                  '</div>').format(self=t["self_label"], alt=alt_href,
                                   other=t["other"], other_label=t["other_label"])

    return """<header class="nav" data-nav>
  <div class="nav__bar">
    <a class="nav__logo" href="{home}" aria-label="{name}">{logo}</a>
    <nav class="nav__links" aria-label="{navlabel}">
      <ul>
        {links}
      </ul>
    </nav>
    <div class="nav__end">
      {lang}
      <button class="nav__toggle" type="button" data-nav-toggle
              aria-expanded="false" aria-controls="nav-menu" aria-label="{menu}">
        <span></span><span></span>
      </button>
    </div>
  </div>
  <div class="nav__menu" id="nav-menu" data-nav-menu aria-hidden="true">
    <div class="nav__menu-inner">
      <ul>
        {mlinks}
      </ul>
    </div>
  </div>
</header>
""".format(home=t["home_href"], name=t["footer_name"], logo=LOGO,
           navlabel=("التنقّل" if t["lang"] == "ar" else "Primary"),
           links=links("nav__link"), lang=lang_block, menu=t["menu_open"],
           mlinks=links(""))


def footer(t):
    flat = []
    for item in t["nav"][1:]:
        flat.append((item[0], item[1]))
        flat.extend(item[2] if len(item) > 2 else [])
    nav_items = "\n          ".join(
        '<li><a href="%s">%s</a></li>' % (
            (t["home_href"] + h) if h.startswith("#") else h, label)
        for h, label in flat)
    return """<footer class="footer">
  <div class="wrap">
    <div class="footer__top">
      <div>
        <a class="footer__logo" href="{home}" aria-label="{name}">{logo}</a>
        <p class="footer__tag">{tag}</p>
      </div>
      <div class="footer__col">
        <h2>{navtitle}</h2>
        <ul>
          {nav}
        </ul>
      </div>
      <div class="footer__col">
        <h2>{contacttitle}</h2>
        <ul>
          <li><a class="footer__value" href="mailto:{email}">{email}</a></li>
          <li><a class="footer__value" href="tel:{phone}">{phone_display}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© <span data-year>{year}</span> {name}. {rights}</span>
    </div>
  </div>
</footer>
<script src="{assets}/js/site.js?v={jsv}" defer></script>
</body>
</html>
""".format(home=t["home_href"], name=t["footer_name"], logo=LOGO_FOOTER,
           tag=t["footer_tag"], navtitle=t["footer_nav_title"], nav=nav_items,
           contacttitle=t["footer_contact_title"], email=SITE["email"],
           phone=SITE["phone"], phone_display=SITE["phone_display"],
           year=YEAR, rights=t["footer_rights"], assets=ASSETS,
           jsv=asset_ver("assets/js/site.js"))


# ============================================================
# 5. Pages
# ============================================================


def hero_field():
    """Two drifting rows of work thumbnails — the hero's mosaic horizon.

    Each row prints the same 8-tile set six times and the CSS loops by
    -16.6667%, i.e. exactly one set, leaving five spare copies. The band
    can never run out at any viewport ratio, and the field is forced to
    LTR flow in CSS so RTL cannot reverse the loop.
    """
    rows = []
    for i, items in enumerate(HERO_ROWS):
        one = "".join(
            '<span class="hero__tile"><img src="{a}/{img}-400.webp" alt="" '
            'loading="eager" decoding="async" width="400" height="400"></span>'.format(
                a=A, img=img)
            for img in items)
        rows.append('<div class="hero__row hero__row--{c}">{s}{s}{s}{s}{s}{s}</div>'.format(
            c="ab"[i], s=one))
    return '<div class="hero__field" aria-hidden="true">%s</div>' % "".join(rows)


def home(t, alt_href):
    tiles = []
    for w in WORKS:
        alt = w["alt_ar"] if t["lang"] == "ar" else w["alt_en"]
        tiles.append("""<figure class="tile">
          <span class="tile__frame">{pic}</span>
          <figcaption class="tile__year">{year}</figcaption>
        </figure>""".format(
            pic=picture(w["img"], alt, [1000, 640, 400],
                        "(min-width: 1000px) 42vw, (min-width: 720px) 46vw, 46vw",
                        w=1000, h=1000),
            year=w["year"]))

    bio = "\n        ".join("<p>%s</p>" % p for p in t["about_body"])
    athar_paras = "\n        ".join("<p>%s</p>" % p for p in t["athar_body"])
    film_paras = "\n        ".join("<p>%s</p>" % p for p in t["film_body"])
    cottages_paras = "\n        ".join("<p>%s</p>" % p for p in t["cottages_body"])
    media_story = "\n        ".join("<p>%s</p>" % p for p in t["media_story"])

    return head(t, page="home", title=SITE["site_name"], desc=SITE["tagline"],
                canonical=BASE_URL + "/" + ("" if t["lang"] == "ar" else "en/")) \
        + navbar(t, "home", alt_href) + """
<main id="main">

  <!-- Hero -->
  <section class="hero ambient" id="top" data-hero>
    <div class="hero__content">
      <div class="wrap">
        <p class="meta hero__eyebrow">{greet}</p>
        <h1 class="hero__name">{name}</h1>
        <p class="lead">{lead}</p>
      </div>
    </div>
    <div class="hero__strip">
      {field}
    </div>
  </section>

  <!-- Intro: biography + portrait -->
  <section class="section intro ambient ambient--soft" id="about" aria-labelledby="about-title">
    <div class="wrap">
      <h2 class="meta reveal" id="about-title">{about_meta}</h2>
      <div class="intro__grid">
        <div class="intro__body">
          <div class="prose reveal">
        {bio}
          </div>
        </div>
        <div class="intro__portrait img-reveal">{portrait}</div>
      </div>
    </div>
  </section>

  <!-- Works mosaic -->
  <section class="section works" id="works" aria-labelledby="works-title">
    <div class="wrap">
      <div class="section-head reveal">
        <h2 class="section-title" id="works-title">{works_title}</h2>
      </div>
      <div class="works__lead">
        <a class="lead-shot lead-shot--wide img-reveal" href="emirati.html">
          <span class="lead-shot__frame">{lead_facade}</span>
          <span class="lead-shot__cap"><span class="lead-shot__title">{lead_title}</span><span class="tile__year" dir="ltr">2026</span>{arrow}</span>
        </a>
        <figure class="lead-shot lead-shot--tall img-reveal" data-delay="1">
          <span class="lead-shot__frame">{lead_majed}</span>
          <figcaption class="tile__year">{lead_majed_cap}</figcaption>
        </figure>
      </div>
      <div class="mosaic" data-mosaic>
        {tiles}
      </div>
    </div>
  </section>

  <!-- Athar -->
  <section class="section athar" id="athar" aria-labelledby="athar-title">
    <div class="wrap">
      <div class="athar__grid">
        <div class="athar__mark reveal" role="img" aria-label="{athar_logo_alt}">{athar_mark}</div>
        <div class="athar__body">
          <h2 class="athar__title reveal" id="athar-title">{athar_title}</h2>
          <div class="prose athar__story reveal" data-delay="1">
        {athar_paras}
          </div>

          <!-- a documented moment: the film, screened in Madinah -->
          <figure class="film">
            <div class="film__stage reveal" data-film>
              <video class="film__video" data-film-video
                     poster="{film_poster}" preload="none" playsinline controls
                     width="480" height="608" aria-label="{film_alt}">
                <source src="{film_src}" type="video/mp4">
              </video>
              <button class="film__play" type="button" data-film-play>
                <span class="film__play-mark" aria-hidden="true">{play_icon}</span>
                <span class="film__play-label">{film_play}</span>
              </button>
            </div>
            <figcaption class="film__body reveal" data-delay="1">
              <p class="meta">{film_meta}</p>
              <h3 class="film__title">{film_title}</h3>
              <div class="prose film__note">
            {film_paras}
              </div>
            </figcaption>
          </figure>

          <p class="athar__visit reveal" data-delay="2">
            <a class="btn" href="{athar_url}" target="_blank" rel="noopener">
              <span>{athar_cta}</span>{arrow}
            </a>
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Al Majed Cottages -->
  <section class="section cottages" id="cottages" aria-labelledby="cottages-title">
    <div class="wrap">
      <div class="athar__grid">
        <div class="athar__mark athar__mark--wide reveal" role="img" aria-label="{cottages_logo_alt}">{cottages_mark}</div>
        <div class="athar__body">
          <h2 class="athar__title reveal" id="cottages-title">{cottages_title}</h2>
          <div class="prose athar__story reveal" data-delay="1">
        {cottages_paras}
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Al Jazeera -->
  <section class="section section--tight media" id="media" aria-labelledby="media-title">
    <div class="wrap">
      <div class="section-head reveal">
        <h2 class="section-title" id="media-title">{media_title}</h2>
        <p class="meta">{media_meta}</p>
      </div>
      <a class="media__link img-reveal" href="{interview}" target="_blank" rel="noopener">
        <div class="media__frame">{cover}</div>
        <div class="media__caption">
          <span class="media__title">{media_headline}</span>
          <span class="meta media__note"><span>{media_note}</span>{arrow}</span>
        </div>
      </a>

      <div class="media__story">
        <figure class="media__story-figure img-reveal">{car}</figure>
        <div class="media__story-body reveal" data-delay="1">
          <div class="prose">
        {media_story}
          </div>
          <p class="media__more">
            <a class="link" href="aqsa.html"><span>{aqsa_cta}</span>{arrow}</a>
          </p>
        </div>
      </div>
    </div>
  </section>

</main>
""".format(
        field=hero_field(),
        greet=t["hero_greet"], name=words(t["hero_name"]), lead=t["hero_lead"],
        about_meta=t["about_meta"], bio=bio,
        portrait=picture("majed-portrait", t["about_portrait_alt"], [900, 600],
                         "(min-width: 880px) 40vw, 86vw"),
        works_title=t["works_title"],
        lead_facade=lead_pic("home-facade", t["lead_facade_alt"],
                             "(min-width: 1320px) 820px, (min-width: 880px) 62vw, 92vw"),
        lead_majed=lead_pic("home-majed", t["lead_majed_alt"],
                            "(min-width: 1320px) 300px, (min-width: 880px) 23vw, 70vw"),
        lead_majed_cap=t["lead_majed_cap"], lead_title=t["house_title"],
        tiles="\n        ".join(tiles),
        athar_mark=ATHAR_MARK, athar_logo_alt=t["athar_logo_alt"],
        athar_title=t["athar_title"],
        athar_paras=athar_paras,
        athar_url=SITE["athar_url"], athar_cta=t["athar_cta"], arrow=ARROW,
        film_poster="%s/athar-film-480.jpg" % A,
        film_src="%s/video/athar-madinah-film.mp4" % ASSETS,
        film_alt=t["film_alt"], play_icon=PLAY_ICON,
        film_play=t["film_play"], film_meta=t["film_meta"],
        film_title=t["film_title"], film_paras=film_paras,
        cottages_mark=COTTAGES_MARK, cottages_logo_alt=t["cottages_logo_alt"],
        cottages_title=t["cottages_title"],
        cottages_paras=cottages_paras,
        media_title=t["media_title"], media_meta=t["media_meta"],
        media_headline=t["media_headline"], media_note=t["media_note"],
        interview=SITE["interview_url"],
        cover=picture("aljazeera", t["media_alt"], [1600, 900],
                      "(min-width: 1320px) 1240px, 92vw", w=1600, h=900),
        media_story=media_story,
        car=picture("aqsa-car", t["media_story_alt"], [1200, 800],
                    "(min-width: 880px) 46vw, 92vw", w=1200, h=800),
        aqsa_cta=t["aqsa_cta"],
    ) + footer(t)


def contact(t, alt_href):
    options = "\n            ".join(
        '<option value="%s">%s</option>' % (o, o) for o in t["f_subjects"])

    return head(t, page="contact", title=SITE["site_name"], desc=SITE["tagline"],
                canonical=BASE_URL + "/" + ("contact.html" if t["lang"] == "ar"
                                            else "en/contact.html")) \
        + navbar(t, "contact", alt_href) + """
<main id="main">
  <section class="contact-hero section ambient">
    <div class="wrap">
      <div class="contact__grid">

        <div class="contact__intro">
          <h1 class="contact__title reveal">{title}</h1>
          <p class="lead reveal" data-delay="1">{lead}</p>
        </div>

        <form class="form reveal" data-delay="1" data-form
              data-endpoint="{endpoint}"
              data-msg-sending="{f_sending}"
              data-msg-ok="{f_ok}"
              data-msg-fail="{f_fail}"
              data-msg-unconfigured="{f_unconfigured}"
              method="post" action="{endpoint}">

          <div class="field">
            <label for="f-name">{f_name}</label>
            <input id="f-name" name="name" type="text" autocomplete="name"
                   placeholder="{f_name_ph}" required>
          </div>

          <div class="field">
            <label for="f-email">{f_email}</label>
            <input id="f-email" name="email" type="email" autocomplete="email"
                   placeholder="{f_email_ph}" required dir="ltr">
          </div>

          <div class="field field__select">
            <label for="f-subject">{f_subject}</label>
            <select id="f-subject" name="subject" required>
            {options}
            </select>
          </div>

          <div class="field">
            <label for="f-message">{f_message}</label>
            <textarea id="f-message" name="message" rows="6"
                      placeholder="{f_message_ph}" required></textarea>
          </div>

          <button class="form__submit" type="submit">{f_submit}</button>

          <p class="form__status" data-form-status role="status" aria-live="polite"></p>
        </form>

        <div class="contact__details reveal" data-delay="2">
          <a class="contact__detail" href="mailto:{email}">{email}</a>
          <a class="contact__detail" href="tel:{phone}">{phone_display}</a>
        </div>

      </div>
    </div>
  </section>
</main>
""".format(title=t["contact_title"], lead=t["contact_lead"],
           email=SITE["email"], phone=SITE["phone"],
           phone_display=SITE["phone_display"], endpoint=SITE["form_endpoint"],
           options=options,
           f_name=t["f_name"], f_name_ph=t["f_name_ph"],
           f_email=t["f_email"], f_email_ph=t["f_email_ph"],
           f_subject=t["f_subject"], f_message=t["f_message"],
           f_message_ph=t["f_message_ph"], f_submit=t["f_submit"],
           f_sending=t["f_sending"], f_ok=t["f_ok"], f_fail=t["f_fail"],
           f_unconfigured=t["f_unconfigured"]) + footer(t)


def shot(base, alt, sizes, cap="", cls="", delay=None, eager=False):
    """One photograph in the story: a zoomable frame, an optional caption."""
    widths, w, h = AQSA_IMG[base]
    pic = picture(base, alt, widths, sizes,
                  loading=("eager" if eager else "lazy"),
                  fetchpriority=("high" if eager else None), w=w, h=h)
    big = "%s/%s-%d.webp" % (A, base, widths[0])
    d = ' data-delay="%d"' % delay if delay else ""
    caption = ('<figcaption class="meta shot__cap">%s</figcaption>' % cap) if cap else ""
    return ('<figure class="shot {cls} img-reveal"{d}>'
            '<button class="shot__frame" type="button" data-shot '
            'data-shot-src="{big}" data-shot-alt="{alt}" aria-label="{zoom}">'
            '{pic}</button>{cap}</figure>').format(
                cls=cls, d=d, big=big, alt=alt, pic=pic, cap=caption,
                zoom=SHOT_ZOOM)


def aqsa(t, alt_href):
    global SHOT_ZOOM
    SHOT_ZOOM = t["aqsa_zoom"]

    def prose(key, delay=1):
        return ('<div class="prose story__prose reveal" data-delay="%d">%s</div>'
                % (delay, "".join("<p>%s</p>" % x for x in t[key])))

    FULL = "(min-width: 1320px) 1240px, 92vw"
    HALF = "(min-width: 880px) 46vw, 92vw"
    SPLIT = "(min-width: 880px) 52vw, 92vw"

    body = """
<main id="main">

  <section class="story-hero ambient" id="top">
    <div class="wrap">
      <p class="meta reveal story-hero__eyebrow">{eyebrow}</p>
      <h1 class="story-hero__title reveal" data-delay="1">{title}</h1>
      <p class="lead story-hero__sub reveal" data-delay="2">{sub}</p>
    </div>
    <div class="wrap story-hero__figure">{hero}</div>
  </section>

  <section class="section section--tight story ambient ambient--soft" aria-labelledby="ch1">
    <div class="wrap">
      <div class="section-head reveal">
        <h2 class="section-title" id="ch1">{h1}</h2>
        <p class="meta story__num" dir="ltr">01</p>
      </div>
      {p1}
    </div>
  </section>

  <section class="section section--tight story" aria-labelledby="ch2">
    <div class="wrap">
      <div class="section-head reveal">
        <h2 class="section-title" id="ch2">{h2}</h2>
        <p class="meta story__num" dir="ltr">02</p>
      </div>
      {p2}
      <div class="story__pair">{model_a}{model_b}</div>
      <div class="story__full">{chassis}</div>
    </div>
  </section>

  <section class="section section--tight story ambient ambient--soft" aria-labelledby="ch3">
    <div class="wrap">
      <div class="section-head reveal">
        <h2 class="section-title" id="ch3">{h3}</h2>
        <p class="meta story__num" dir="ltr">03</p>
      </div>
      <div class="story__split">
        {stone}
        {p3}
      </div>
      <div class="story__full">{car_body}</div>
    </div>
  </section>

  <section class="section section--tight story" aria-labelledby="ch4">
    <div class="wrap">
      <div class="section-head reveal">
        <h2 class="section-title" id="ch4">{h4}</h2>
        <p class="meta story__num" dir="ltr">04</p>
      </div>
      <div class="story__full story__full--lead">{drive}</div>
      {p4}
      <div class="story__pair">{dome}{court}</div>
      <div class="story__pair story__pair--uneven">{indoor}{night}</div>
    </div>
  </section>

  <section class="section section--tight story ambient ambient--soft" aria-labelledby="ch5">
    <div class="wrap">
      <div class="section-head reveal">
        <h2 class="section-title" id="ch5">{h5}</h2>
        <p class="meta story__num" dir="ltr">05</p>
      </div>
      {p5}
      <div class="story__pair story__pair--uneven">{people_b}{people_a}</div>
    </div>
  </section>

  <section class="section section--tight story-end">
    <div class="wrap">
      <p class="story-end__line reveal">{end}</p>
      <p class="story-end__links reveal" data-delay="1">
        <a class="link" href="{interview}" target="_blank" rel="noopener"><span>{link_media}</span>{arrow}</a>
        <a class="link" href="{contact_href}"><span>{link_contact}</span>{arrow}</a>
      </p>
    </div>
  </section>

</main>

<div class="lightbox" data-lightbox hidden>
  <div class="lightbox__backdrop" data-lightbox-close></div>
  <figure class="lightbox__stage"><img alt="" data-lightbox-img></figure>
  <button class="lightbox__close" type="button" data-lightbox-close aria-label="{close}">
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false">
      <path d="M4 4l12 12M16 4L4 16" stroke="currentColor" stroke-width="1.2"/>
    </svg>
  </button>
  <button class="lightbox__nav lightbox__nav--prev" type="button" data-lightbox-prev aria-label="{prev}">
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false">
      <path d="M12.5 3.5L5.5 10l7 6.5" stroke="currentColor" stroke-width="1.2"/>
    </svg>
  </button>
  <button class="lightbox__nav lightbox__nav--next" type="button" data-lightbox-next aria-label="{next}">
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false">
      <path d="M7.5 3.5l7 6.5-7 6.5" stroke="currentColor" stroke-width="1.2"/>
    </svg>
  </button>
</div>
""".format(
        eyebrow=t["aqsa_eyebrow"], title=t["aqsa_title"], sub=t["aqsa_sub"],
        hero=shot("aqsa-drive", t["aqsa_hero_alt"], FULL,
                  cls="shot--hero", eager=True),
        h1=t["aqsa_h1"], p1=prose("aqsa_p1"),
        h2=t["aqsa_h2"], p2=prose("aqsa_p2"),
        model_a=shot("aqsa-model-a", t["aqsa_alt_model_a"], HALF,
                     cap=t["aqsa_cap_model"], cls="shot--wide"),
        model_b=shot("aqsa-model-b", t["aqsa_alt_model_b"], HALF,
                     cls="shot--wide", delay=1),
        chassis=shot("aqsa-chassis", t["aqsa_alt_chassis"], FULL,
                     cap=t["aqsa_cap_chassis"], cls="shot--wide"),
        h3=t["aqsa_h3"], p3=prose("aqsa_p3"),
        stone=shot("aqsa-stone", t["aqsa_alt_stone"], SPLIT,
                   cap=t["aqsa_cap_stone"], cls="shot--wide"),
        car_body=shot("aqsa-body", t["aqsa_alt_body"], FULL,
                      cap=t["aqsa_cap_body"], cls="shot--classic"),
        h4=t["aqsa_h4"], p4=prose("aqsa_p4"),
        drive=shot("aqsa-drive", t["aqsa_alt_drive"], FULL, cls="shot--classic"),
        dome=shot("aqsa-dome", t["aqsa_alt_dome"], HALF, cls="shot--classic"),
        court=shot("aqsa-court", t["aqsa_alt_court"], HALF,
                   cls="shot--classic", delay=1),
        indoor=shot("aqsa-indoor", t["aqsa_alt_indoor"], HALF, cls="shot--wide"),
        night=shot("aqsa-night", t["aqsa_alt_night"], HALF,
                   cap=t["aqsa_cap_night"], cls="shot--wide", delay=1),
        h5=t["aqsa_h5"], p5=prose("aqsa_p5"),
        people_b=shot("aqsa-people-b", t["aqsa_alt_people_b"], HALF, cls="shot--wide"),
        people_a=shot("aqsa-people-a", t["aqsa_alt_people_a"], HALF,
                      cls="shot--wide", delay=1),
        end=t["aqsa_end"], interview=SITE["interview_url"],
        link_media=t["aqsa_link_media"], link_contact=t["aqsa_link_contact"],
        contact_href=t["contact_href"], arrow=ARROW,
        close=t["aqsa_close"], prev=t["aqsa_prev"], next=t["aqsa_next"],
    )

    return head(t, page="aqsa", title=t["aqsa_page_title"], desc=t["aqsa_desc"],
                canonical=BASE_URL + "/" + ("aqsa.html" if t["lang"] == "ar"
                                            else "en/aqsa.html")) \
        + navbar(t, "aqsa", alt_href) + body + footer(t)


def mono_pic(base, alt, sizes, eager=False):
    widths, w, h = MONO_IMG[base]
    return picture(base, alt, widths, sizes,
                   loading=("eager" if eager else "lazy"), w=w, h=h)


def monolith(t, alt_href):
    """The Stone Block Majlis — a project page with its own art
    direction. Same navbar and footer as every other page; the cream
    ground and the editorial grid come from assets/css/monolith.css,
    which only this page loads. Deliberately short: five brief
    chapters and a closing line."""

    def prose(key):
        return ('<div class="prose mono-prose reveal" data-delay="1">%s</div>'
                % "".join("<p>%s</p>" % x for x in t[key]))

    def chapter_head(n, key):
        return ('<header class="mono-ch__head reveal">'
                '<p class="mono-num" dir="ltr">%02d</p>'
                '<h2 class="mono-ch__title" id="m%d">%s</h2>'
                '</header>' % (n, n, t[key]))

    def figure(base, alt, sizes, cls=""):
        return ('<figure class="mono-plate mono-plate--{k} {cls} img-reveal">'
                '<div class="mono-plate__frame">{pic}</div></figure>').format(
                    k=base.replace("mono-", ""), cls=cls,
                    pic=mono_pic(base, alt, sizes))

    def plate(base, sizes, delay=None):
        label, alt = t["mono_plates"][base]
        d = ' data-delay="%d"' % delay if delay else ""
        return ('<figure class="mono-plate mono-plate--{k} img-reveal"{d}>'
                '<div class="mono-plate__frame">{pic}</div>'
                '<figcaption class="mono-plate__cap">{label}</figcaption>'
                '</figure>').format(
                    k=base.replace("mono-", ""), d=d,
                    pic=mono_pic(base, alt, sizes), label=label)

    hw, hh = MONO_IMG["mono-hero"][1:]
    mw, mh = MONO_IMG["mono-hero-m"][1:]
    hero_srcset = ", ".join("%s/mono-hero-%d.webp %dw" % (A, n, n)
                            for n in MONO_IMG["mono-hero"][0])
    hero_pic = (
        '<picture>'
        '<source media="(max-width: 699px)" type="image/webp" '
        'srcset="{a}/mono-hero-m-{mw}.webp" width="{mw}" height="{mh}">'
        '<source type="image/webp" sizes="100vw" srcset="{srcset}">'
        '<img src="{a}/mono-hero-{hw}.jpg" alt="{alt}" width="{hw}" height="{hh}" '
        'loading="eager" decoding="async" fetchpriority="high">'
        '</picture>').format(
            a=A, mw=mw, mh=mh, hw=hw, hh=hh, alt=t["mono_hero_alt"],
            srcset=hero_srcset)

    latin_alt = t["mono_title_alt_lang"] == "en"
    title_alt = ('<p class="mono-hero__alt {cls} reveal" data-delay="1" lang="{l}" dir="{d}">{x}</p>'
                 .format(cls=("mono-latin" if latin_alt else ""),
                         l=t["mono_title_alt_lang"],
                         d=("ltr" if latin_alt else "rtl"), x=t["mono_title_alt"]))

    info = "".join(
        '<div class="mono-info__row"><dt>%s</dt><dd>%s</dd></div>' % kv
        for kv in t["mono_info"])

    court_label, court_alt = t["mono_court"]
    court = ('<figure class="mono-plate mono-plate--court img-reveal">'
             '<div class="mono-plate__frame">{pic}</div>'
             '<figcaption class="mono-plate__cap">{label}</figcaption>'
             '</figure>').format(
                 pic=mono_pic("mono-court", court_alt, "(min-width: 1320px) 1240px, 92vw"),
                 label=court_label)

    THIRD = "(min-width: 1320px) 400px, (min-width: 820px) 30vw, 78vw"
    INSET = "(min-width: 900px) 400px, 78vw"

    body = """
<main id="main" class="mono">

  <section class="mono-hero" id="top" aria-labelledby="mono-title">
    <figure class="mono-hero__media">{hero_pic}</figure>
    <div class="wrap mono-hero__head">
      <p class="mono-hero__eyebrow reveal"><span>{place}</span><span>{date}</span></p>
      <h1 class="mono-hero__title reveal" id="mono-title">{title}</h1>
      {title_alt}
    </div>
  </section>

  <section class="mono-open">
    <div class="wrap">
      <p class="mono-statement reveal">{open}</p>
    </div>
  </section>

  <section class="mono-ch" aria-labelledby="m1">
    <div class="wrap mono-ch__grid">
      {head1}
      <div class="mono-ch__body">{p1}</div>
    </div>
  </section>

  <section class="mono-ch" aria-labelledby="m2">
    <div class="wrap mono-ch__grid">
      {head2}
      <div class="mono-ch__body">{p2}{block}</div>
    </div>
  </section>

  <section class="mono-ch" aria-labelledby="m3">
    <div class="wrap mono-ch__grid">
      {head3}
      <div class="mono-ch__body">{p3}{sky}</div>
    </div>
    <div class="wrap">{court}</div>
  </section>

  <section class="mono-ch mono-ch--plates" aria-labelledby="m4">
    <div class="wrap mono-ch__grid">
      {head4}
      <div class="mono-ch__body">{p4}</div>
    </div>
    <div class="wrap">
      {above}
      <div class="mono-trio">{seat}{wall}{table}</div>
      {front}
    </div>
  </section>

  <section class="mono-film" aria-labelledby="mono-film-title">
    <div class="wrap">
      <header class="mono-film__head reveal">
        <h2 class="mono-ch__title" id="mono-film-title">{film_title}</h2>
        <p class="mono-film__note">{film_note}</p>
      </header>
      <div class="mono-film__stage film__stage reveal" data-film>
        <video class="film__video" data-film-video
               poster="{film_poster}" preload="none" playsinline controls
               width="1280" height="720" aria-label="{film_alt}">
          <source src="{film_src}" type="video/mp4">
        </video>
        <button class="film__play" type="button" data-film-play>
          <span class="film__play-mark" aria-hidden="true">{play_icon}</span>
          <span class="film__play-label">{film_play}</span>
        </button>
      </div>
    </div>
  </section>

  <section class="mono-ch" aria-labelledby="m5">
    <div class="wrap mono-ch__grid">
      {head5}
      <div class="mono-ch__body">
        <dl class="mono-info reveal" data-delay="1">{info}</dl>
      </div>
    </div>
  </section>

  <section class="mono-end">
    <div class="wrap">
      <p class="mono-end__line reveal"><span>{end_a}</span> <span>{end_b}</span></p>
      <div class="mono-sign reveal" data-delay="1">
        <span class="mono-sign__mark">{logo}</span>
        <p class="mono-sign__alt mono-latin" lang="en" dir="ltr">{sign}</p>
      </div>
      <p class="mono-end__links reveal" data-delay="2">
        <a class="link" href="emirati.html"><span>{link_house}</span>{arrow}</a>
        <a class="link" href="{works_href}"><span>{link_works}</span>{arrow}</a>
        <a class="link" href="{contact_href}"><span>{link_contact}</span>{arrow}</a>
      </p>
    </div>
  </section>

</main>
""".format(
        link_house=t["mono_link_house"],
        hero_pic=hero_pic, place=t["mono_place"], date=t["mono_date"],
        title=t["mono_title"], title_alt=title_alt, open=t["mono_open"],
        head1=chapter_head(1, "mono_h1"), p1=prose("mono_p1"),
        head2=chapter_head(2, "mono_h2"), p2=prose("mono_p2"),
        block=figure("mono-block", t["mono_block_alt"], INSET, "mono-ch__fig"),
        head3=chapter_head(3, "mono_h3"), p3=prose("mono_p3"),
        sky=figure("mono-sky", t["mono_sky_alt"], INSET, "mono-ch__fig mono-ch__fig--end"),
        head4=chapter_head(4, "mono_h4"), p4=prose("mono_p4"),
        above=plate("mono-above", "(min-width: 1320px) 1240px, 92vw"),
        seat=plate("mono-seat", THIRD),
        wall=plate("mono-wall", THIRD, delay=1),
        table=plate("mono-table", THIRD, delay=2),
        court=court,
        front=plate("mono-front", "(min-width: 1320px) 1240px, 92vw"),
        film_title=t["mono_film_title"],
        film_note=t["mono_film_note"], film_play=t["mono_film_play"],
        film_alt=t["mono_film_alt"], play_icon=PLAY_ICON,
        film_poster="%s/mono-film-1280.jpg" % A,
        film_src="%s/video/mono-film.mp4" % ASSETS,
        head5=chapter_head(5, "mono_h5"), info=info,
        end_a=t["mono_end"][0], end_b=t["mono_end"][1],
        # the mark already spells the Arabic name, so the signature adds
        # only the Latin one beneath it, never the same name twice
        logo=LOGO, sign=t["mono_sign_latin"],
        works_href=t["home_href"] + "#works", contact_href=t["contact_href"],
        link_works=t["mono_link_works"], link_contact=t["mono_link_contact"],
        arrow=ARROW,
    )

    preload = (
        '\n  <link rel="preload" as="image" type="image/webp" '
        'href="{a}/mono-hero-m-{mw}.webp" media="(max-width: 699px)" fetchpriority="high">'
        '\n  <link rel="preload" as="image" type="image/webp" '
        'imagesrcset="{srcset}" imagesizes="100vw" media="(min-width: 700px)" '
        'fetchpriority="high">').format(a=A, mw=mw, srcset=hero_srcset)

    return head(t, page="monolith", title=t["mono_page_title"], desc=t["mono_desc"],
                canonical=BASE_URL + "/" + ("monolith.html" if t["lang"] == "ar"
                                            else "en/monolith.html"),
                theme="theme-cream", css="monolith.css", theme_color="#f9f4ea",
                og_image="mono-hero-1600.jpg", preload=preload,
                preload_display=False) \
        + navbar(t, "monolith", alt_href) + body + footer(t)


def emirati(t, alt_href):
    """The Emirati House — a project page in the same family as the
    Stone Block Majlis (it reuses monolith.css), but on the site's own
    grey ground. Very little text: one line per chapter, photographs
    carry the rest. The Instagram reel stays a still until it is asked
    for, so Instagram's frame and script never load on their own."""

    def hpic(base, alt, sizes, eager=False):
        widths, w, h = HOUSE_IMG[base]
        return picture(base, alt, widths, sizes,
                       loading=("eager" if eager else "lazy"), w=w, h=h)

    def ratio(base):
        _, w, h = HOUSE_IMG[base]
        return {16 / 9: "r169", 4 / 3: "r43", 4 / 5: "r45"}.get(
            min((16 / 9, 4 / 3, 4 / 5), key=lambda r: abs(r - w / h)))

    WIDE = "(min-width: 1320px) 1240px, 92vw"
    HALF = "(min-width: 820px) 54vw, 86vw"
    NARROW = "(min-width: 820px) 30vw, 64vw"

    def plate(base, sizes, delay=None, wide=False):
        label, alt = t["house_plates"][base]
        r = ratio(base)
        d = ' data-delay="%d"' % delay if delay else ""
        cls = "house-wide" if wide else ("is-tall" if r == "r45" else "")
        return ('<figure class="mono-plate house-plate {cls} img-reveal"{d}>'
                '<div class="mono-plate__frame {r}">{pic}</div>'
                '<figcaption class="mono-plate__cap">{label}</figcaption>'
                '</figure>').format(cls=cls, d=d, r=r,
                                    pic=hpic(base, alt, sizes), label=label)

    def chapter(n, plates):
        title, line = t["house_ch"][n - 1]
        return """
  <section class="mono-ch mono-ch--plates" aria-labelledby="h{n}">
    <div class="wrap mono-ch__grid">
      <header class="mono-ch__head reveal">
        <p class="mono-num" dir="ltr">{nn:02d}</p>
        <h2 class="mono-ch__title" id="h{n}">{title}</h2>
      </header>
      <div class="mono-ch__body">
        <div class="prose mono-prose reveal" data-delay="1"><p>{line}</p></div>
      </div>
    </div>
    <div class="wrap">{plates}</div>
  </section>
""".format(n=n, nn=n, title=title, line=line, plates=plates)

    def row(kind, *items):
        return '<div class="house-row house-row--%s">%s</div>' % (kind, "".join(items))

    hw, hh = HOUSE_IMG["house-hero"][1:]
    mw, mh = HOUSE_IMG["house-hero-m"][1:]
    hero_srcset = ", ".join("%s/house-hero-%d.webp %dw" % (A, n, n)
                            for n in HOUSE_IMG["house-hero"][0])
    hero_pic = (
        '<picture>'
        '<source media="(max-width: 699px)" type="image/webp" '
        'srcset="{a}/house-hero-m-{mw}.webp" width="{mw}" height="{mh}">'
        '<source type="image/webp" sizes="100vw" srcset="{srcset}">'
        '<img src="{a}/house-hero-{hw}.jpg" alt="{alt}" width="{hw}" height="{hh}" '
        'loading="eager" decoding="async" fetchpriority="high">'
        '</picture>').format(a=A, mw=mw, mh=mh, hw=hw, hh=hh,
                             alt=t["house_hero_alt"], srcset=hero_srcset)

    latin_alt = t["lang"] == "ar"
    title_alt = ('<p class="mono-hero__alt {cls} reveal" data-delay="1" lang="{l}" dir="{d}">{x}</p>'
                 .format(cls=("mono-latin" if latin_alt else ""),
                         l=("en" if latin_alt else "ar"),
                         d=("ltr" if latin_alt else "rtl"), x=t["house_title_alt"]))

    info = "".join('<div class="mono-info__row"><dt>%s</dt><dd>%s</dd></div>' % kv
                   for kv in t["house_info"])

    chapters = "".join([
        chapter(1, plate("house-side", WIDE, wide=True)
                + row("pair-r", plate("house-arcade", NARROW),
                      plate("house-canopy", HALF, delay=1))),
        chapter(2, row("trio", plate("house-olive-arch", NARROW),
                       plate("house-gallery", NARROW, delay=1),
                       plate("house-corridor", NARROW, delay=2))
                + row("pair", plate("house-entrance", HALF),
                      plate("house-basin-arch", NARROW, delay=1))),
        chapter(3, plate("house-majlis", WIDE, wide=True)
                + row("pair", plate("house-majlis-b", HALF),
                      plate("house-carpet", NARROW, delay=1))),
        chapter(4, plate("house-olive", WIDE, wide=True)
                + row("trio", plate("house-above", NARROW),
                      plate("house-kitchen", NARROW, delay=1),
                      plate("house-pergola", NARROW, delay=2))
                + row("pair-r", plate("house-niches", NARROW),
                      plate("house-night", HALF, delay=1))),
    ])

    mw0, mh0 = MONO_IMG["mono-hero"][1:]
    majlis_link = """
  <section class="mono-ch mono-ch--plates" aria-labelledby="h5">
    <div class="wrap mono-ch__grid">
      <header class="mono-ch__head reveal">
        <p class="mono-num" dir="ltr">05</p>
        <h2 class="mono-ch__title" id="h5">{title}</h2>
      </header>
      <div class="mono-ch__body">
        <div class="prose mono-prose reveal" data-delay="1"><p>{line}</p></div>
      </div>
    </div>
    <div class="wrap">
      <a class="mono-plate house-wide house-link img-reveal" href="monolith.html">
        <span class="mono-plate__frame r169">{pic}</span>
        <span class="mono-plate__cap house-link__cap"><span>{title}</span>{arrow}</span>
      </a>
    </div>
  </section>
""".format(title=t["house_majlis_title"], line=t["house_majlis_line"], arrow=ARROW,
           pic=picture("mono-hero", t["house_majlis_alt"], MONO_IMG["mono-hero"][0],
                       WIDE, w=mw0, h=mh0))

    body = """
<main id="main" class="mono house">

  <section class="mono-hero" id="top" aria-labelledby="house-title">
    <figure class="mono-hero__media">{hero_pic}</figure>
    <div class="wrap mono-hero__head">
      <p class="mono-hero__eyebrow reveal"><span>{place}</span><span>{date}</span></p>
      <h1 class="mono-hero__title reveal" id="house-title">{title}</h1>
      {title_alt}
    </div>
  </section>

  <section class="mono-open">
    <div class="wrap">
      <p class="mono-statement reveal">{open}</p>
    </div>
  </section>
{chapters}{majlis_link}
  <section class="mono-film house-reel" aria-labelledby="house-reel-title">
    <div class="wrap house-reel__grid">
      <div class="house-reel__stage reveal" data-reel data-reel-src="{reel_embed}"
           data-reel-title="{reel_frame}">
        <button class="house-reel__cover" type="button" data-reel-play>
          {reel_pic}
          <span class="film__play-mark" aria-hidden="true">{play_icon}</span>
          <span class="film__play-label">{reel_play}</span>
        </button>
      </div>
      <header class="house-reel__body reveal" data-delay="1">
        <h2 class="mono-ch__title" id="house-reel-title">{reel_title}</h2>
        <p class="mono-film__note">{reel_note}</p>
        <p class="house-reel__open">
          <a class="link" href="{reel_url}" target="_blank" rel="noopener"><span>{reel_open}</span>{arrow}</a>
        </p>
      </header>
    </div>
  </section>

  <section class="mono-ch" aria-labelledby="h6">
    <div class="wrap mono-ch__grid">
      <header class="mono-ch__head reveal">
        <p class="mono-num" dir="ltr">06</p>
        <h2 class="mono-ch__title" id="h6">{h_info}</h2>
      </header>
      <div class="mono-ch__body">
        <dl class="mono-info reveal" data-delay="1">{info}</dl>
        <figure class="mono-plate house-majed mono-ch__fig mono-ch__fig--end img-reveal">
          <div class="mono-plate__frame r45">{majed}</div>
          <figcaption class="mono-plate__cap">{majed_cap}</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section class="mono-end">
    <div class="wrap">
      <div class="mono-sign reveal">
        <span class="mono-sign__mark">{logo}</span>
        <p class="mono-sign__alt mono-latin" lang="en" dir="ltr">Majed Namous</p>
      </div>
      <p class="mono-end__links reveal" data-delay="1">
        <a class="link" href="monolith.html"><span>{link_majlis}</span>{arrow}</a>
        <a class="link" href="{works_href}"><span>{link_works}</span>{arrow}</a>
        <a class="link" href="{contact_href}"><span>{link_contact}</span>{arrow}</a>
      </p>
    </div>
  </section>

</main>
""".format(
        hero_pic=hero_pic, place=t["house_place"], date=t["house_date"],
        title=t["house_title"], title_alt=title_alt, open=t["house_open"],
        chapters=chapters, majlis_link=majlis_link,
        reel_embed=HOUSE_REEL + "embed/", reel_url=HOUSE_REEL,
        reel_frame=t["house_reel_frame"],
        reel_pic=hpic("house-reel", t["house_reel_alt"], "(min-width: 820px) 400px, 78vw"),
        play_icon=PLAY_ICON, reel_play=t["house_reel_play"],
        reel_title=t["house_reel_title"], reel_note=t["house_reel_note"],
        reel_open=t["house_reel_open"],
        h_info=t["house_h_info"], info=info,
        majed=hpic("house-majed", t["house_majed_alt"], "(min-width: 900px) 400px, 78vw"),
        majed_cap=t["house_majed_cap"],
        logo=LOGO, link_majlis=t["house_link_majlis"],
        works_href=t["home_href"] + "#works", contact_href=t["contact_href"],
        link_works=t["house_link_works"], link_contact=t["house_link_contact"],
        arrow=ARROW,
    )

    preload = (
        '\n  <link rel="preload" as="image" type="image/webp" '
        'href="{a}/house-hero-m-{mw}.webp" media="(max-width: 699px)" fetchpriority="high">'
        '\n  <link rel="preload" as="image" type="image/webp" '
        'imagesrcset="{srcset}" imagesizes="100vw" media="(min-width: 700px)" '
        'fetchpriority="high">').format(a=A, mw=mw, srcset=hero_srcset)

    return head(t, page="emirati", title=t["house_page_title"], desc=t["house_desc"],
                canonical=BASE_URL + "/" + ("emirati.html" if t["lang"] == "ar"
                                            else "en/emirati.html"),
                theme="theme-house", css="monolith.css",
                og_image="house-hero-1600.jpg", preload=preload) \
        + navbar(t, "emirati", alt_href) + body + footer(t)


SHOT_ZOOM = ""


# ============================================================
# 6. Write
# ============================================================

def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("→", path, "%.1f KB" % (len(html.encode("utf-8")) / 1024))


if __name__ == "__main__":
    ROOTREL, ASSETS = "", "assets"
    A = "assets/img"
    write("index.html", home(AR, "en/index.html"))
    write("aqsa.html", aqsa(AR, "en/aqsa.html"))
    write("monolith.html", monolith(AR, "en/monolith.html"))
    write("emirati.html", emirati(AR, "en/emirati.html"))
    write("contact.html", contact(AR, "en/contact.html"))

    ROOTREL, ASSETS = "../", "../assets"
    A = "../assets/img"
    write("en/index.html", home(EN, "../index.html"))
    write("en/aqsa.html", aqsa(EN, "../aqsa.html"))
    write("en/monolith.html", monolith(EN, "../monolith.html"))
    write("en/emirati.html", emirati(EN, "../emirati.html"))
    write("en/contact.html", contact(EN, "../contact.html"))

    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % BASE_URL)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in ["", "emirati.html", "aqsa.html", "monolith.html", "contact.html",
              "en/", "en/emirati.html", "en/aqsa.html", "en/monolith.html", "en/contact.html"]:
        sm.append("  <url><loc>%s/%s</loc></url>" % (BASE_URL, u))
    sm.append("</urlset>\n")
    write("sitemap.xml", "\n".join(sm))
