import math
import re

import streamlit as st

st.set_page_config(page_title="Simple Calc", page_icon="🧮", layout="centered")

# 계산에 허용할 함수들 (sin/cos/tan은 degree 단위, 원본과 동일)
SAFE_NAMES = {
    "__builtins__": {},
    "pi": math.pi,
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "sqrt": math.sqrt,
    "root": lambda n, x: x ** (1 / n),  # n제곱근: root(n,x)
    "abs": abs,
}

# 전역변수 역할: session_state (rerun 되어도 값이 유지됨)
if "expr" not in st.session_state:
    st.session_state.expr = "0"


# ── @st.cache_data ─────────────────────────────────────────────
# 같은 수식이면 다시 계산하지 않고 캐시에서 결과를 꺼내 쓴다.
@st.cache_data
def calculate(expr: str) -> str:
    try:
        expr = expr.replace("π", "pi").replace("^", "**").replace("√", "sqrt")
        expr = re.sub(r"(\d|\))(pi|\(|sin|cos|tan|sqrt|root|abs)", r"\1*\2", expr)
        open_b, close_b = expr.count("("), expr.count(")")
        expr += ")" * max(0, open_b - close_b)
        res = eval(expr, SAFE_NAMES)  # 버튼 입력만 들어오고 builtins는 막아둠
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        return str(res)
    except Exception:
        return "0"


def press(token):
    expr = st.session_state.expr
    st.session_state.expr = token if expr == "0" else expr + token


def delete():
    expr = st.session_state.expr
    st.session_state.expr = "0" if len(expr) <= 1 else expr[:-1]


def clear():
    st.session_state.expr = "0"


def run():
    st.session_state.expr = calculate(st.session_state.expr)


# (표시 글자, 입력될 값)
ROWS = [
    [("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("π", "π"), ("abs", "abs("), ("ⁿ√", "root(")],
    [("√", "√("), ("x²", "^2"), ("xⁿ", "^"), ("(", "("), (")", ")"), (",", ",")],
    [("7", "7"), ("8", "8"), ("9", "9"), ("÷", "/"), ("DEL", None), ("C", None)],
    [("4", "4"), ("5", "5"), ("6", "6"), ("×", "*")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("−", "-")],
    [("0", "0"), (".", "."), ("=", None), ("+", "+")],
]


# ── @st.fragment ───────────────────────────────────────────────
# 버튼을 누를 때 이 함수 안쪽만 다시 실행된다. (페이지 전체 rerun 방지)
@st.fragment
def calculator():
    st.code(st.session_state.expr, language=None)

    for r, row in enumerate(ROWS):
        cols = st.columns(len(row))
        for c, (label, value) in enumerate(row):
            key = f"btn_{r}_{c}"
            if label == "DEL":
                cols[c].button(label, key=key, on_click=delete, use_container_width=True)
            elif label == "C":
                cols[c].button(label, key=key, on_click=clear, use_container_width=True)
            elif label == "=":
                cols[c].button(label, key=key, on_click=run, use_container_width=True, type="primary")
            else:
                cols[c].button(label, key=key, on_click=press, args=(value,), use_container_width=True)


st.title("🧮 Simple Calc")
calculator()
st.caption("sin/cos/tan은 각도(degree) 기준 · n제곱근은 root(n,x) 형태 (예: root(3,8) = 2)")
