const currentEl = document.getElementById('current');
const expressionEl = document.getElementById('expression');
const opButtons = document.querySelectorAll('[data-op]');

const MAX_DIGITS = 12;

let current = '0';     // 현재 입력 중인 값 (문자열)
let previous = null;   // 이전 값 (숫자)
let operator = null;   // 대기 중인 연산자
let fresh = false;     // true면 다음 숫자 입력 시 current를 새로 시작
let error = false;

function compute(a, op, b) {
  switch (op) {
    case '+': return a + b;
    case '−': return a - b;
    case '×': return a * b;
    case '÷': return b === 0 ? NaN : a / b;
  }
  return b;
}

// 부동소수점 오차 제거 (0.1 + 0.2 → 0.3)
function format(n) {
  if (!Number.isFinite(n)) return '오류';
  return String(parseFloat(n.toPrecision(12)));
}

function render() {
  if (currentEl.textContent !== current) popDisplay();
  currentEl.textContent = current;
  expressionEl.textContent =
    previous !== null && operator ? `${format(previous)} ${operator}` : '';

  const len = current.length;
  currentEl.style.fontSize = len > 12 ? '1.6rem' : len > 9 ? '2.1rem' : '';

  opButtons.forEach(b =>
    b.classList.toggle('selected', fresh && b.dataset.op === operator));
}

// ---- 폭죽 ----
const canvas = document.getElementById('fireworks');
const ctx = canvas.getContext('2d');
const COLORS = ['#ff4d6d', '#ffd166', '#4cc9f0', '#80ed99', '#b388ff', '#ff9f1c'];
let particles = [];
let animating = false;

function resizeCanvas() {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = innerWidth * dpr;
  canvas.height = innerHeight * dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}
resizeCanvas();
addEventListener('resize', resizeCanvas);

function burst(x, y) {
  const count = 40;
  const color = COLORS[Math.floor(Math.random() * COLORS.length)];
  for (let i = 0; i < count; i++) {
    const angle = (Math.PI * 2 * i) / count + Math.random() * 0.2;
    const speed = 2 + Math.random() * 4;
    particles.push({
      x, y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      life: 1,
      decay: 0.012 + Math.random() * 0.012,
      color: Math.random() < 0.7 ? color : COLORS[Math.floor(Math.random() * COLORS.length)],
    });
  }
}

function fireworks() {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  // 계산기 주변 여러 곳에서 시차를 두고 터뜨림
  for (let i = 0; i < 5; i++) {
    setTimeout(() => {
      burst(innerWidth * (0.2 + Math.random() * 0.6),
            innerHeight * (0.15 + Math.random() * 0.45));
      if (!animating) { animating = true; requestAnimationFrame(tick); }
    }, i * 180);
  }
}

function tick() {
  ctx.clearRect(0, 0, innerWidth, innerHeight);
  particles = particles.filter(p => p.life > 0);
  for (const p of particles) {
    p.x += p.vx;
    p.y += p.vy;
    p.vx *= 0.98;
    p.vy = p.vy * 0.98 + 0.06; // 중력
    p.life -= p.decay;
    ctx.globalAlpha = Math.max(p.life, 0);
    ctx.fillStyle = p.color;
    ctx.beginPath();
    ctx.arc(p.x, p.y, 2.5, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;
  if (particles.length) requestAnimationFrame(tick);
  else animating = false;
}

function addRipple(btn, e) {
  const rect = btn.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height) * 2;
  // 키보드로 눌렀을 때(clientX가 0)는 버튼 중앙에서 시작
  const x = e.clientX ? e.clientX - rect.left : rect.width / 2;
  const y = e.clientY ? e.clientY - rect.top : rect.height / 2;
  const r = document.createElement('span');
  r.className = 'ripple';
  r.style.width = r.style.height = size + 'px';
  r.style.left = x - size / 2 + 'px';
  r.style.top = y - size / 2 + 'px';
  btn.appendChild(r);
  r.addEventListener('animationend', () => r.remove());
}

function popDisplay() {
  currentEl.classList.remove('pop');
  void currentEl.offsetWidth; // 애니메이션 재시작
  currentEl.classList.add('pop');
}

function reset() {
  current = '0';
  previous = null;
  operator = null;
  fresh = false;
  error = false;
}

function inputDigit(d) {
  if (error) reset();
  if (fresh) { current = '0'; fresh = false; }
  if (current.replace(/[-.]/g, '').length >= MAX_DIGITS) return;
  current = current === '0' ? d : current === '-0' ? '-' + d : current + d;
}

function inputDecimal() {
  if (error) reset();
  if (fresh) { current = '0'; fresh = false; }
  if (!current.includes('.')) current += '.';
}

function chooseOperator(op) {
  if (error) return;
  if (operator && !fresh) {
    // 연속 입력: 입력 순서대로 먼저 계산
    const result = compute(previous, operator, parseFloat(current));
    if (Number.isNaN(result)) return showError();
    previous = result;
    current = format(result);
  } else if (!operator) {
    previous = parseFloat(current);
  }
  operator = op;
  fresh = true;
}

function equals() {
  if (error || !operator) return;
  const result = compute(previous, operator, parseFloat(current));
  if (Number.isNaN(result)) return showError();
  current = format(result);
  previous = null;
  operator = null;
  fresh = true;
  fireworks();
}

function showError() {
  reset();
  current = '오류';
  error = true;
}

function backspace() {
  if (error) return reset();
  if (fresh) return;
  current = current.length > 1 && !(current.length === 2 && current[0] === '-')
    ? current.slice(0, -1)
    : '0';
}

function negate() {
  if (error || current === '0') return;
  current = current.startsWith('-') ? current.slice(1) : '-' + current;
}

function percent() {
  if (error) return;
  current = format(parseFloat(current) / 100);
  fresh = false;
}

function handleAction(action) {
  switch (action) {
    case 'clear': reset(); break;
    case 'backspace': backspace(); break;
    case 'percent': percent(); break;
    case 'negate': negate(); break;
    case 'decimal': inputDecimal(); break;
    case 'equals': equals(); break;
  }
}

document.querySelector('.keys').addEventListener('click', e => {
  const btn = e.target.closest('button');
  if (!btn) return;
  addRipple(btn, e);
  if (btn.dataset.digit !== undefined) inputDigit(btn.dataset.digit);
  else if (btn.dataset.op) chooseOperator(btn.dataset.op);
  else handleAction(btn.dataset.action);
  render();
});

const KEY_OPS = { '+': '+', '-': '−', '*': '×', '/': '÷' };

document.addEventListener('keydown', e => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  const k = e.key;
  if (/^[0-9]$/.test(k)) inputDigit(k);
  else if (k in KEY_OPS) { e.preventDefault(); chooseOperator(KEY_OPS[k]); }
  else if (k === '.' || k === ',') inputDecimal();
  else if (k === '%') percent();
  else if (k === 'Enter' || k === '=') { e.preventDefault(); equals(); }
  else if (k === 'Backspace') backspace();
  else if (k === 'Escape') reset();
  else return;
  render();
});

render();
