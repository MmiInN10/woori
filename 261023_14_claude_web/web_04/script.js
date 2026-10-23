const MAX_DIGITS = 12;
const MAX_HISTORY = 20;

const state = {
  current: "0",
  previous: null,
  operator: null,
  justEvaluated: false,
  error: false,
};
const history = [];

const resultEl = document.getElementById("result");
const expressionEl = document.getElementById("expression");
const historyList = document.getElementById("historyList");

function format(str) {
  if (str === "" || str === "-") return "0";
  const negative = str.startsWith("-");
  const [int, frac] = str.replace("-", "").split(".");
  const grouped = int.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return (negative ? "-" : "") + grouped + (frac !== undefined ? "." + frac : "");
}

function render() {
  resultEl.classList.remove("small", "tiny", "error");
  if (state.error) {
    resultEl.textContent = "0으로 나눌 수 없습니다";
    resultEl.classList.add("error");
    expressionEl.textContent = "";
    return;
  }
  const text = format(state.current === "" ? state.previous : state.current);
  resultEl.textContent = text;
  if (text.length > 14) resultEl.classList.add("tiny");
  else if (text.length > 9) resultEl.classList.add("small");
  expressionEl.textContent =
    state.previous !== null && state.operator
      ? `${format(state.previous)} ${state.operator}`
      : "";
}

function compute(a, b, op) {
  const x = parseFloat(a);
  const y = parseFloat(b);
  switch (op) {
    case "+": return x + y;
    case "−": return x - y;
    case "×": return x * y;
    case "÷": return y === 0 ? null : x / y;
  }
  return y;
}

// 0.1 + 0.2 같은 부동소수 오차를 정리한다.
function clean(n) {
  if (!isFinite(n)) return "0";
  let s = String(parseFloat(n.toPrecision(MAX_DIGITS)));
  if (s.includes("e")) s = n.toExponential(6);
  return s;
}

function reset() {
  state.current = "0";
  state.previous = null;
  state.operator = null;
  state.justEvaluated = false;
  state.error = false;
}

function inputDigit(d) {
  if (state.error) reset();
  if (state.justEvaluated) {
    state.current = "0";
    state.justEvaluated = false;
  }
  const digits = state.current.replace(/[-.]/g, "").length;
  if (digits >= MAX_DIGITS) return;
  state.current = state.current === "0" ? d : state.current === "-0" ? "-" + d : state.current + d;
}

function inputDecimal() {
  if (state.error) reset();
  if (state.justEvaluated) {
    state.current = "0";
    state.justEvaluated = false;
  }
  if (!state.current.includes(".")) state.current += ".";
}

function inputOperator(op) {
  if (state.error) return;
  // 연산자를 연달아 누르면 앞의 연산자를 바꾼다.
  if (state.operator && state.previous !== null && state.current === "" ) {
    state.operator = op;
    return;
  }
  if (state.operator && state.previous !== null && !state.justEvaluated) {
    const r = compute(state.previous, state.current, state.operator);
    if (r === null) { fail(); return; }
    state.previous = clean(r);
  } else {
    state.previous = state.current;
  }
  state.operator = op;
  state.justEvaluated = false;
  state.current = "";
}

function fail() {
  state.error = true;
  state.previous = null;
  state.operator = null;
  state.current = "0";
}

function equals() {
  if (state.error || !state.operator || state.previous === null) return;
  const right = state.current === "" ? state.previous : state.current;
  const r = compute(state.previous, right, state.operator);
  if (r === null) { fail(); return; }
  const answer = clean(r);
  addHistory(`${format(state.previous)} ${state.operator} ${format(right)}`, answer);
  state.current = answer;
  state.previous = null;
  state.operator = null;
  state.justEvaluated = true;
}

function backspace() {
  if (state.error) { reset(); return; }
  if (state.justEvaluated) return;
  const next = state.current.slice(0, -1);
  state.current = next === "" || next === "-" ? (state.operator ? "" : "0") : next;
}

function toggleSign() {
  if (state.error || state.current === "" ) return;
  if (state.current === "0") return;
  state.current = state.current.startsWith("-") ? state.current.slice(1) : "-" + state.current;
}

function percent() {
  if (state.error || state.current === "") return;
  state.current = clean(parseFloat(state.current) / 100);
  state.justEvaluated = false;
}

function addHistory(equation, answer) {
  history.unshift({ equation, answer });
  if (history.length > MAX_HISTORY) history.pop();
  renderHistory();
}

function renderHistory() {
  historyList.textContent = "";
  if (history.length === 0) {
    const li = document.createElement("li");
    li.className = "history-empty";
    li.textContent = "계산하면 여기에 쌓입니다.";
    historyList.append(li);
    return;
  }
  history.forEach((h) => {
    const li = document.createElement("li");
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "history-item";
    btn.setAttribute("aria-label", `${h.equation} = ${h.answer}, 누르면 불러오기`);
    btn.innerHTML = '<span class="eq"></span><span class="val"></span>';
    btn.querySelector(".eq").textContent = h.equation + " =";
    btn.querySelector(".val").textContent = format(h.answer);
    btn.addEventListener("click", () => {
      reset();
      state.current = h.answer;
      state.justEvaluated = true;
      render();
    });
    li.append(btn);
    historyList.append(li);
  });
}

function press(action, value) {
  switch (action) {
    case "digit": inputDigit(value); break;
    case "decimal": inputDecimal(); break;
    case "operator": inputOperator(value); break;
    case "equals": equals(); break;
    case "clear": reset(); break;
    case "backspace": backspace(); break;
    case "sign": toggleSign(); break;
    case "percent": percent(); break;
  }
  render();
}

document.getElementById("keys").addEventListener("click", (e) => {
  const btn = e.target.closest(".key");
  if (btn) press(btn.dataset.action, btn.dataset.value);
});

document.getElementById("historyClear").addEventListener("click", () => {
  history.length = 0;
  renderHistory();
});

const keyMap = {
  "+": ["operator", "+"],
  "-": ["operator", "−"],
  "*": ["operator", "×"],
  "x": ["operator", "×"],
  "/": ["operator", "÷"],
  ".": ["decimal"],
  ",": ["decimal"],
  "=": ["equals"],
  "Enter": ["equals"],
  "Backspace": ["backspace"],
  "Escape": ["clear"],
  "%": ["percent"],
};

document.addEventListener("keydown", (e) => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  // 기록 항목에 포커스가 있을 때 Enter는 그 항목을 여는 데 쓴다.
  if (e.target.closest && e.target.closest(".history-item, .history-clear")) return;

  let entry = null;
  if (/^[0-9]$/.test(e.key)) entry = ["digit", e.key];
  else if (keyMap[e.key]) entry = keyMap[e.key];
  if (!entry) return;

  e.preventDefault();
  press(entry[0], entry[1]);

  // 화면 키도 같이 눌린 모양을 보여 준다.
  const sel = entry[1] !== undefined
    ? `.key[data-action="${entry[0]}"][data-value="${entry[1]}"]`
    : `.key[data-action="${entry[0]}"]`;
  const keyEl = document.querySelector(sel);
  if (keyEl) {
    keyEl.classList.add("pressed");
    setTimeout(() => keyEl.classList.remove("pressed"), 100);
  }
});

render();
