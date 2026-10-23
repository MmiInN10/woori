(() => {
  const STORAGE_KEY = "calc-history-v1";
  const MAX_HISTORY = 20;
  const MAX_DIGITS = 12;
  const OP_LABEL = { "+": "+", "-": "−", "*": "×", "/": "÷" };

  const exprEl = document.getElementById("expr");
  const valueEl = document.getElementById("value");
  const keysEl = document.getElementById("keys");
  const listEl = document.getElementById("historyList");
  const emptyEl = document.getElementById("historyEmpty");
  const clearHistoryBtn = document.getElementById("clearHistory");

  // current: 입력 중인 문자열, prev: 앞 피연산자(문자열), op: 연산자
  let state = { current: "0", prev: null, op: null, fresh: true, error: null };
  let history = load();

  function load() {
    try {
      const data = JSON.parse(localStorage.getItem(STORAGE_KEY));
      return Array.isArray(data) ? data.slice(0, MAX_HISTORY) : [];
    } catch {
      return [];
    }
  }

  function save() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
    } catch {
      // 저장이 막힌 환경에서는 메모리에서만 유지한다
    }
  }

  function clean(n) {
    return String(parseFloat(n.toPrecision(12)));
  }

  function fmt(str) {
    if (str.includes("e")) return str;
    const neg = str.startsWith("-");
    const [int, dec] = str.replace("-", "").split(".");
    const withCommas = int.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return (neg ? "-" : "") + withCommas + (dec !== undefined ? "." + dec : "");
  }

  function compute(a, op, b) {
    const x = parseFloat(a), y = parseFloat(b);
    switch (op) {
      case "+": return x + y;
      case "-": return x - y;
      case "*": return x * y;
      case "/": return y === 0 ? null : x / y;
    }
  }

  function render() {
    if (state.error) {
      valueEl.textContent = state.error;
      valueEl.classList.add("is-error");
      exprEl.textContent = "";
    } else {
      valueEl.classList.remove("is-error");
      valueEl.textContent = fmt(state.current);
      exprEl.textContent = state.op ? `${fmt(state.prev)} ${OP_LABEL[state.op]}` : "";
    }
    fitValue();
    keysEl.querySelectorAll("[data-op]").forEach((b) =>
      b.classList.toggle("is-active", !state.error && state.op === b.dataset.op && state.fresh));
  }

  // 자릿수가 많아지면 글자를 줄여 표시 영역 안에 맞춘다
  function fitValue() {
    valueEl.style.fontSize = "";
    if (state.error) return;
    const max = valueEl.parentElement.clientWidth - 40;
    let size = parseFloat(getComputedStyle(valueEl).fontSize);
    while (valueEl.scrollWidth > max && size > 24) {
      size -= 2;
      valueEl.style.fontSize = size + "px";
    }
  }

  function resetAll() {
    state = { current: "0", prev: null, op: null, fresh: true, error: null };
  }

  function digit(d) {
    if (state.error) resetAll();
    if (state.fresh) {
      state.current = d;
      state.fresh = false;
    } else if (state.current.replace(/[-.]/g, "").length < MAX_DIGITS) {
      state.current = state.current === "0" ? d : state.current + d;
    }
  }

  function dot() {
    if (state.error) resetAll();
    if (state.fresh) {
      state.current = "0.";
      state.fresh = false;
    } else if (!state.current.includes(".")) {
      state.current += ".";
    }
  }

  function back() {
    if (state.error) return resetAll();
    if (state.fresh) return;
    state.current = state.current.length > 1 && state.current !== "-0"
      ? state.current.slice(0, -1) : "0";
    if (state.current === "-") state.current = "0";
  }

  function sign() {
    if (state.error || state.current === "0") return;
    state.current = state.current.startsWith("-") ? state.current.slice(1) : "-" + state.current;
  }

  function percent() {
    if (state.error) return;
    state.current = clean(parseFloat(state.current) / 100);
    state.fresh = true;
  }

  function fail(message) {
    resetAll();
    state.error = message;
  }

  function operator(op) {
    if (state.error) return;
    if (state.op && !state.fresh) {
      const result = compute(state.prev, state.op, state.current);
      if (result === null) return fail("0으로 나눌 수 없어요");
      state.prev = clean(result);
      state.current = state.prev;
    } else if (!state.op) {
      state.prev = state.current;
    }
    state.op = op;
    state.fresh = true;
  }

  function equals() {
    if (state.error || !state.op) return;
    const result = compute(state.prev, state.op, state.current);
    if (result === null) return fail("0으로 나눌 수 없어요");
    const out = clean(result);
    addHistory(`${fmt(state.prev)} ${OP_LABEL[state.op]} ${fmt(state.current)}`, out);
    state = { current: out, prev: null, op: null, fresh: true, error: null };
  }

  function addHistory(expr, result) {
    history.unshift({ expr, result });
    history = history.slice(0, MAX_HISTORY);
    save();
    renderHistory();
  }

  function renderHistory() {
    listEl.textContent = "";
    history.forEach((item, i) => {
      const li = document.createElement("li");
      li.className = "history__item";
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "history__btn";
      btn.dataset.index = i;
      btn.setAttribute("aria-label", `${item.expr} = ${fmt(item.result)}, 결과 불러오기`);
      const e = document.createElement("span");
      e.className = "history__expr";
      e.textContent = item.expr + " =";
      const r = document.createElement("span");
      r.className = "history__result";
      r.textContent = fmt(item.result);
      btn.append(e, r);
      li.append(btn);
      listEl.append(li);
    });
    emptyEl.hidden = history.length > 0;
    clearHistoryBtn.hidden = history.length === 0;
  }

  function act(action) {
    switch (action) {
      case "clear": resetAll(); break;
      case "back": back(); break;
      case "sign": sign(); break;
      case "percent": percent(); break;
      case "dot": dot(); break;
      case "equals": equals(); break;
    }
  }

  keysEl.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button");
    if (!btn) return;
    if (btn.dataset.digit) digit(btn.dataset.digit);
    else if (btn.dataset.op) operator(btn.dataset.op);
    else if (btn.dataset.action) act(btn.dataset.action);
    render();
  });

  listEl.addEventListener("click", (ev) => {
    const btn = ev.target.closest(".history__btn");
    if (!btn) return;
    state = { current: history[btn.dataset.index].result, prev: null, op: null, fresh: true, error: null };
    render();
  });

  clearHistoryBtn.addEventListener("click", () => {
    history = [];
    save();
    renderHistory();
  });

  // 키보드 입력: 눌린 키에 해당하는 버튼을 찾아 눌림 효과를 준다
  const KEY_MAP = { Enter: "equals", "=": "equals", Backspace: "back", Escape: "clear", "%": "percent", ".": "dot", ",": "dot" };

  document.addEventListener("keydown", (ev) => {
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const k = ev.key;
    // 기록·네비 버튼에 포커스가 있을 때 Enter는 그 버튼의 기본 동작에 맡긴다
    if (k === "Enter" && ev.target.closest?.("button, a") && !keysEl.contains(ev.target)) return;
    let selector = null;
    if (/^[0-9]$/.test(k)) selector = `[data-digit="${k}"]`;
    else if (OP_LABEL[k]) selector = `[data-op="${k}"]`;
    else if (KEY_MAP[k]) selector = `[data-action="${KEY_MAP[k]}"]`;
    if (!selector) return;

    // 포커스된 버튼에서 Enter를 누르면 그 버튼이 눌리므로, 중복 입력을 막는다
    ev.preventDefault();
    const btn = keysEl.querySelector(selector);
    btn.classList.add("is-pressed");
    setTimeout(() => btn.classList.remove("is-pressed"), 110);
    btn.click();
  });

  window.addEventListener("resize", fitValue);

  renderHistory();
  render();
})();
