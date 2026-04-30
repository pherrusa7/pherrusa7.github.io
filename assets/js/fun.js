(() => {
  const enabledKey = "pedro-fun-text";
  const settingsKey = "pedro-fun-settings";
  const targets = "main p, main li, main h1, main h2, main h3";
  const skipTags = new Set(["SCRIPT", "STYLE", "CODE", "PRE", "IMG", "BUTTON", "INPUT", "LABEL"]);
  const defaults = {
    force: 2.8,
    radius: 34,
    motion: 0.04,
    return: 0.16,
    settle: 0.78,
    weight: 50,
  };
  const controls = [
    ["force", "how hard letters separate", 1, 8, 0.1, "q"],
    ["radius", "how close the mouse needs to be", 18, 80, 1, "w"],
    ["motion", "how much swipe speed matters", 0, 0.12, 0.005, "e"],
    ["return", "how strongly text pulls itself back", 0.06, 0.3, 0.01, "r"],
    ["settle", "how quickly movement fades", 0.55, 0.92, 0.01, "t"],
    ["weight", "regular text thickness", 50, 700, 130, "y"],
  ];
  const controlKeys = new Map(controls.map((control) => [control[5], control[0]]));

  let settings = loadSettings();
  let chars = [];
  let enabled = false;
  let pointer = { x: -9999, y: -9999, px: -9999, py: -9999, vx: 0, vy: 0 };
  let raf = 0;
  let selected = controls[0][0];
  const inputs = new Map();
  const rows = new Map();

  const toggle = makeToggle();
  const panel = makePanel();
  applySettings();

  function loadSettings() {
    try {
      return { ...defaults, ...JSON.parse(localStorage.getItem(settingsKey) || "{}") };
    } catch (_) {
      return { ...defaults };
    }
  }

  function saveSettings() {
    applySettings();
    try { localStorage.setItem(settingsKey, JSON.stringify(settings)); } catch (_) {}
  }

  function applySettings() {
    document.documentElement.style.setProperty("--body-weight", String(settings.weight));
    const ink = 18 + ((settings.weight - 50) / 650) * 82;
    document.documentElement.style.setProperty("--body-ink", `${Math.round(ink)}%`);
  }

  function makeToggle() {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "fun-toggle";
    button.setAttribute("aria-pressed", "false");
    button.innerHTML = "Fun off <kbd>f</kbd>";
    button.addEventListener("click", () => setEnabled(!enabled));
    document.body.appendChild(button);
    return button;
  }

  function makePanel() {
    const panelEl = document.createElement("div");
    panelEl.className = "fun-panel";
    panelEl.hidden = true;

    for (const [key, title, min, max, step, shortcut] of controls) {
      const row = document.createElement("label");
      row.className = "fun-control";
      row.title = title;

      row.dataset.control = key;

      const name = document.createElement("span");
      name.innerHTML = `<kbd>${shortcut}</kbd>${key}`;

      const input = document.createElement("input");
      input.type = "range";
      input.min = String(min);
      input.max = String(max);
      input.step = String(step);
      input.value = String(settings[key]);
      input.addEventListener("input", () => {
        selected = key;
        syncSelected();
        settings[key] = Number(input.value);
        saveSettings();
      });

      inputs.set(key, input);
      rows.set(key, row);
      row.append(name, input);
      panelEl.appendChild(row);
    }

    const hint = document.createElement("p");
    hint.className = "fun-hint";
    hint.textContent = "hover over text";
    panelEl.appendChild(hint);

    const legend = document.createElement("p");
    legend.className = "fun-legend";
    legend.innerHTML = "<span><kbd>q</kbd><kbd>w</kbd><kbd>e</kbd><kbd>r</kbd><kbd>t</kbd><kbd>y</kbd> select</span><span><kbd>a</kbd>/<kbd>s</kbd> tune · <kbd>f</kbd> off</span>";
    panelEl.appendChild(legend);

    const reset = document.createElement("button");
    reset.type = "button";
    reset.className = "fun-reset";
    reset.textContent = "reset";
    reset.addEventListener("click", () => {
      settings = { ...defaults };
      for (const [key, input] of inputs) {
        input.value = String(settings[key]);
      }
      saveSettings();
    });
    panelEl.appendChild(reset);

    document.body.appendChild(panelEl);
    syncSelected();
    return panelEl;
  }

  function syncSelected() {
    for (const [key, row] of rows) {
      row.classList.toggle("is-selected", key === selected);
    }
  }

  function nudgeSelected(direction) {
    const control = controls.find(([key]) => key === selected);
    if (!control) return;
    const [key, , min, max] = control;
    const amount = (max - min) / 5;
    const next = Math.min(max, Math.max(min, settings[key] + direction * amount));
    settings[key] = Number(next.toFixed(3));
    const input = inputs.get(key);
    if (input) input.value = String(settings[key]);
    saveSettings();
  }

  function onKey(event) {
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    const tag = event.target && event.target.tagName;
    if (tag === "TEXTAREA" || tag === "SELECT" || event.target?.isContentEditable) return;
    const key = event.key.toLowerCase();
    if (key === "f") {
      setEnabled(!enabled);
      event.preventDefault();
      return;
    }
    if (!enabled) return;
    if (controlKeys.has(key)) {
      selected = controlKeys.get(key);
      syncSelected();
      event.preventDefault();
      return;
    }
    if (key === "a" || key === "s") {
      nudgeSelected(key === "s" ? 1 : -1);
      event.preventDefault();
    }
  }

  function wrapText(node) {
    if (!node.nodeValue || !node.nodeValue.trim()) return;
    const frag = document.createDocumentFragment();
    for (const ch of node.nodeValue) {
      if (ch === " ") {
        frag.appendChild(document.createTextNode(" "));
        continue;
      }
      const span = document.createElement("span");
      span.className = "fun-char";
      span.textContent = ch;
      span._fx = 0;
      span._fy = 0;
      span._vx = 0;
      span._vy = 0;
      frag.appendChild(span);
      chars.push(span);
    }
    node.parentNode.replaceChild(frag, node);
  }

  function prepare() {
    chars = [];
    document.querySelectorAll(targets).forEach((root) => {
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
        acceptNode(node) {
          const parent = node.parentElement;
          if (!parent || skipTags.has(parent.tagName) || parent.closest(".fun-toggle, .fun-panel")) {
            return NodeFilter.FILTER_REJECT;
          }
          return node.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
        },
      });
      const textNodes = [];
      while (walker.nextNode()) textNodes.push(walker.currentNode);
      textNodes.forEach(wrapText);
    });
  }

  function setEnabled(next) {
    enabled = next;
    document.body.classList.toggle("fun-mode", enabled);
    toggle.innerHTML = enabled ? "Fun on <kbd>f</kbd>" : "Fun off <kbd>f</kbd>";
    toggle.setAttribute("aria-pressed", String(enabled));
    panel.hidden = !enabled;
    try { localStorage.setItem(enabledKey, enabled ? "1" : "0"); } catch (_) {}
    if (!enabled) {
      for (const el of chars) {
        el._fx = el._fy = el._vx = el._vy = 0;
        el.style.transform = "";
      }
    }
    if (enabled && !raf) tick();
  }

  function onMove(event) {
    if (pointer.px < 0) {
      pointer.px = event.clientX;
      pointer.py = event.clientY;
    }
    pointer.vx = event.clientX - pointer.px;
    pointer.vy = event.clientY - pointer.py;
    pointer.px = pointer.x = event.clientX;
    pointer.py = pointer.y = event.clientY;
  }

  function tick() {
    if (!enabled) {
      raf = 0;
      return;
    }
    raf = requestAnimationFrame(tick);

    for (const el of chars) {
      const box = el.getBoundingClientRect();
      const cx = box.left + box.width / 2;
      const cy = box.top + box.height / 2;
      const dx = cx - pointer.x;
      const dy = cy - pointer.y;
      const dist = Math.hypot(dx, dy) || 1;

      if (dist < settings.radius) {
        const force = (1 - dist / settings.radius) * settings.force;
        el._vx += (dx / dist) * force + pointer.vx * settings.motion;
        el._vy += (dy / dist) * force + pointer.vy * settings.motion;
      }

      el._vx += -el._fx * settings.return;
      el._vy += -el._fy * settings.return;
      el._vx *= settings.settle;
      el._vy *= settings.settle;
      el._fx += el._vx;
      el._fy += el._vy;

      if (Math.abs(el._fx) + Math.abs(el._fy) < 0.02) {
        el._fx = 0;
        el._fy = 0;
      }
      el.style.transform = `translate(${el._fx.toFixed(2)}px, ${el._fy.toFixed(2)}px)`;
    }
  }

  prepare();
  window.addEventListener("mousemove", onMove, { passive: true });
  window.addEventListener("keydown", onKey);
  let saved = false;
  try { saved = localStorage.getItem(enabledKey) === "1"; } catch (_) {}
  setEnabled(saved);
})();
