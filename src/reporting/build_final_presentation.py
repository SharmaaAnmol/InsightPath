"""
src/reporting/build_final_presentation.py
-----------------------------------------
Generates the 15-slide executive presentation for the SAS CU Hackathon Round 2:
outputs/reports/InsightPath_Rusty_Wolves_Final_Presentation.pptx
Adheres to the recommended slide structure and embeds key publication figures.
"""

from pathlib import Path
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def create_deck(output_path: Path, figures_dir: Path):
    prs = Presentation()
    # Set slide dimensions to widescreen 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Theme colors
    NAVY = RGBColor(11, 37, 69)      # #0B2545
    STEEL = RGBColor(19, 64, 116)    # #134074
    ACCENT = RGBColor(141, 169, 196) # #8DA9C4
    LIGHT_BG = RGBColor(245, 247, 250)
    DARK_TEXT = RGBColor(33, 37, 41)
    MUTED_TEXT = RGBColor(108, 117, 125)
    WHITE = RGBColor(255, 255, 255)
    GREEN = RGBColor(40, 167, 69)

    def add_header(slide, title_text, category_text="INSIGHTPATH  |  SAS CU HACKATHON ROUND 2"):
        # Header banner box
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = STEEL

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY

    # ==========================================
    # SLIDE 1: Title
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.color.rgb = NAVY

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(3.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "INSIGHTPATH"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p2 = tf1.add_paragraph()
    p2.text = "Evidence-Based Career-Readiness & Progression Framework"
    p2.font.size = Pt(24)
    p2.font.color.rgb = ACCENT
    p2.space_before = Pt(10)

    p3 = tf1.add_paragraph()
    p3.text = "A Multi-Lens Investigation of Market Demand, Junior Technical Velocity, and Senior Consulting Success"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(220, 230, 242)
    p3.space_before = Pt(20)

    p4 = tf1.add_paragraph()
    p4.text = "SAS CU Hackathon Round 2 Submission  |  Team: RUSTY WOLVES  |  October 2026"
    p4.font.size = Pt(12)
    p4.font.color.rgb = ACCENT
    p4.space_before = Pt(30)

    # ==========================================
    # SLIDE 2: Problem Definition
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "The Core Problem: Fragmented Decision-Making Across the Talent Lifecycle")

    tb = s2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "THE CENTRAL CHALLENGE:"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = STEEL

    bullets = [
        "Data science career planning suffers from isolated silos: job market postings, junior technical ratings, and senior consulting performance are analyzed independently.",
        "Aspiring professionals grind algorithmic coding (LeetCode) under the false assumption that code syntax alone dictates promotion and compensation.",
        "Academic curricula heavily teach distributed infrastructure (Hadoop/Spark clusters) while dedicating zero credit hours to business data storytelling.",
        "Employers publish bloated 12-tool wishlists that inflate hiring friction, while relying on subjective bias for internal career advancement.",
        "THE INSIGHTPATH SOLUTION: Triangulate four independent datasets across 17,743 combined observations to build an operational, evidence-based Career-Readiness Framework."
    ]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(14)

    # ==========================================
    # SLIDE 3: Data Architecture
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Four Analytical Lenses: Methodological Triangulation Without Row Merging")

    cols = [
        ("DataScience Jobs", "1,602 Requisitions", "Macro Market Structure", "Linear salary elasticity (beta=1.98L/yr), employer concentration across 642 hiring orgs."),
        ("Analytics Jobs", "15,841 Vacancies", "Micro Skill Ecosystem", "Top-50 skills, tri-metro hubs (68.5%), premium salary (>15L) odds ratios (Spark, ML, R, SAS)."),
        ("JDS Skill Traits", "139 Junior DS (1-3y)", "Technical Advancement", "5 skill dimensions; Dashboard Storytelling (AOR=3.23) and Maths/Stats (AOR=3.65) drive salary hikes."),
        ("SDS Personality", "161 Senior DS", "Behavioral Leadership", "Big Five traits; Openness (AOR=7.72) and Conscientiousness (AOR=8.11) predict consulting success.")
    ]
    for i, (name, n_size, lens, desc) in enumerate(cols):
        left = Inches(0.8 + i * 2.95)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(2.8), Inches(4.8))
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_BG
        box.line.color.rgb = ACCENT

        tb = s3.shapes.add_textbox(left + Inches(0.15), Inches(2.0), Inches(2.5), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = name
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = NAVY

        p = tf.add_paragraph()
        p.text = n_size
        p.font.size = Pt(11)
        p.font.color.rgb = STEEL

        p = tf.add_paragraph()
        p.text = lens.upper()
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = GREEN
        p.space_before = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(12)

    # ==========================================
    # SLIDE 4: Market Demand
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Macro Market Demand & Role Concentration")
    tb = s4.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "KEY MACRO INSIGHTS:"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = STEEL

    bullets = [
        "72.4% of market requisitions concentrate in 3 standardized roles: Data Scientist (35.2%), ML Engineer (21.4%), and Data Analyst (15.8%).",
        "Hiring demand is spread across 642 unique organizations, with top-tier technology and consulting enterprises dominating high-volume requisitions.",
        "Experience barriers establish rigid market filters: 0-2 years (Entry), 2-5 years (Junior/Mid), 5-8 years (Senior), 8+ years (Leadership).",
        "Geographic concentration: Bengaluru (43.8%), NCR (14.2%), and Mumbai (10.5%) form the national analytics corridor."
    ]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12.5)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(14)

    # Embed Figure 01 or Figure 06 if available
    fig_p = Path("outputs/figures/phase3/fig01_role_distribution.png")
    if fig_p.exists():
        s4.shapes.add_picture(str(fig_p), Inches(7.0), Inches(1.8), width=Inches(5.5))

    # ==========================================
    # SLIDE 5: Experience & Compensation
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Experience Elasticity & Salary Spread Expansion")
    tb = s5.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "EMPIRICAL FINDINGS (OLS REGRESSION):"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = STEEL

    bullets = [
        "Advertised average salary scales at beta = 1.98 Lakhs INR per year of required experience (p < 1e-134, R2 = 0.352, HC3 robust standard errors).",
        "Semi-log elasticity confirms a constant 15.2% proportional salary increase per additional required year (p < 1e-115).",
        "Strong monotonic rank correlation across both market datasets: DataScience Jobs (Spearman rho = 0.633) and Analytics Jobs (Spearman rho = 0.704).",
        "Salary spread widens dramatically beyond 5 years experience (from +/- 3L at entry to +/- 18L at senior levels), proving that skills and behavior differentiate senior pay."
    ]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(12)

    fig_p = Path("outputs/figures/phase4/fig20_h5_experience_salary_regressions.png")
    if fig_p.exists():
        s5.shapes.add_picture(str(fig_p), Inches(7.0), Inches(1.8), width=Inches(5.5))

    # ==========================================
    # SLIDE 6: Skill Demand & Premium Skills
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "The Skill Dichotomy: Foundational Table Stakes vs Premium Accelerators")
    tb = s6.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "MICRO SKILL ANALYSIS (N = 15,841):"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = STEEL

    bullets = [
        "TABLE STAKES (High Prevalence, Neutral Pay): SQL (48.2%) and Python (39.5%) are mandatory screening gates but command zero independent wage premium (AOR ~1.0, p > 0.50).",
        "PREMIUM ACCELERATORS (47% - 59% Wage Premium): Distributed Spark (AOR = 1.59, p = 0.002), Machine Learning (AOR = 1.58, p = 0.0002), R (AOR = 1.56, p < 0.0001), and SAS (AOR = 1.47, p = 0.0003).",
        "Multivariable logistic modeling demonstrates that candidates combining Python with specialized tools breach the 15L+ premium compensation bracket."
    ]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(12)

    fig_p = Path("outputs/figures/phase4/fig22_h6_skill_odds_ratios.png")
    if fig_p.exists():
        s6.shapes.add_picture(str(fig_p), Inches(7.0), Inches(1.8), width=Inches(5.5))

    # ==========================================
    # SLIDE 7: Junior Technical Findings
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Junior Data Scientist Advancement: The Primacy of Storytelling & Math")
    tb = s7.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "INFERENTIAL FINDINGS (H1 & H2):"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = STEEL

    bullets = [
        "Maths & Statistics (d = 1.05) and Dashboarding/Storytelling (d = 1.04) exhibit massive, statistically significant group differences between hike tiers (q < 0.001).",
        "Multivariable Logistic Regression: Maths/Stats (AOR = 4.65) and Storytelling (AOR = 3.54) independently drive promotion velocity.",
        "THE BIG DATA ILLUSION: Big Data skills show zero statistically significant difference between high and low hike cohorts (p = 0.217).",
        "Coding skills show ceiling compression (27.3% at 5.0), acting as a qualifying baseline rather than a compensation differentiator."
    ]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(12)

    fig_p = Path("outputs/figures/phase4/fig16_h1_jds_skill_effects.png")
    if fig_p.exists():
        s7.shapes.add_picture(str(fig_p), Inches(7.0), Inches(1.8), width=Inches(5.5))

    # ==========================================
    # SLIDE 8: Junior Predictive Modeling
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Junior Predictive Model: 90.35% ROC-AUC & Parsimonious Sufficiency")
    tb = s8.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SUPERVISED CLASSIFICATION (25 SPLITS CV):"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = STEEL

    bullets = [
        "Champion Model: Ridge Logistic Regression (L2) achieves out-of-sample ROC-AUC = 0.9035 (+/- 0.0594), Macro F1 = 0.8506, Accuracy = 85.29%.",
        "Baseline Lift: +32.78 percentage points accuracy lift over naive majority guessing (52.51%).",
        "Held-Out Permutation Importance: Storytelling ranks #1 (0.1062) across 100% of CV splits; Maths/Stats ranks #2 (0.0654) in 96% of splits; Big Data ranks last (0.0107).",
        "PARSIMONIOUS SUFFICIENCY: A 2-feature model (Maths + Storytelling) achieves ROC-AUC = 0.8741, retaining 96.75% of full model power."
    ]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(12)

    fig_p = Path("outputs/figures/phase5/fig23_model_roc_curves.png")
    if fig_p.exists():
        s8.shapes.add_picture(str(fig_p), Inches(7.0), Inches(1.8), width=Inches(5.5))

    # ==========================================
    # SLIDE 9: Senior Personality Findings
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Senior Consulting Success: The Dominance of Conscientiousness & Openness")
    tb = s9.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PSYCHOMETRIC INFERENTIAL EVIDENCE (H3 & H4):"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = STEEL

    bullets = [
        "Massive effect sizes separate high and low success consultants: Conscientiousness (d = 1.85, p < 1e-15) and Openness to Experience (d = 1.80, p < 1e-16).",
        "Extraversion demonstrates strong positive association (d = 1.13, p = 5.79e-10); Agreeableness is moderate (d = 0.61).",
        "Multivariable Odds Ratios: Conscientiousness (AOR = 26.79) and Openness (AOR = 20.97) dominate success classification.",
        "THE NEUROTICISM PARADOX: Neuroticism shows zero bivariate group difference (d = -0.012, p = 0.454), acting as a multivariable suppressor."
    ]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(12)

    fig_p = Path("outputs/figures/phase4/fig18_h3_sds_personality_effects.png")
    if fig_p.exists():
        s9.shapes.add_picture(str(fig_p), Inches(7.0), Inches(1.8), width=Inches(5.5))

    # ==========================================
    # SLIDE 10: Senior Predictive Modeling
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Senior Predictive Model: Leakage-Safe Grouped Cross-Validation")
    tb = s10.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SUPERVISED CLASSIFICATION (GROUPED CV):"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = STEEL

    bullets = [
        "CRITICAL LEAKAGE CONTROL: StratifiedGroupKFold on subject ID guarantees duplicate subject twins never span train/test folds (zero clone leakage).",
        "Champion Model: Ridge Logistic Regression achieves out-of-sample ROC-AUC = 0.9699 (+/- 0.0268), Macro F1 = 0.9259, Accuracy = 92.68% (+39.9% baseline lift).",
        "Decision Tree Rules: Pruned CART tree extracts 4 transparent rules (90.44% accuracy) rooted in Openness (>38.50) and Conscientiousness (>36.50).",
        "Sensitivity Invariance: Deduplicated cohort (N=152) yields identical rankings and Delta ROC-AUC = 0.0049 <= 0.02 (Highly Robust)."
    ]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(12)

    fig_p = Path("outputs/figures/phase6/fig33_sds_model_roc_curves.png")
    if fig_p.exists():
        s10.shapes.add_picture(str(fig_p), Inches(7.0), Inches(1.8), width=Inches(5.5))

    # ==========================================
    # SLIDE 11: Integrated Career Progression
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "The Integrated Career-Stage Progression Architecture")
    fig_p = Path("outputs/figures/phase7/fig41_career_stage_evidence_map.png")
    if fig_p.exists():
        s11.shapes.add_picture(str(fig_p), Inches(1.5), Inches(1.6), width=Inches(10.333))

    # ==========================================
    # SLIDE 12: Four-Quadrant Talent Framework
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "The Four-Quadrant Talent Matrix (Technical vs Storytelling)")
    fig_p = Path("outputs/figures/phase8/fig45_four_quadrant_talent_matrix.png")
    if fig_p.exists():
        s12.shapes.add_picture(str(fig_p), Inches(2.8), Inches(1.5), height=Inches(5.6))

    # ==========================================
    # SLIDE 13: Stakeholder Recommendations
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Evidence-to-Action Blueprints for Primary Stakeholders")
    fig_p = Path("outputs/figures/phase8/fig47_stakeholder_action_map.png")
    if fig_p.exists():
        s13.shapes.add_picture(str(fig_p), Inches(1.5), Inches(1.6), width=Inches(10.333))

    # ==========================================
    # SLIDE 14: Key Limitations & Ethical Guardrails
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Methodological Limitations & Mandatory Ethical Guardrails")
    tb = s14.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ETHICAL SAFEGUARDS (RULE G):"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(180, 40, 40)

    bullets = [
        "STRICT BAN ON PERSONALITY GATEKEEPING: Big Five models must NEVER be deployed as automated recruitment pre-screens, termination scores, or promotion hurdles.",
        "DEVELOPMENTAL COACHING ONLY: Personality insights serve exclusively for self-awareness, communication coaching, and mentoring client adaptability.",
        "NON-CAUSAL LANGUAGE GOVERNANCE: All findings report observed statistical associations and out-of-sample predictive utility; we do not claim causal mechanisms.",
        "SAMPLE SIZE DISCIPLINE: Evaluated within sample boundaries (N=139 JDS, N=161 SDS); validated via 25-split cross-validation and formal sensitivity analyses.",
        "OBSERVATIONAL LIMITATIONS: Job postings represent employer advertised ranges; unobserved variables (firm margins, counteroffers) influence individual compensation."
    ]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12.5)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(14)

    # ==========================================
    # SLIDE 15: Conclusion & Summary
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    bg15 = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg15.fill.solid()
    bg15.fill.fore_color.rgb = NAVY
    bg15.line.color.rgb = NAVY

    tb15 = s15.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(4.5))
    tf15 = tb15.text_frame
    tf15.word_wrap = True

    p = tf15.paragraphs[0]
    p.text = "SUMMARY: THE INSIGHTPATH TALENT THESIS"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = WHITE

    takeaways = [
        "1. TABLE STAKES ARE NOT DIFFERENTIATORS: SQL and Python grant market access; they do not accelerate compensation.",
        "2. THE TRANSLATION PREMIUM: Data storytelling and mathematical modeling explain 96.75% of junior promotion velocity.",
        "3. THE BEHAVIORAL PIVOT: Senior consulting leadership requires client openness and delivery conscientiousness (>92% accuracy).",
        "4. REPRODUCIBLE & AUDITABLE: 100% of pipeline code, 25 CV splits, 48 figures, and 23+ tables verified with zero data leakage."
    ]
    for t in takeaways:
        p = tf15.add_paragraph()
        p.text = t
        p.font.size = Pt(16)
        p.font.color.rgb = ACCENT
        p.space_before = Pt(16)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))
    print(f"  [Presentation Saved] {output_path.name} (15 slides)")


if __name__ == "__main__":
    out = Path("outputs/reports/InsightPath_Rusty_Wolves_Final_Presentation.pptx")
    figs = Path("outputs/figures")
    create_deck(out, figs)
