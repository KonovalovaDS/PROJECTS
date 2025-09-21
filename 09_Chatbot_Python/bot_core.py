# bot_core.py
import os, re, json, numpy as np, pandas as pd
from annoy import AnnoyIndex

# ---- Optional spaCy (POS-aware) preprocessing ----
def _load_spacy():
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm", exclude=["parser","ner","textcat","senter"])
        except Exception:
            # If the model isn't installed on the server, just skip; we'll fall back
            return None
        return nlp
    except Exception:
        return None

_WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._\-]*")

def make_preprocess(nlp):
    if nlp is None:
        # Fallback: simple regex + stopwords
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
        STOP = set(ENGLISH_STOP_WORDS)
        def preprocess(text: str):
            toks = _WORD_RE.findall(str(text).lower())
            return [t for t in toks if t and t not in STOP]
        return preprocess
    else:
        STOP = set(nlp.Defaults.stop_words)
        WH_KEEP = {"why","what","how","where","when","which","who","whom","whose"}
        STOP = STOP - WH_KEEP  # keep question words
        def preprocess(text: str):
            toks = _WORD_RE.findall(str(text).lower())
            if not toks: return []
            doc = nlp(" ".join(toks))
            return [t.lemma_ for t in doc if t.lemma_ and t.lemma_ not in STOP]
        return preprocess

def _norm(s: str) -> str:
    s = str(s or "").casefold()
    s = re.sub(r"[\"'’`´]", "", s)
    s = re.sub(r"\s+"," ", s).strip()
    return s

# Stoplists (we tuned these together)
LEX_STOP = {
    "python","package","library","module","install","pip","pip3","pipx","pypi",
    "on","for","with","the","a","an","in","to","of","and","is","are"
}
FAQ_STOP = {
    "package","library","module","install","pip","pip3","pipx","pypi",
    "on","for","with","the","a","an","in","to","of","and","is","are"
}
WH = {"what","why","how","where","when","which","who","whom","whose",
      "can","are","is","does","do","did","was","were","will","shall",
      "should","could","would","may","might","must"}
GENERIC_Q = {"use","using","today","now","way","ways","make","get","work",
             "works","find","need","want","example","examples","show","tell","help"}
FAQ_OVERLAP_STOP = FAQ_STOP | WH | GENERIC_Q

# Preferences (same as your notebook)
PROD_SIM_TH = 0.60
FAQ_SIM_TH  = 0.35
PREF_MARGIN = 0.20

_WH_WORDS = {"what","why","how","where","when","which","who","whom","whose","can","are","is","does","do"}
def _looks_like_question(q: str) -> bool:
    s = (q or "").strip().lower()
    if not s: return False
    if s.endswith("?"): return True
    first = re.findall(r"^[a-z]+", s)
    return bool(first and first[0] in _WH_WORDS)

def _tokset(text, stop):
    return set(t for t in re.findall(r"[a-z0-9]+", _norm(text)) if t not in stop)

def _canon_pkg(s: str) -> str:
    s = str(s or "").strip().lower().replace("_","-")
    return re.sub(r"[^a-z0-9\-.]+", "", s)

# ---- Artifact loader ----
class Chatbot:
    def __init__(self, base_dir=".", models_dir="models", data_dir="data"):
        self.base_dir   = base_dir
        self.models_dir = os.path.join(base_dir, models_dir)
        self.data_dir   = os.path.join(base_dir, data_dir)

        # 1) Preprocessing
        self.nlp = _load_spacy()
        self.preprocess = make_preprocess(self.nlp)

        # 2) Load KeyedVectors OR fallback
        self.kv = None
        self.D  = 100  # default embedding size
        try:
            from gensim.models import KeyedVectors
            kv_path = os.path.join(self.models_dir, "w2v_vectors.kv")
            if os.path.exists(kv_path):
                self.kv = KeyedVectors.load(kv_path, mmap="r")
                self.kv.fill_norms()
                self.D = int(self.kv.vector_size)
        except Exception:
            self.kv = None

        # 3) Load Annoy indexes + maps
        self.prod_index = AnnoyIndex(self.D, "angular")
        self.prod_index.load(os.path.join(self.models_dir, "product.ann"))
        self.faq_index  = AnnoyIndex(self.D, "angular")
        self.faq_index.load(os.path.join(self.models_dir, "faq.ann"))

        with open(os.path.join(self.models_dir, "product_map.json"), "r", encoding="utf-8") as f:
            _pmap = json.load(f)
        self.prod_map = {int(k): v for k, v in _pmap.items()}

        with open(os.path.join(self.models_dir, "faq_map.json"), "r", encoding="utf-8") as f:
            _fmap = json.load(f)
        self.faq_map = {int(k): v for k, v in _fmap.items()}

        with open(os.path.join(self.models_dir, "faq_q.json"), "r", encoding="utf-8") as f:
            self.faq_questions = json.load(f)

        # 4) Build lexical structures
        # products
        prod_csv = os.path.join(self.data_dir, "products_pypi.csv")
        self.product = pd.read_csv(prod_csv)
        self.product["product_id"]  = self.product["product_id"].astype(str)
        self.product["title"]       = self.product["title"].fillna("").astype(str)
        self.product["description"] = self.product["description"].fillna("").astype(str)

        self.product_lex = []
        for r in self.product.itertuples(index=False):
            title = str(getattr(r, "title", ""))
            desc  = str(getattr(r, "description", ""))
            self.product_lex.append({
                "product_id": str(r.product_id),
                "title": title,
                "norm_title": _norm(title),
                "title_toks": _tokset(title, LEX_STOP),
                "desc_toks":  _tokset(desc,  LEX_STOP),
            })

        # name aliases (for pip install)
        self.name_index = {}
        for r in self.product.itertuples(index=False):
            pid   = _canon_pkg(getattr(r, "product_id", ""))
            title = str(getattr(r, "title", "")) or pid
            if not pid:
                continue
            rec = {"product_id": str(getattr(r,"product_id")), "title": title}
            self.name_index[pid] = rec
            alias = _canon_pkg(title)
            if alias and alias not in self.name_index:
                self.name_index[alias] = rec
            if alias.startswith("python-"):
                core = alias[len("python-"):]
                if core and core not in self.name_index:
                    self.name_index[core] = rec

        # faq lexical
        self.faq_lex = []
        for i, q in enumerate(self.faq_questions):
            a = self.faq_map.get(i, "")
            nq = _norm(q)
            toks_exact   = _tokset(nq, FAQ_STOP)
            toks_overlap = _tokset(nq, FAQ_OVERLAP_STOP)
            self.faq_lex.append({"nq": nq, "toks": toks_exact, "toks_overlap": toks_overlap, "ans": a})

        # optional: BM25 (if rank_bm25 is installed)
        self.bm25 = None
        try:
            from rank_bm25 import BM25Okapi
            faq_q_tok_bm25 = [self.preprocess(q) for q in self.faq_questions]
            self.bm25 = BM25Okapi(faq_q_tok_bm25)
        except Exception:
            pass

        # optional: classifiers (if present)
        self.svc = None; self.lr = None
        try:
            import joblib
            svc_p = os.path.join(self.models_dir, "product_query_svc.pkl")
            lr_p  = os.path.join(self.models_dir, "product_query_lr.pkl")
            if os.path.exists(svc_p): self.svc = joblib.load(svc_p)
            if os.path.exists(lr_p):  self.lr  = joblib.load(lr_p)
        except Exception:
            pass

    # ---- encoding / sims ----
    def encode_tokens(self, tokens):
        if self.kv is None or not tokens:
            return None
        vec = np.zeros(self.D, dtype=np.float32); n = 0
        for w in tokens:
            if w in self.kv:
                vec += self.kv.get_vector(w, norm=True); n += 1
        if n == 0: return None
        vec /= n; nrm = np.linalg.norm(vec)
        if nrm == 0: return None
        return (vec / nrm).astype(np.float32)

    def _encode_query(self, text):
        return self.encode_tokens(self.preprocess(text))

    def _best_sim_product(self, qv, k=3):
        ids, dists = self.prod_index.get_nns_by_vector(qv, k, include_distances=True)
        if not ids: return None, -1.0
        sims = [1.0 - (d*d)/2.0 for d in dists]
        return ids[0], sims[0]

    def _best_sim_faq(self, qv, k=3):
        ids, dists = self.faq_index.get_nns_by_vector(qv, k, include_distances=True)
        if not ids: return None, -1.0
        sims = [1.0 - (d*d)/2.0 for d in dists]
        return ids[0], sims[0]

    # ---- lexical helpers ----
    def _faq_bm25_lookup(self, query, min_score=1.5):
        if self.bm25 is None: return None
        toks = self.preprocess(query)
        if not toks: return None
        scores = self.bm25.get_scores(toks)
        idx = int(np.argmax(scores))
        return self.faq_map.get(idx) if scores[idx] >= min_score else None

    def _faq_lexical_lookup(self, query, min_overlap=2):
        if not self.faq_lex: return None
        qn = _norm(query)
        for rec in self.faq_lex:
            if rec["nq"] == qn:
                return rec["ans"]
        qtok = _tokset(qn, FAQ_OVERLAP_STOP)
        best, best_ov = None, 0
        for rec in self.faq_lex:
            ov = len(qtok & rec["toks_overlap"])
            if ov > best_ov:
                best, best_ov = rec, ov
        if best and best_ov >= min_overlap:
            return best["ans"]
        return None

    def _lexical_product_lookup(self, query):
        # early guard: question-like -> let FAQ handle
        s = (query or "").strip()
        if _looks_like_question(s): return None

        qn = _norm(query)
        if not qn: return None

        # exact title fast path
        for rec in self.product_lex:
            if rec["norm_title"] == qn:
                return f"{rec['product_id']} {rec['title']}".strip()

        qtok = _tokset(qn, LEX_STOP)
        best, best_title_ov, best_total = None, 0, 0
        for rec in self.product_lex:
            ot = len(qtok & rec["title_toks"])
            od = len(qtok & rec["desc_toks"])
            total = ot + od
            if (ot, total) > (best_title_ov, best_total):
                best, best_title_ov, best_total = rec, ot, total

        # need at least TWO overlaps with the title tokens
        if best and best_title_ov >= 2:
            return f"{best['product_id']} {best['title']}".strip()
        return None

    def _name_hit(self, query):
        q = str(query or "").lower()
        m = re.search(r"\b(?:pip|pip3|pipx)\s+install\s+([a-z0-9._\-]+)\b", q)
        if not m: return None
        cand = _canon_pkg(m.group(1))
        if cand in self.name_index:
            rec = self.name_index[cand]
            return f"{rec['product_id']} {rec['title']}".strip()
        return None

    def _faq_semantic_ok(self, query, fid, fsim, min_overlap=2):
        if fid is None or fsim < FAQ_SIM_TH: return False
        try:
            cand = self.faq_lex[fid]
        except Exception:
            return False
        qtok = _tokset(query, FAQ_OVERLAP_STOP)
        return len(qtok & cand["toks_overlap"]) >= min_overlap

    # ---- optional classifier gate ----
    def _sigmoid(self, x): return 1.0/(1.0+np.exp(-x))
    def _score_positive(self, model, text):
        if model is None: return None
        try:
            return float(model.predict_proba([text])[0][1])
        except Exception:
            pass
        try:
            margin = float(model.decision_function([text])[0])
            return self._sigmoid(margin)
        except Exception:
            return None

    def is_product_query(self, text, svc_floor=0.55, lr_floor=0.65):
        if not str(text).strip(): return False
        svc_pred = False
        try:
            if self.svc is not None:
                svc_pred = int(self.svc.predict([text])[0]) == 1
        except Exception:
            svc_pred = False
        if not svc_pred: return False
        ps = self._score_positive(self.svc, text)
        if ps is not None and ps < svc_floor: return False
        plr = self._score_positive(self.lr, text)
        if plr is not None and plr < lr_floor: return False
        return True

    # ---- public API ----
    def get_answer(self, query: str) -> str:
        # 0) explicit pip install
        hit = self._name_hit(query)
        if hit: return hit

        # 1) FAQ lexical (BM25, then overlap)
        hit = self._faq_bm25_lookup(query, min_score=1.5)
        if hit: return hit
        hit = self._faq_lexical_lookup(query, min_overlap=2)
        if hit: return hit

        # 2) product lexical (strict)
        hit = self._lexical_product_lookup(query)
        if hit: return hit

        # 3) semantic comparison
        qv = self._encode_query(query)
        if qv is None: return "Sorry, I couldn't understand your question."

        pid, psim = self._best_sim_product(qv, k=3)
        fid, fsim = self._best_sim_faq(qv, k=3)

        if _looks_like_question(query):
            if self._faq_semantic_ok(query, fid, fsim, min_overlap=2) and \
               (fsim + PREF_MARGIN/2 >= psim or psim < PROD_SIM_TH + 0.05):
                return self.faq_map[fid] if fid is not None else "Sorry, I couldn't find an answer."

        if self._faq_semantic_ok(query, fid, fsim, min_overlap=2) and \
           (fsim + PREF_MARGIN >= psim or psim < PROD_SIM_TH):
            return self.faq_map[fid] if fid is not None else "Sorry, I couldn't find an answer."

        if psim >= PROD_SIM_TH and (psim >= fsim + PREF_MARGIN):
            item = self.prod_map[pid]
            return f"{item['product_id']} {item['title']}".strip()

        if self.is_product_query(query):
            if psim >= PROD_SIM_TH - 0.05 and (psim >= fsim + PREF_MARGIN/2):
                item = self.prod_map[pid]
                return f"{item['product_id']} {item['title']}".strip()

        return self.faq_map[fid] if fid is not None and fsim > 0 else "Sorry, I couldn't find an answer."
