const OP_SYMBOLS = { "+": "+", "-": "−", "*": "×", "/": "÷" };
const MAX_DIGITS = 15;
const MSG_DIV_ZERO = "0으로 나눌 수 없어요";
const MSG_OVERFLOW = "계산할 수 없는 값이에요";

// tokens는 완성된 부분 [숫자, 연산자, 숫자, ...], cur는 입력 중이거나 방금 나온 숫자.
const state = {
  tokens: [],
  cur: "0",
  awaiting: false, // 연산자를 막 눌러서 다음 숫자를 기다리는 중
  done: false, // = 직후, cur가 결과
  expr: "",
  error: false,
  errorMsg: "",
};

const expressionEl = document.getElementById("expression");
const resultEl = document.getElementById("result");
const keysEl = document.getElementById("keys");
const keyButtons = [...keysEl.querySelectorAll("button")];

function reset() {
  state.tokens = [];
  state.cur = "0";
  state.awaiting = false;
  state.done = false;
  state.expr = "";
  state.error = false;
  state.errorMsg = "";
}

// 결과 숫자를 12자리 유효숫자로 반올림해서 0.1+0.2 같은 오차를 감춘다.
function format(n) {
  const rounded = Number(n.toPrecision(12));
  if (rounded === 0) return "0";
  const abs = Math.abs(rounded);
  if (abs >= 1e15 || abs < 1e-6) return rounded.toExponential();
  return String(rounded);
}

// 곱셈/나눗셈을 먼저 처리하고 나머지를 왼쪽부터 더하고 뺀다. 0으로 나누면 null.
function calculate(tokens) {
  const nums = [Number(tokens[0])];
  const ops = [];
  for (let i = 1; i < tokens.length; i += 2) {
    const op = tokens[i];
    const n = Number(tokens[i + 1]);
    if (op === "*" || op === "/") {
      if (op === "/" && n === 0) return null;
      const a = nums.pop();
      nums.push(op === "*" ? a * n : a / n);
    } else {
      ops.push(op);
      nums.push(n);
    }
  }
  return ops.reduce((acc, op, i) => (op === "+" ? acc + nums[i + 1] : acc - nums[i + 1]), nums[0]);
}

function exprText(tokens) {
  return tokens.map((t, i) => (i % 2 ? OP_SYMBOLS[t] : t)).join(" ");
}

function digitCount(s) {
  return s.replace(/[-.]/g, "").length;
}

// = 직후이거나 연산자 직후라면 새 숫자를 받을 수 있게 정리한다.
function prepareNumberEntry() {
  if (state.error) reset();
  if (state.done) {
    state.tokens = [];
    state.cur = "0";
    state.done = false;
    state.expr = "";
  }
  if (state.awaiting) {
    state.cur = "0";
    state.awaiting = false;
  }
}

function inputDigit(d) {
  prepareNumberEntry();
  if (digitCount(state.cur) >= MAX_DIGITS) return;
  const neg = state.cur.startsWith("-");
  const body = neg ? state.cur.slice(1) : state.cur;
  state.cur = (neg ? "-" : "") + (body === "0" ? d : body + d);
}

function inputDot() {
  prepareNumberEntry();
  if (state.cur.includes(".") || digitCount(state.cur) >= MAX_DIGITS) return;
  state.cur += ".";
}

function inputOp(op) {
  if (state.error) reset();
  if (state.done) {
    state.tokens = [];
    state.done = false;
    state.expr = "";
  }
  if (state.awaiting) {
    state.tokens[state.tokens.length - 1] = op;
    return;
  }
  state.tokens.push(state.cur, op);
  state.awaiting = true;
}

function evaluate() {
  if (state.error || state.done) return;
  const tokens = state.awaiting ? state.tokens.slice(0, -1) : [...state.tokens, state.cur];
  if (tokens.length < 3) return;

  const result = calculate(tokens);
  state.expr = exprText(tokens) + " =";
  state.tokens = [];
  state.awaiting = false;
  state.done = true;

  if (result === null || !Number.isFinite(result)) {
    state.error = true;
    state.errorMsg = result === null ? MSG_DIV_ZERO : MSG_OVERFLOW;
    state.cur = "0";
  } else {
    state.cur = format(result);
  }
}

function percent() {
  if (state.error) reset();
  if (state.awaiting) return;
  state.cur = format(Number(state.cur) / 100);
}

function negate() {
  if (state.error) reset();
  if (state.awaiting) {
    state.cur = "-0";
    state.awaiting = false;
    return;
  }
  if (state.cur.startsWith("-")) state.cur = state.cur.slice(1);
  else state.cur = "-" + state.cur;
}

function backspace() {
  if (state.error) {
    reset();
    return;
  }
  if (state.done || state.awaiting) return;
  state.cur = state.cur.slice(0, -1);
  if (state.cur === "" || state.cur === "-") state.cur = "0";
}

function render() {
  let expr = state.expr;
  if (!state.done && state.tokens.length) {
    expr = exprText(state.tokens) + (state.awaiting ? "" : " " + state.cur);
  }
  expressionEl.textContent = expr;
  expressionEl.scrollLeft = expressionEl.scrollWidth;

  const text = state.error ? state.errorMsg : state.cur;
  resultEl.textContent = text;
  resultEl.classList.toggle("is-error", state.error);
  resultEl.dataset.size = text.length > 14 ? "xs" : text.length > 10 ? "s" : "";
}

function press(action, value) {
  switch (action) {
    case "digit": inputDigit(value); break;
    case "dot": inputDot(); break;
    case "op": inputOp(value); break;
    case "equals": evaluate(); break;
    case "percent": percent(); break;
    case "negate": negate(); break;
    case "backspace": backspace(); break;
    case "clear": reset(); break;
  }
  render();
}

function spark(button) {
  if (!button) return;
  button.classList.remove("spark");
  void button.offsetWidth; // 애니메이션을 처음부터 다시 재생
  button.classList.add("spark");
}

keysEl.addEventListener("click", (e) => {
  const button = e.target.closest("button[data-action]");
  if (!button) return;
  spark(button);
  press(button.dataset.action, button.dataset.value);
});

function keyToCommand(key) {
  if (/^[0-9]$/.test(key)) return ["digit", key];
  if (key === "." || key === ",") return ["dot"];
  if (key === "+" || key === "-") return ["op", key];
  if (key === "*" || key === "x" || key === "X") return ["op", "*"];
  if (key === "/") return ["op", "/"];
  if (key === "Enter" || key === "=") return ["equals"];
  if (key === "Backspace") return ["backspace"];
  if (key === "Escape" || key === "Delete") return ["clear"];
  if (key === "%") return ["percent"];
  return null;
}

document.addEventListener("keydown", (e) => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  if (e.target.closest("#theme-toggle")) return;
  const command = keyToCommand(e.key);
  if (!command) return;
  e.preventDefault(); // 포커스된 버튼이 Enter로 한 번 더 눌리는 것을 막는다
  const [action, value] = command;
  spark(keyButtons.find((b) => b.dataset.action === action && b.dataset.value === value));
  press(action, value);
});

const root = document.documentElement;
const themeToggle = document.getElementById("theme-toggle");

function applyTheme(theme) {
  root.dataset.theme = theme;
  themeToggle.textContent = theme === "dark" ? "☀️" : "🌙";
  themeToggle.setAttribute("aria-label", theme === "dark" ? "라이트 모드로 전환" : "다크 모드로 전환");
}

themeToggle.addEventListener("click", () => {
  const next = root.dataset.theme === "dark" ? "light" : "dark";
  applyTheme(next);
  try {
    localStorage.setItem("theme", next);
  } catch (e) {
    // 저장소를 쓸 수 없어도 전환 자체는 동작한다.
  }
});

applyTheme(root.dataset.theme === "dark" ? "dark" : "light");
render();
