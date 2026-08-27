#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Majed Namous — static site generator.

Run:  python3 build.py
Out:  index.html, contact.html, en/index.html, en/contact.html,
      robots.txt, sitemap.xml

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
    
    
    "nav": [("#top", "الرئيسية"), ("#works", "الأعمال"), ("#about", "عن ماجد"),
            ("#athar", "أثر"), ("aqsa.html", "سيارة الأقصى"),
            ("contact.html", "تواصل")],
    "skip": "تخطّي إلى المحتوى",
    "menu_open": "فتح القائمة",
    "home_href": "index.html", "contact_href": "contact.html",

    "hero_greet": "حيّاكم الله في مساحتي",
    "hero_name": "ماجد ناموس",
    "hero_lead": "أعيش بين العمارة والإعلام الوقفي، أبحث عن الأثر الذي يتركه الإنسان في المكان، وعن الحكاية التي تستحق أن تُروى.",
    "hero_cue": "الأعمال في الأسفل",

    "works_title": "الأعمال",
    "works_meta": "<span dir=\"ltr\">2007 - 2018</span>",

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
        "في عام 2023، أنشأتُ أكواخ الماجد في شارع الأردن بمدينة عمّان، وتولّيت تصميمها وتنفيذها بنفسي، من الفكرة الأولى وحتى تفاصيلها الأخيرة.",
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
    
    
    "nav": [("#top", "Home"), ("#works", "Works"), ("#about", "About"),
            ("#athar", "Athar"), ("aqsa.html", "Al-Aqsa Car"),
            ("contact.html", "Contact")],
    "skip": "Skip to content",
    "menu_open": "Open menu",
    "home_href": "index.html", "contact_href": "contact.html",

    "hero_greet": "Welcome to my space",
    "hero_name": "Majed Namous",
    "hero_lead": "I live between architecture and waqf media, looking for the mark a person leaves on a place, and for the story worth telling.",
    "hero_cue": "Works below",

    "works_title": "Works",

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
        "In 2023 I built Al Majed Cottages on Jordan Street in Amman, designing them and carrying out the work myself, from the first idea through to the last detail.",
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
}


def head(t, *, page, title, desc, canonical):
    preload = ""
    if page == "home":
        preload = ('\n  <link rel="preload" as="image" type="image/webp" '
                   'href="%s/work-2016-400.webp" fetchpriority="high">' % A)
    body_font = "%s/fonts/thmanyah-light.woff" % ASSETS
    display_font = "%s/fonts/majed-arabic.woff" % ASSETS
    preload_fonts = ('<link rel="preload" as="font" type="font/woff" href="%s" '
                     'crossorigin>' % body_font)
    if t["lang"] == "ar":
        preload_fonts += ('\n  <link rel="preload" as="font" type="font/woff" '
                          'href="%s" crossorigin>' % display_font)
    return """<!DOCTYPE html>
<html lang="{lang}" dir="{dir}" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="ar" href="{base}/{ar_path}">
  <link rel="alternate" hreflang="en" href="{base}/{en_path}">
  <link rel="alternate" hreflang="x-default" href="{base}/{ar_path}">
  <meta name="theme-color" content="#d4d4d4">
  <link rel="icon" href="{root}favicon.ico" sizes="32x32">
  <link rel="icon" href="{a}/favicon-512.png" type="image/png" sizes="512x512">
  <link rel="apple-touch-icon" href="{a}/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{ogsite}">
  <meta property="og:locale" content="{oglocale}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{base}/assets/img/work-2016-1000.jpg">
  <meta name="twitter:card" content="summary_large_image">
  {preload_fonts}{preload}
  <link rel="stylesheet" href="{assets}/css/site.css?v={cssv}">
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
           skip=t["skip"])


def navbar(t, page, alt_href):
    def links(cls):
        out = []
        for href, label in t["nav"]:
            h = href
            if page != "home" and href.startswith("#"):
                h = t["home_href"] + href
            current = ' aria-current="page"' if href == page + ".html" else ""
            out.append('<li><a class="%s" href="%s"%s>%s</a></li>'
                       % (cls, h, current, label))
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
    nav_items = "\n          ".join(
        '<li><a href="%s">%s</a></li>' % (
            (t["home_href"] + h) if h.startswith("#") else h, label)
        for h, label in t["nav"][1:])
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
    n = len(WORKS)
    for i in range(2):
        items = [WORKS[(i * 4 + j) % n] for j in range(n)]
        one = "".join(
            '<span class="hero__tile"><img src="{a}/{img}-400.webp" alt="" '
            'loading="eager" decoding="async" width="400" height="400"></span>'.format(
                a=A, img=w["img"])
            for w in items)
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
    write("contact.html", contact(AR, "en/contact.html"))

    ROOTREL, ASSETS = "../", "../assets"
    A = "../assets/img"
    write("en/index.html", home(EN, "../index.html"))
    write("en/aqsa.html", aqsa(EN, "../aqsa.html"))
    write("en/contact.html", contact(EN, "../contact.html"))

    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % BASE_URL)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in ["", "aqsa.html", "contact.html",
              "en/", "en/aqsa.html", "en/contact.html"]:
        sm.append("  <url><loc>%s/%s</loc></url>" % (BASE_URL, u))
    sm.append("</urlset>\n")
    write("sitemap.xml", "\n".join(sm))
