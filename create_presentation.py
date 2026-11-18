from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE


# US-inspired palette
NAVY = RGBColor(11, 36, 92)
RED = RGBColor(179, 25, 66)
WHITE = RGBColor(255, 255, 255)
LIGHT_BG = RGBColor(245, 247, 252)
TEXT_DARK = RGBColor(25, 31, 46)


OUTPUT_FILE = Path(__file__).resolve().parent / "history_of_usa_ru.pptx"


def set_background(slide):
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = LIGHT_BG


def add_top_banner(slide, title_text):
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
    banner.fill.solid()
    banner.fill.fore_color.rgb = NAVY
    banner.line.fill.background()

    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.2), Inches(12.2), Inches(0.7))
    tf = title_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.LEFT
    run = p.runs[0]
    run.font.name = "Calibri"
    run.font.size = Pt(31)
    run.font.bold = True
    run.font.color.rgb = WHITE


def style_body_paragraph(paragraph, text):
    paragraph.text = text
    paragraph.level = 0
    paragraph.alignment = PP_ALIGN.LEFT
    paragraph.space_after = Pt(6)
    run = paragraph.runs[0]
    run.font.name = "Calibri"
    run.font.size = Pt(20)
    run.font.color.rgb = TEXT_DARK


def add_content_box(slide, bullet_points):
    body_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), Inches(1.45), Inches(8.7), Inches(5.5))
    body_shape.fill.solid()
    body_shape.fill.fore_color.rgb = WHITE
    body_shape.line.color.rgb = RGBColor(210, 219, 238)

    text_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(8.2), Inches(5.1))
    tf = text_box.text_frame
    tf.word_wrap = True
    tf.clear()

    first = tf.paragraphs[0]
    style_body_paragraph(first, f"• {bullet_points[0]}")

    for point in bullet_points[1:]:
        p = tf.add_paragraph()
        style_body_paragraph(p, f"• {point}")


def add_flag_motif(slide):
    x = Inches(10.0)
    y = Inches(1.7)
    w = Inches(2.7)
    h = Inches(1.7)

    stripe_h = h / 6
    for i in range(6):
        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y + stripe_h * i, w, stripe_h)
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = RED if i % 2 == 0 else WHITE
        stripe.line.fill.background()

    canton = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w * 0.45, h * 0.55)
    canton.fill.solid()
    canton.fill.fore_color.rgb = NAVY
    canton.line.fill.background()

    star_rows = 3
    star_cols = 4
    step_x = (w * 0.45) / (star_cols + 1)
    step_y = (h * 0.55) / (star_rows + 1)
    for r in range(star_rows):
        for c in range(star_cols):
            star = slide.shapes.add_shape(
                MSO_SHAPE.STAR_5_POINT,
                x + step_x * (c + 1) - Inches(0.06),
                y + step_y * (r + 1) - Inches(0.06),
                Inches(0.12),
                Inches(0.12),
            )
            star.fill.solid()
            star.fill.fore_color.rgb = WHITE
            star.line.fill.background()


def add_timeline(slide):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.8), Inches(3.8), Inches(2.9), Inches(0.08))
    line.fill.solid()
    line.fill.fore_color.rgb = NAVY
    line.line.fill.background()

    milestones = [
        ("1607", "Колонии"),
        ("1776", "Независимость"),
        ("1787", "Конституция"),
    ]

    for idx, (year, label) in enumerate(milestones):
        cx = Inches(9.95 + idx * 0.95)
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx, Inches(3.7), Inches(0.25), Inches(0.25))
        dot.fill.solid()
        dot.fill.fore_color.rgb = RED
        dot.line.fill.background()

        tx = slide.shapes.add_textbox(cx - Inches(0.25), Inches(4.03), Inches(0.8), Inches(0.62))
        tf = tx.text_frame
        tf.clear()
        p1 = tf.paragraphs[0]
        p1.text = year
        p1.alignment = PP_ALIGN.CENTER
        p1.runs[0].font.name = "Calibri"
        p1.runs[0].font.bold = True
        p1.runs[0].font.size = Pt(13)
        p1.runs[0].font.color.rgb = NAVY

        p2 = tf.add_paragraph()
        p2.text = label
        p2.alignment = PP_ALIGN.CENTER
        p2.runs[0].font.name = "Calibri"
        p2.runs[0].font.size = Pt(10)
        p2.runs[0].font.color.rgb = TEXT_DARK


def add_growth_visual(slide):
    base = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.7), Inches(1.6), Inches(3.0), Inches(3.3))
    base.fill.solid()
    base.fill.fore_color.rgb = WHITE
    base.line.color.rgb = RGBColor(210, 219, 238)

    bars = [0.7, 1.2, 1.8, 2.4]
    for i, value in enumerate(bars):
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(10.0 + i * 0.62),
            Inches(4.5 - value),
            Inches(0.42),
            Inches(value),
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = NAVY if i % 2 == 0 else RED
        bar.line.fill.background()

    star = slide.shapes.add_shape(MSO_SHAPE.STAR_5_POINT, Inches(11.0), Inches(1.9), Inches(0.45), Inches(0.45))
    star.fill.solid()
    star.fill.fore_color.rgb = RED
    star.line.fill.background()


def add_federal_badge(slide):
    badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.4), Inches(5.3), Inches(1.9), Inches(1.2))
    badge.fill.solid()
    badge.fill.fore_color.rgb = NAVY
    badge.line.color.rgb = RED
    badge.line.width = Pt(2)

    t = slide.shapes.add_textbox(Inches(10.45), Inches(5.56), Inches(1.8), Inches(0.8))
    tf = t.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = "50\nштатов"
    p.alignment = PP_ALIGN.CENTER
    r = p.runs[0]
    r.font.name = "Calibri"
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = WHITE


def create_presentation(output_path: Path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # Slide 1
    slide1 = prs.slides.add_slide(blank)
    set_background(slide1)
    add_top_banner(slide1, "История США: от колоний к независимости")
    add_content_box(
        slide1,
        [
            "Английские колонии возникли на восточном побережье Северной Америки в XVII веке.",
            "В колониях активно развивались торговля, сельское хозяйство и первые мануфактуры.",
            "Недовольство налогами и жёстким контролем Великобритании усиливало протесты.",
            "4 июля 1776 года была принята Декларация независимости США.",
            "После войны за независимость закрепилась Конституция 1787 года.",
        ],
    )
    add_flag_motif(slide1)
    add_timeline(slide1)

    # Slide 2
    slide2 = prs.slides.add_slide(blank)
    set_background(slide2)
    add_top_banner(slide2, "Развитие США: расширение, борьба и мировое влияние")
    add_content_box(
        slide2,
        [
            "В XIX веке США активно расширялись на запад и осваивали новые территории.",
            "Гражданская война 1861–1865 годов стала ключевым конфликтом между Севером и Югом.",
            "Отмена рабства открыла путь к восстановлению и преобразованию страны.",
            "В XX веке США стали ведущей промышленной и политической державой мира.",
            "Современные США — федерация из 50 штатов, опирающаяся на свободу, равенство и демократию.",
        ],
    )
    add_growth_visual(slide2)
    add_federal_badge(slide2)

    prs.save(output_path)


if __name__ == "__main__":
    create_presentation(OUTPUT_FILE)
    print(f"Presentation created: {OUTPUT_FILE}")
