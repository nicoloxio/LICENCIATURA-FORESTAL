import streamlit as st
import json
import random
from pathlib import Path
import time
from collections import defaultdict
import html
from streamlit_local_storage import LocalStorage

BASE = Path(__file__).parent
QUESTIONS_PATH = BASE / "questions.json"
CURRICULUM_PATH = BASE / "curriculum.json"
SOURCES_PATH = BASE / "sources.json"

st.set_page_config(
    page_title="Licenciatura Forestal",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded",
)

ACCENT = "#ff4b4b"

st.markdown("""
<style>
:root {
  --accent: #ff4b4b;
  --accent-soft: #fff1f1;
  --ink: #252936;
  --muted: #737989;
  --line: #e4e8ef;
  --panel: #f5f7fa;
  --good: #16825d;
  --good-bg: #edf9f4;
  --bad: #c33c49;
  --bad-bg: #fff1f3;
}
html, body, [class*="css"], [data-testid="stAppViewContainer"] {
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: var(--ink);
}
[data-testid="stAppViewContainer"] { background: #ffffff; }
[data-testid="stSidebar"] { background: var(--panel); border-right: 1px solid var(--line); }
[data-testid="stSidebar"] * { font-family: inherit; }
.block-container { max-width: 1180px; padding-top: 2.1rem; padding-bottom: 3rem; }
h1, h2, h3 { letter-spacing: -0.025em; color: var(--ink); }
h1 { font-weight: 780 !important; font-size: clamp(2.15rem, 3.3vw, 3.35rem) !important; line-height: 1.05 !important; }
h2 { font-weight: 730 !important; }
p, label, div { line-height: 1.45; }
[data-testid="stMetricLabel"] { font-size: .88rem; color: var(--muted); }
[data-testid="stMetricValue"] { font-size: 2rem; font-weight: 650; letter-spacing: -0.04em; }
[data-testid="stProgress"] > div > div > div > div { background-color: var(--accent); }

/* Buttons become answer cards */
div[data-testid="stButton"] > button {
  width: 100%;
  min-height: 3.25rem;
  border-radius: 14px;
  border: 1px solid var(--line);
  background: #fff;
  color: var(--ink);
  justify-content: flex-start;
  text-align: left;
  white-space: normal;
  padding: .82rem 1rem;
  font-size: 1.02rem;
  font-weight: 540;
  line-height: 1.48;
  box-shadow: none;
  transition: border-color .14s ease, transform .14s ease, background .14s ease;
}
div[data-testid="stButton"] > button:hover {
  border-color: #ff8b8b;
  background: #fff8f8;
  color: var(--ink);
  transform: translateY(-1px);
}
div[data-testid="stButton"] > button[kind="primary"] {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
  font-weight: 650;
}
div[data-testid="stButton"] > button[kind="primary"]:hover { color: white; background: #ef4141; }

.question-shell {
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 1.2rem 1.35rem .3rem 1.35rem;
  background: #fff;
  margin-top: .45rem;
}
.eyebrow { color: var(--muted); font-size: .9rem; font-weight: 560; margin-bottom: .65rem; }
.question-text { font-size: clamp(1.35rem, 2vw, 1.72rem); line-height: 1.33; font-weight: 680; letter-spacing: -0.018em; margin: .2rem 0 1.05rem 0; }
.badges { display:flex; flex-wrap:wrap; gap:.4rem; margin:.25rem 0 .9rem 0; }
.badge { display:inline-flex; align-items:center; border:1px solid var(--line); border-radius:999px; padding:.26rem .58rem; font-size:.78rem; color:#5f6573; background:#fafbfc; }
.badge.accent { color:#c73939; border-color:#ffd2d2; background:#fff5f5; }
.answer-card { border:1px solid var(--line); border-radius:14px; padding:.86rem 1rem; margin:.55rem 0; font-size:1rem; line-height:1.42; }
.answer-card.correct { border-color:#aadfca; background:var(--good-bg); color:#125f47; font-weight:620; }
.answer-card.wrong { border-color:#f0b8bd; background:var(--bad-bg); color:#9e2f3b; font-weight:620; }
.answer-card.neutral { background:#fafbfc; color:#6a707e; }
.answer-letter { display:inline-flex; width:1.75rem; height:1.75rem; align-items:center; justify-content:center; border-radius:8px; margin-right:.55rem; background:#eef1f5; font-weight:720; }
.answer-card.correct .answer-letter { background:#d5f0e4; }
.answer-card.wrong .answer-letter { background:#f8d8dc; }
.hero-kicker { color: var(--accent); font-weight: 720; font-size: .82rem; text-transform: uppercase; letter-spacing: .08em; }
.hero-sub { color: var(--muted); font-size: 1rem; margin-top: -.2rem; }
.coverage-row { display:grid; grid-template-columns:minmax(170px,1fr) 72px; gap:.7rem; align-items:center; margin:.45rem 0; }
.coverage-name { font-size:.92rem; color:#525866; }
.coverage-count { text-align:right; font-size:.83rem; color:#848a97; }
.source-note { color:#8a909b; font-size:.78rem; margin-top:.3rem; }
.small-note { color:var(--muted); font-size:.86rem; }
[data-testid="stSidebar"] h2 { font-size: 1.25rem; }
[data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] .stMultiSelect { margin-bottom: .15rem; }
@media (max-width: 700px) {
  .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 1rem; }
  .question-shell { padding: 1rem .95rem .25rem .95rem; }
}

.reason-grid { margin-top:.55rem; display:grid; gap:.48rem; }
.reason-row { border:1px solid var(--line); border-radius:12px; padding:.72rem .85rem; background:#fafbfc; }
.reason-row.good { border-color:#b8dfcf; background:#f3fbf7; }
.reason-row.bad { border-color:#e4e8ef; background:#fafbfc; }
.reason-head { font-weight:700; margin-bottom:.18rem; }
.reason-text { color:#535a68; font-size:.94rem; line-height:1.5; }
.why-box { border-left:3px solid var(--accent); padding:.25rem 0 .25rem .9rem; margin:.85rem 0 1rem 0; }
.why-title { font-weight:760; margin-bottom:.25rem; }
.why-text { color:#454b58; line-height:1.58; }

.visual-wrap { margin:.85rem 0 1.1rem 0; }
.visual-caption { color:var(--muted); font-size:.82rem; margin-top:.32rem; }
.qtable-wrap { overflow-x:auto; margin:.85rem 0 1.05rem 0; border:1px solid var(--line); border-radius:14px; }
.qtable { width:100%; border-collapse:collapse; font-size:.94rem; }
.qtable th { background:#f6f8fa; font-weight:700; color:#414754; }
.qtable th,.qtable td { padding:.64rem .72rem; border-bottom:1px solid var(--line); text-align:center; }
.qtable tr:last-child td { border-bottom:none; }

</style>
""", unsafe_allow_html=True)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_question_visual(q):
    vis = q.get("visual")
    if not vis:
        return
    vtype = vis.get("type")
    if vtype == "image":
        source = vis.get("url") or str(BASE / vis.get("path", ""))
        st.image(source, use_container_width=True)
        if vis.get("caption"):
            st.markdown(f"<div class='visual-caption'>{html.escape(str(vis['caption']))}</div>", unsafe_allow_html=True)
    elif vtype == "table":
        cols = vis.get("columns", [])
        rows = vis.get("rows", [])
        h = "<div class='qtable-wrap'><table class='qtable'><thead><tr>" + "".join(f"<th>{html.escape(str(c))}</th>" for c in cols) + "</tr></thead><tbody>"
        for row in rows:
            h += "<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>"
        h += "</tbody></table></div>"
        st.markdown(h, unsafe_allow_html=True)
        if vis.get("caption"):
            st.markdown(f"<div class='visual-caption'>{html.escape(str(vis['caption']))}</div>", unsafe_allow_html=True)

QUESTIONS = load_json(QUESTIONS_PATH)
CURRICULUM = load_json(CURRICULUM_PATH)
SOURCES = load_json(SOURCES_PATH)
Q_BY_ID = {str(q["id"]): q for q in QUESTIONS}


# El progreso se guarda en el navegador, no en el servidor.
# Así dos personas pueden usar la misma URL sin mezclar estadísticas.
LOCAL_STORAGE_KEY = "licenciatura_forestal_progress_v1"
local_storage = LocalStorage()


def _empty_history():
    return {}


def load_history():
    if "history_cache" not in st.session_state:
        stored = local_storage.getItem(LOCAL_STORAGE_KEY)
        st.session_state.history_cache = stored if isinstance(stored, dict) else _empty_history()
    return st.session_state.history_cache


def persist_history():
    local_storage.setItem(LOCAL_STORAGE_KEY, st.session_state.history_cache)


def save_attempt(question_id, correct, selected):
    qid = str(question_id)
    history = load_history()
    row = history.get(qid, {"attempts": 0, "correct": 0, "last_selected": None})
    row["attempts"] = int(row.get("attempts", 0)) + 1
    row["correct"] = int(row.get("correct", 0)) + int(bool(correct))
    row["last_selected"] = int(selected)
    history[qid] = row
    st.session_state.history_cache = history
    persist_history()


def all_stats():
    return load_history()


def reset_session():
    st.session_state.queue = []
    st.session_state.idx = 0
    st.session_state.answered = False
    st.session_state.selected = None
    st.session_state.session_correct = 0
    st.session_state.session_total = 0
    st.session_state.session_results = []


def start_session(pool, n):
    random.shuffle(pool)
    st.session_state.queue = [str(q["id"]) for q in pool[:min(n, len(pool))]]
    st.session_state.idx = 0
    st.session_state.answered = False
    st.session_state.selected = None
    st.session_state.session_correct = 0
    st.session_state.session_total = 0
    st.session_state.session_results = []


for key, default in {
    "queue": [], "idx": 0, "answered": False, "selected": None,
    "session_correct": 0, "session_total": 0, "session_results": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

history = all_stats()

# ----- Sidebar -----
with st.sidebar:
    st.markdown("## Configurar práctica")
    mode = st.radio("Modo", ["Práctica", "Simulacro"], horizontal=True)

    courses = ["Todos"] + sorted({q["course"] for q in QUESTIONS})
    course = st.selectbox("Ramo", courses)

    theme_pool = sorted({q["theme"] for q in QUESTIONS if course == "Todos" or q["course"] == course})
    theme = st.selectbox("Tema", ["Todos"] + theme_pool)

    diff = st.multiselect("Dificultad", [1, 2, 3, 4], default=[1, 2, 3, 4])
    max_n = min(80, len(QUESTIONS))
    n = st.slider("Número de preguntas", 5, max_n, 15, step=5)
    only_failed = st.checkbox("Priorizar preguntas falladas")
    origin_options = ["Tipo/oficial", "Examen anterior", "Investigada"]
    origins = st.multiselect("Origen", origin_options, default=origin_options)
    only_visual = st.checkbox("Sólo preguntas visuales")

    def origin_label(item):
        prov = item.get("provenance")
        if prov == "official_type":
            return "Tipo/oficial"
        if prov == "recovered_exam":
            return "Examen anterior"
        return "Investigada"

    if st.button("Iniciar / reiniciar", type="primary", use_container_width=True):
        pool = [q for q in QUESTIONS
                if (course == "Todos" or q["course"] == course)
                and (theme == "Todos" or q["theme"] == theme)
                and q["difficulty"] in diff
                and origin_label(q) in origins
                and (not only_visual or bool(q.get("visual")))]
        if only_failed:
            failed = [q for q in pool if history.get(str(q["id"]), {}).get("attempts", 0) > history.get(str(q["id"]), {}).get("correct", 0)]
            if failed:
                pool = failed
        if not pool:
            st.warning("No hay preguntas que cumplan esos filtros.")
        else:
            start_session(pool, n)
            st.rerun()

    st.divider()
    st.markdown("<div class='small-note'>El banco distingue preguntas tipo/oficiales, preguntas recuperadas de exámenes anteriores y preguntas investigadas. En las recuperadas se excluyeron anotaciones y claves estudiantiles antes de validar la respuesta.</div>", unsafe_allow_html=True)

# ----- Header -----
st.markdown("<div class='hero-kicker'>Entrenador de examen</div>", unsafe_allow_html=True)
st.title("Examen de Licenciatura · Ingeniería Forestal")
st.markdown("<div class='hero-sub'>Práctica guiada por ramo, tema y dificultad, con preguntas conceptuales, cálculos e interpretación visual.</div>", unsafe_allow_html=True)

attempts = sum(v["attempts"] for v in history.values())
corrects = sum(v["correct"] for v in history.values())
accuracy = round(100 * corrects / attempts) if attempts else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Preguntas", len(QUESTIONS))
m2.metric("Temas cubiertos", len({q['theme_id'] for q in QUESTIONS}))
m3.metric("Intentos", attempts)
m4.metric("Precisión", f"{accuracy}%")

# ----- Empty state / coverage -----
if not st.session_state.queue:
    st.info("Configura una sesión en la barra lateral y presiona **Iniciar / reiniciar**.")
    st.subheader("Cobertura del banco")
    by_course = defaultdict(int)
    themes_by_course = defaultdict(set)
    for q in QUESTIONS:
        by_course[q["course"]] += 1
        themes_by_course[q["course"]].add(q["theme_id"])
    cols = st.columns(2)
    for j, c in enumerate(sorted(by_course)):
        with cols[j % 2]:
            st.markdown(f"**{c}**")
            st.caption(f"{by_course[c]} preguntas · {len(themes_by_course[c])} temas")
            st.progress(by_course[c] / max(by_course.values()))
    st.stop()

# ----- Question -----
idx = st.session_state.idx
queue = st.session_state.queue
if idx >= len(queue):
    st.success("Sesión terminada")
    score = st.session_state.session_correct
    total = st.session_state.session_total
    pct = round(100 * score / total) if total else 0
    a, b, c = st.columns(3)
    a.metric("Resultado", f"{score}/{total}")
    b.metric("Precisión sesión", f"{pct}%")
    c.metric("Errores", max(0, total-score))

    wrongs = [r for r in st.session_state.session_results if not r["correct"]]
    if wrongs:
        st.subheader("Preguntas a repasar")
        for r in wrongs:
            q = Q_BY_ID[r["qid"]]
            with st.expander(f"{q['course']} · {q['theme']} — {q['question'][:85]}…"):
                st.write(q["question"])
                st.write(f"**Tu respuesta:** {q['options'][r['selected']]}")
                st.write(f"**Correcta:** {q['options'][q['answer']]}")
                st.write(q["explanation"])
    if st.button("Nueva sesión", type="primary"):
        reset_session(); st.rerun()
    st.stop()

q = Q_BY_ID[queue[idx]]
progress = idx / max(1, len(queue))
st.progress(progress)

if q.get("provenance") == "official_type":
    prov = "Tipo/oficial"
elif q.get("provenance") == "recovered_exam":
    prov = "Examen anterior"
else:
    prov = "Investigada"
course_html = html.escape(str(q['course']))
theme_html = html.escape(str(q['theme']))
qtype_html = html.escape(str(q['question_type']))
question_html = html.escape(str(q['question']))
st.markdown(f"""
<div class="question-shell">
  <div class="eyebrow">Pregunta {idx+1} de {len(queue)}</div>
  <div class="badges">
    <span class="badge accent">{course_html}</span>
    <span class="badge">{theme_html}</span>
    <span class="badge">Dificultad {q['difficulty']}/4</span>
    <span class="badge">{qtype_html}</span>
    <span class="badge">{prov}</span>
  </div>
  <div class="question-text">{question_html}</div>
</div>
""", unsafe_allow_html=True)

render_question_visual(q)

if not st.session_state.answered:
    st.caption("Elige una alternativa")
    for i, option in enumerate(q["options"]):
        label = str(option)
        if st.button(label, key=f"opt_{q['id']}_{idx}_{i}", use_container_width=True):
            selected = i
            correct = selected == q["answer"]
            save_attempt(q["id"], correct, selected)
            time.sleep(0.15)
            st.session_state.session_total += 1
            st.session_state.session_correct += int(correct)
            st.session_state.session_results.append({"qid": str(q["id"]), "selected": selected, "correct": correct})
            if mode == "Simulacro":
                st.session_state.idx += 1
                st.session_state.selected = None
                st.rerun()
            else:
                st.session_state.selected = selected
                st.session_state.answered = True
                st.rerun()
else:
    selected = st.session_state.selected
    for i, option in enumerate(q["options"]):
        if i == q["answer"]:
            cls = "correct"
        elif i == selected and selected != q["answer"]:
            cls = "wrong"
        else:
            cls = "neutral"
        st.markdown(f"<div class='answer-card {cls}'>{html.escape(str(option))}</div>", unsafe_allow_html=True)

    if selected == q["answer"]:
        st.success("Correcta")
    else:
        st.error(f"Incorrecta · Respuesta correcta: {q['options'][q['answer']]}")
    explanation_html = html.escape(str(q['explanation']))
    st.markdown(f"<div class='why-box'><div class='why-title'>Por qué</div><div class='why-text'>{explanation_html}</div></div>", unsafe_allow_html=True)

    option_reasons = q.get('option_explanations', [])
    if option_reasons:
        st.markdown("**Revisión de alternativas**")
        st.markdown("<div class='reason-grid'>", unsafe_allow_html=True)
        for i, reason in enumerate(option_reasons):
            good = i == q['answer']
            status = 'Correcta' if good else 'Incorrecta'
            cls = 'good' if good else 'bad'
            st.markdown(
                f"<div class='reason-row {cls}'><div class='reason-head'>{status}</div><div class='reason-text'>{html.escape(str(reason).replace('Correcta. ','').replace('Incorrecta. ',''))}</div></div>",
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

    refs = q.get('references', [])
    if refs:
        with st.expander('Base técnica', expanded=False):
            st.caption('Referencias usadas para construir o verificar esta pregunta:')
            for ref_id in refs:
                ref = SOURCES.get(ref_id)
                if ref:
                    st.markdown(f"- [{ref['title']}]({ref['url']})" if ref.get('url') else f"- {ref['title']}")


    if st.button("Siguiente →", type="primary", use_container_width=True):
        st.session_state.idx += 1
        st.session_state.answered = False
        st.session_state.selected = None
        st.rerun()

st.divider()
with st.expander("Progreso de este tema"):
    theme_questions = [x for x in QUESTIONS if x["theme_id"] == q["theme_id"]]
    attempted = [x for x in theme_questions if str(x["id"]) in history]
    total_a = sum(history[str(x["id"])]["attempts"] for x in attempted) if attempted else 0
    total_c = sum(history[str(x["id"])]["correct"] for x in attempted) if attempted else 0
    theme_acc = round(100*total_c/total_a) if total_a else 0
    st.write(f"**{q['theme']}**")
    st.write(f"{len(theme_questions)} preguntas disponibles · {len(attempted)} distintas practicadas · {theme_acc}% de precisión histórica")
