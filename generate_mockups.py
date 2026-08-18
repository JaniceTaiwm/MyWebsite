#!/usr/bin/env python3
"""Generate personal website UI mockup PNGs with the specified color palette."""

from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
W, H = 1440, 900

# Color palette
COLORS = {
    "dark1": "#3A3238",       # Primary text - Charcoal Plum
    "light1": "#FAF7F5",      # Primary background - Warm Ivory
    "dark2": "#6E2C3A",       # Secondary text - Deep Maroon
    "light2": "#E5DAD2",      # Subtle background - Beige-Grey
    "accent1": "#C98FA0",     # Dusty Rose
    "accent2": "#8CA3B5",     # Dusty Blue
    "accent3": "#A99B8B",     # Warm Taupe
    "accent4": "#7C7A85",     # Cool Grey
    "accent5": "#B5495B",     # Bright Maroon - CTA
    "accent6": "#D9C7B8",     # Sand
    "link": "#6E8FA3",        # Muted Blue
    "visited": "#9C6B7A",     # Mauve
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb(name):
    return hex_to_rgb(COLORS[name])


def get_font(size, bold=False):
    paths = [
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf" if bold else "",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for p in paths:
        if p and os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_nav(draw, active_page=None):
    """Shared top navigation bar."""
    draw.rectangle([0, 0, W, 72], fill=rgb("light1"))
    draw.line([0, 72, W, 72], fill=rgb("light2"), width=2)

    font_logo = get_font(22, bold=True)
    font_nav = get_font(14)
    font_nav_active = get_font(14, bold=True)

    draw.text((48, 22), "Alex Chen", fill=rgb("dark2"), font=font_logo)

    pages = [
        ("Profile", "profile"),
        ("Hobbies", "hobbies"),
        ("Interests", "interests"),
        ("Experiences", "experiences"),
        ("Resume", "resume"),
        ("Contact", "contact"),
    ]
    x = 520
    for label, key in pages:
        is_active = key == active_page
        color = rgb("accent5") if is_active else rgb("dark1")
        font = font_nav_active if is_active else font_nav
        draw.text((x, 28), label, fill=color, font=font)
        if is_active:
            tw = draw.textlength(label, font=font)
            draw.line([x, 52, x + tw, 52], fill=rgb("accent5"), width=2)
        x += 130

    # CTA button
    rounded_rect(draw, [W - 180, 18, W - 48, 54], 8, fill=rgb("accent5"))
    draw.text((W - 148, 26), "Download CV", fill=rgb("light1"), font=get_font(13, bold=True))


def draw_footer(draw):
    draw.rectangle([0, H - 56, W, H], fill=rgb("dark2"))
    draw.text((48, H - 38), "© 2026 Alex Chen  ·  University Student Portfolio", fill=rgb("light2"), font=get_font(12))
    draw.text((W - 320, H - 38), "LinkedIn  ·  GitHub  ·  Email", fill=rgb("accent1"), font=get_font(12))


def save(img, name):
    path = os.path.join(OUTPUT_DIR, name)
    img.save(path, "PNG", optimize=True)
    print(f"Saved: {path}")


def mockup_inspiration_board():
    img = Image.new("RGB", (W, H), rgb("light1"))
    draw = ImageDraw.Draw(img)

    title_f = get_font(36, bold=True)
    sub_f = get_font(16)
    card_title = get_font(18, bold=True)
    body = get_font(13)
    small = get_font(11)

    draw.text((48, 40), "Design Inspiration & Color System", fill=rgb("dark2"), font=title_f)
    draw.text((48, 88), "Reference portfolios for university student biographies", fill=rgb("accent4"), font=sub_f)

    # Color swatches row
    swatch_y = 130
    palette = [
        ("Charcoal Plum", "dark1", "Primary text"),
        ("Warm Ivory", "light1", "Background"),
        ("Deep Maroon", "dark2", "Secondary"),
        ("Beige-Grey", "light2", "Subtle bg"),
        ("Dusty Rose", "accent1", "Accent 1"),
        ("Dusty Blue", "accent2", "Tech accent"),
        ("Warm Taupe", "accent3", "Beige accent"),
        ("Cool Grey", "accent4", "Neutral"),
        ("Bright Maroon", "accent5", "CTA / Pop"),
        ("Sand", "accent6", "Light neutral"),
        ("Muted Blue", "link", "Links"),
        ("Mauve", "visited", "Visited"),
    ]
    sx = 48
    for name, key, role in palette:
        rounded_rect(draw, [sx, swatch_y, sx + 96, swatch_y + 56], 6, fill=rgb(key), outline=rgb("accent4"), width=1)
        draw.text((sx, swatch_y + 62), name, fill=rgb("dark1"), font=small)
        draw.text((sx, swatch_y + 76), COLORS[key], fill=rgb("accent4"), font=small)
        draw.text((sx, swatch_y + 90), role, fill=rgb("accent3"), font=small)
        sx += 112

    # Reference cards
    refs = [
        ("brittanychiang.com", "Clean dev portfolio with timeline & projects",
         "Minimal nav, serif headings, muted palette, scroll sections"),
        ("leemunroe.com", "Designer biography with strong typography",
         "Hero intro, case study cards, personal voice"),
        ("jacekjeznach.com", "Interactive student-friendly portfolio",
         "Bold accent color, animated sections, skills grid"),
        ("rleonardi.github.io", "GitHub-style interactive resume",
         "Gamified experience timeline, playful but professional"),
        ("faculty.washington.edu/*", "Academic personal page pattern",
         "Research focus, publications list, contact sidebar"),
        ("about.me / linktree style", "Quick-link bio hub for students",
         "Single page, social links, short bio blurb"),
    ]

    card_y = 260
    col_w = 420
    for i, (site, tagline, notes) in enumerate(refs):
        col = i % 3
        row = i // 3
        x = 48 + col * (col_w + 24)
        y = card_y + row * 200
        rounded_rect(draw, [x, y, x + col_w, y + 180], 12, fill=rgb("light2"))
        rounded_rect(draw, [x + 16, y + 16, x + col_w - 16, y + 56], 6, fill=rgb("accent2"))
        draw.text((x + 24, y + 26), site, fill=rgb("light1"), font=card_title)
        draw.text((x + 24, y + 72), tagline, fill=rgb("dark2"), font=body)
        draw.text((x + 24, y + 98), notes, fill=rgb("dark1"), font=small)
        draw.text((x + 24, y + 148), "→ View reference", fill=rgb("link"), font=small)

    # Design direction callout
    rounded_rect(draw, [48, H - 120, W - 48, H - 48], 12, fill=rgb("dark2"))
    draw.text((72, H - 108), "Design Direction", fill=rgb("accent1"), font=get_font(16, bold=True))
    draw.text((72, H - 82),
              "Warm ivory base · Maroon & dusty rose accents · Academic yet approachable · Card-based sections · Clear 6-page nav",
              fill=rgb("light2"), font=body)

    save(img, "00-inspiration-board.png")


def mockup_site_structure():
    img = Image.new("RGB", (W, H), rgb("light1"))
    draw = ImageDraw.Draw(img)

    title_f = get_font(36, bold=True)
    sub_f = get_font(16)
    node_f = get_font(15, bold=True)
    desc_f = get_font(12)

    draw.text((48, 40), "Site Structure & Information Architecture", fill=rgb("dark2"), font=title_f)
    draw.text((48, 88), "Six-page personal website for a university student", fill=rgb("accent4"), font=sub_f)

    # Home hub
    cx, cy = W // 2, 200
    rounded_rect(draw, [cx - 100, cy - 30, cx + 100, cy + 30], 10, fill=rgb("accent5"))
    draw.text((cx - 72, cy - 10), "Global Nav", fill=rgb("light1"), font=node_f)

    pages = [
        ("Profile", "profile", 180, "Name, photo, university, major, year, short bio, quick facts"),
        ("Hobbies", "hobbies", 320, "Photography, hiking, cooking – cards with images & captions"),
        ("Interests", "interests", 460, "AI, sustainability, finance – tags & reading list"),
        ("Past Experiences", "experiences", 600, "Internships, clubs, volunteer – timeline layout"),
        ("Resume", "resume", 740, "PDF embed + structured sections: education, skills, work"),
        ("Contact Me", "contact", 880, "Form, email, social links, location placeholder"),
    ]

    for label, key, y, desc in pages:
        draw.line([cx, cy + 30, cx, y - 20], fill=rgb("accent3"), width=2)
        rounded_rect(draw, [120, y - 28, 420, y + 28], 10, fill=rgb("light2"))
        draw.text((140, y - 18), label, fill=rgb("dark2"), font=node_f)
        draw.text((140, y + 2), desc, fill=rgb("dark1"), font=desc_f)

        rounded_rect(draw, [480, y - 28, 900, y + 28], 8, fill=rgb("light1"), outline=rgb("accent2"), width=2)
        draw.text((500, y - 8), f"/{key}.html", fill=rgb("link"), font=desc_f)

    # Shared components box
    rounded_rect(draw, [960, 180, 1380, 520], 12, fill=rgb("dark2"))
    draw.text((990, 200), "Shared Components", fill=rgb("accent1"), font=get_font(18, bold=True))
    components = [
        "Header: logo + 6 nav links + CV button",
        "Footer: copyright + social icons",
        "Color tokens from palette (CSS variables)",
        "Typography: Georgia headings, system sans body",
        "Card component for hobbies & interests",
        "Timeline component for experiences",
        "Form fields for contact page",
        "Placeholder images: unsplash / avatar",
    ]
    yy = 240
    for c in components:
        draw.text((990, yy), "•  " + c, fill=rgb("light2"), font=desc_f)
        yy += 32

    # File tree
    rounded_rect(draw, [960, 560, 1380, 820], 12, fill=rgb("light2"))
    draw.text((990, 580), "Suggested File Tree", fill=rgb("dark2"), font=get_font(18, bold=True))
    tree = """MyWebsite/
├── index.html          (Profile)
├── hobbies.html
├── interests.html
├── experiences.html
├── resume.html
├── contact.html
├── css/styles.css
├── assets/avatar.jpg
└── assets/resume.pdf"""
    draw.text((990, 620), tree, fill=rgb("dark1"), font=get_font(12))

    save(img, "01-site-structure.png")


def mockup_profile():
    img = Image.new("RGB", (W, H), rgb("light1"))
    draw = ImageDraw.Draw(img)
    draw_nav(draw, "profile")

    # Hero section
    rounded_rect(draw, [48, 100, W - 48, 340], 16, fill=rgb("light2"))
    rounded_rect(draw, [80, 130, 280, 310], 12, fill=rgb("accent6"))
    draw.text((110, 200), "[Photo]", fill=rgb("accent4"), font=get_font(20))

    draw.text((320, 140), "Alex Chen", fill=rgb("dark2"), font=get_font(42, bold=True))
    draw.text((320, 195), "Computer Science · Year 3", fill=rgb("accent5"), font=get_font(20))
    draw.text((320, 230), "The University of Hong Kong", fill=rgb("accent2"), font=get_font(16))

    bio = "Passionate about building thoughtful software and exploring how\ntechnology intersects with finance and sustainability."
    draw.text((320, 270), bio, fill=rgb("dark1"), font=get_font(15))

    # Quick facts
    facts = [("📍  Hong Kong", 80), ("🎓  GPA: 3.8 / 4.0", 280), ("💼  Seeking Summer Internship", 500)]
    fx = 320
    for fact, _ in facts:
        rounded_rect(draw, [fx, 300, fx + 200, 330], 6, fill=rgb("light1"))
        draw.text((fx + 12, 308), fact, fill=rgb("dark1"), font=get_font(12))
        fx += 220

    # About section
    draw.text((48, 370), "About Me", fill=rgb("dark2"), font=get_font(24, bold=True))
    draw.line([48, 405, 200, 405], fill=rgb("accent1"), width=3)
    about = [
        "Hello! I'm a third-year CS student with a minor in Finance.",
        "I enjoy turning complex problems into elegant solutions.",
        "Currently exploring machine learning and full-stack development.",
    ]
    yy = 430
    for line in about:
        draw.text((48, yy), line, fill=rgb("dark1"), font=get_font(15))
        yy += 28

    # Stats cards
    stats = [("3", "Internships"), ("12", "Projects"), ("5", "Languages"), ("2", "Awards")]
    sx = 48
    for num, label in stats:
        rounded_rect(draw, [sx, 540, sx + 200, 640], 12, fill=rgb("light2"))
        draw.text((sx + 80, 560), num, fill=rgb("accent5"), font=get_font(36, bold=True))
        draw.text((sx + 60, 610), label, fill=rgb("dark1"), font=get_font(14))
        sx += 220

    draw_footer(draw)
    save(img, "02-profile.png")


def mockup_hobbies():
    img = Image.new("RGB", (W, H), rgb("light1"))
    draw = ImageDraw.Draw(img)
    draw_nav(draw, "hobbies")

    draw.text((48, 100), "Hobbies", fill=rgb("dark2"), font=get_font(36, bold=True))
    draw.text((48, 148), "What I do outside of lectures and labs", fill=rgb("accent4"), font=get_font(16))
    draw.line([48, 180, 160, 180], fill=rgb("accent1"), width=3)

    hobbies = [
        ("Photography", "Street & landscape · Canon EOS", "accent2"),
        ("Hiking", "Weekend trails · Lantau & Sai Kung", "accent3"),
        ("Cooking", "Asian fusion · meal prep enthusiast", "accent1"),
        ("Reading", "Sci-fi & biographies · 24 books/yr", "accent6"),
        ("Music", "Piano · indie playlists", "accent2"),
        ("Travel", "12 countries · culture & food", "accent3"),
    ]

    x, y = 48, 210
    for i, (title, desc, accent) in enumerate(hobbies):
        col = i % 3
        row = i // 3
        cx = 48 + col * 448
        cy = 210 + row * 280
        rounded_rect(draw, [cx, cy, cx + 420, cy + 250], 14, fill=rgb("light2"))
        rounded_rect(draw, [cx + 16, cy + 16, cx + 404, cy + 140], 10, fill=rgb(accent))
        draw.text((cx + 170, cy + 70), "[Image]", fill=rgb("light1"), font=get_font(16))
        draw.text((cx + 24, cy + 160), title, fill=rgb("dark2"), font=get_font(20, bold=True))
        draw.text((cx + 24, cy + 192), desc, fill=rgb("dark1"), font=get_font(13))
        draw.text((cx + 24, cy + 218), "Read more →", fill=rgb("link"), font=get_font(12))

    draw_footer(draw)
    save(img, "03-hobbies.png")


def mockup_interests():
    img = Image.new("RGB", (W, H), rgb("light1"))
    draw = ImageDraw.Draw(img)
    draw_nav(draw, "interests")

    draw.text((48, 100), "Interests", fill=rgb("dark2"), font=get_font(36, bold=True))
    draw.text((48, 148), "Topics I'm curious about and actively learning", fill=rgb("accent4"), font=get_font(16))

    tags = [
        "Machine Learning", "FinTech", "Sustainability", "Open Source",
        "UX Design", "Quantitative Finance", "Climate Tech", "Startups",
        "Data Visualization", "Ethical AI", "Product Management", "Blockchain",
    ]
    tx, ty = 48, 200
    for tag in tags:
        tw = len(tag) * 9 + 32
        rounded_rect(draw, [tx, ty, tx + tw, ty + 36], 18, fill=rgb("accent6"))
        draw.text((tx + 16, ty + 10), tag, fill=rgb("dark2"), font=get_font(13))
        tx += tw + 12
        if tx > 900:
            tx = 48
            ty += 48

    # Focus areas
    draw.text((48, 320), "Focus Areas", fill=rgb("dark2"), font=get_font(24, bold=True))
    areas = [
        ("AI & Software", "Building ML pipelines and web apps that solve real problems.", "accent2"),
        ("Finance & Markets", "Following equity research, portfolio theory, and macro trends.", "accent5"),
        ("Social Impact", "Volunteering and projects around education access.", "accent1"),
    ]
    ay = 370
    for title, desc, acc in areas:
        rounded_rect(draw, [48, ay, W - 48, ay + 100], 12, fill=rgb("light2"))
        rounded_rect(draw, [48, ay, 56, ay + 100], 4, fill=rgb(acc))
        draw.text((80, ay + 20), title, fill=rgb("dark2"), font=get_font(18, bold=True))
        draw.text((80, ay + 52), desc, fill=rgb("dark1"), font=get_font(14))
        ay += 120

    # Reading list
    draw.text((48, 640), "Currently Reading", fill=rgb("dark2"), font=get_font(20, bold=True))
    books = ["The Pragmatic Programmer", "Thinking, Fast and Slow", "Designing Data-Intensive Applications"]
    by = 680
    for b in books:
        draw.text((48, by), "📖  " + b, fill=rgb("link"), font=get_font(14))
        by += 28

    draw_footer(draw)
    save(img, "04-interests.png")


def mockup_experiences():
    img = Image.new("RGB", (W, H), rgb("light1"))
    draw = ImageDraw.Draw(img)
    draw_nav(draw, "experiences")

    draw.text((48, 100), "Past Experiences", fill=rgb("dark2"), font=get_font(36, bold=True))
    draw.text((48, 148), "Internships, leadership roles, and volunteer work", fill=rgb("accent4"), font=get_font(16))

    timeline_x = 120
    draw.line([timeline_x, 200, timeline_x, 780], fill=rgb("accent3"), width=3)

    experiences = [
        ("2025", "Software Engineering Intern", "TechCorp HK", "Built internal dashboard with React & Node.js"),
        ("2024", "Research Assistant", "HKU CS Dept", "NLP project on sentiment analysis for finance news"),
        ("2024", "President", "Finance & Investment Society", "Led 80-member club, organized 6 speaker events"),
        ("2023", "Volunteer Tutor", "Community Learning Center", "Taught Python basics to secondary students"),
        ("2023", "Hackathon Winner", "HKU Hackathon", "1st place – sustainability tracking mobile app"),
    ]

    ey = 210
    for year, role, org, desc in experiences:
        draw.ellipse([timeline_x - 8, ey + 8, timeline_x + 8, ey + 24], fill=rgb("accent5"))
        draw.text((timeline_x - 50, ey + 4), year, fill=rgb("accent4"), font=get_font(13, bold=True))
        rounded_rect(draw, [160, ey, W - 80, ey + 90], 10, fill=rgb("light2"))
        draw.text((180, ey + 14), role, fill=rgb("dark2"), font=get_font(17, bold=True))
        draw.text((180, ey + 40), org, fill=rgb("accent2"), font=get_font(14))
        draw.text((180, ey + 62), desc, fill=rgb("dark1"), font=get_font(13))
        ey += 110

    draw_footer(draw)
    save(img, "05-past-experiences.png")


def mockup_resume():
    img = Image.new("RGB", (W, H), rgb("light1"))
    draw = ImageDraw.Draw(img)
    draw_nav(draw, "resume")

    draw.text((48, 100), "Resume", fill=rgb("dark2"), font=get_font(36, bold=True))
    draw.text((48, 148), "Download or view inline", fill=rgb("accent4"), font=get_font(16))

    rounded_rect(draw, [W - 280, 100, W - 48, 140], 8, fill=rgb("accent5"))
    draw.text((W - 248, 110), "⬇  Download PDF", fill=rgb("light1"), font=get_font(14, bold=True))

    # Resume preview panel
    rounded_rect(draw, [48, 180, W - 48, H - 80], 12, fill=rgb("light2"), outline=rgb("accent4"), width=1)

    sections = [
        ("EDUCATION", [
            "The University of Hong Kong – BSc Computer Science (2023–2027)",
            "Minor in Finance · Dean's List 2024",
        ]),
        ("EXPERIENCE", [
            "Software Engineering Intern, TechCorp HK – Summer 2025",
            "Research Assistant, HKU – NLP & Finance – 2024",
        ]),
        ("SKILLS", [
            "Python · JavaScript · React · SQL · Git · Figma",
            "Languages: English (fluent), Cantonese (native), Mandarin (fluent)",
        ]),
        ("PROJECTS", [
            "Portfolio Tracker – full-stack app with real-time data",
            "Sustainability Dashboard – hackathon winning project",
        ]),
    ]

    ry = 210
    for heading, items in sections:
        draw.text((80, ry), heading, fill=rgb("accent5"), font=get_font(14, bold=True))
        draw.line([80, ry + 22, 300, ry + 22], fill=rgb("accent1"), width=2)
        ry += 36
        for item in items:
            draw.text((80, ry), "•  " + item, fill=rgb("dark1"), font=get_font(13))
            ry += 26
        ry += 16

    # Sidebar note
    rounded_rect(draw, [960, 210, 1340, 400], 10, fill=rgb("dark2"))
    draw.text((990, 230), "Resume Page Features", fill=rgb("accent1"), font=get_font(16, bold=True))
    features = [
        "Embedded PDF viewer",
        "One-click download button",
        "Structured HTML fallback",
        "Print-friendly stylesheet",
        "Last updated: Aug 2026",
    ]
    fy = 270
    for f in features:
        draw.text((990, fy), "✓  " + f, fill=rgb("light2"), font=get_font(13))
        fy += 28

    draw_footer(draw)
    save(img, "06-resume.png")


def mockup_contact():
    img = Image.new("RGB", (W, H), rgb("light1"))
    draw = ImageDraw.Draw(img)
    draw_nav(draw, "contact")

    draw.text((48, 100), "Contact Me", fill=rgb("dark2"), font=get_font(36, bold=True))
    draw.text((48, 148), "Let's connect – I'd love to hear from you", fill=rgb("accent4"), font=get_font(16))

    # Contact form
    rounded_rect(draw, [48, 190, 680, H - 80], 14, fill=rgb("light2"))
    draw.text((80, 220), "Send a Message", fill=rgb("dark2"), font=get_font(22, bold=True))

    fields = ["Name", "Email", "Subject", "Message"]
    fy = 270
    for field in fields:
        draw.text((80, fy), field, fill=rgb("dark1"), font=get_font(13))
        h = 100 if field == "Message" else 40
        rounded_rect(draw, [80, fy + 22, 640, fy + 22 + h], 8, fill=rgb("light1"), outline=rgb("accent6"), width=1)
        if field == "Message":
            draw.text((96, fy + 40), "Your message here...", fill=rgb("accent4"), font=get_font(12))
        else:
            draw.text((96, fy + 32), f"Enter your {field.lower()}...", fill=rgb("accent4"), font=get_font(12))
        fy += 22 + h + 24

    rounded_rect(draw, [80, fy, 240, fy + 44], 8, fill=rgb("accent5"))
    draw.text((130, fy + 12), "Send Message", fill=rgb("light1"), font=get_font(14, bold=True))

    # Contact info sidebar
    rounded_rect(draw, [720, 190, W - 48, H - 80], 14, fill=rgb("dark2"))
    draw.text((760, 230), "Get in Touch", fill=rgb("accent1"), font=get_font(22, bold=True))

    contacts = [
        ("✉", "alex.chen@university.edu.hk", "link"),
        ("🔗", "linkedin.com/in/alexchen", "link"),
        ("💻", "github.com/alexchen", "link"),
        ("📍", "Hong Kong SAR", "light2"),
        ("📱", "+852 XXXX XXXX", "light2"),
    ]
    cy = 290
    for icon, text, color in contacts:
        draw.text((760, cy), icon, fill=rgb("accent6"), font=get_font(18))
        draw.text((800, cy + 2), text, fill=rgb(color), font=get_font(14))
        cy += 48

    draw.text((760, 560), "Availability", fill=rgb("accent1"), font=get_font(16, bold=True))
    draw.text((760, 590), "Open to internships & collaborations", fill=rgb("light2"), font=get_font(13))
    draw.text((760, 618), "Response time: within 48 hours", fill=rgb("accent4"), font=get_font(12))

    draw_footer(draw)
    save(img, "07-contact.png")


if __name__ == "__main__":
    mockup_inspiration_board()
    mockup_site_structure()
    mockup_profile()
    mockup_hobbies()
    mockup_interests()
    mockup_experiences()
    mockup_resume()
    mockup_contact()
    print("\nAll mockups generated successfully.")
