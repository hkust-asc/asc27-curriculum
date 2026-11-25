(function () {
  const navItems = [
    { href: "index.html", label: "Home", subtitle: "Knowledge graph, 24-week roadmap, and ASC27 timeline" },
    { href: "stage1-foundations.html", label: "Stage 1: Physics", subtitle: "Cache locality, Amdahl scaling, and Roofline model" },
    { href: "stage2-parallelism.html", label: "Stage 2: Parallel", subtitle: "False sharing, MPI 2D halo, and CUDA GEMM tiling" },
    { href: "stage3-ai-systems.html", label: "Stage 3: AI & Porting", subtitle: "VRAM budget, Ring All-Reduce, KV cache, and AMSS-NCKU" },
    { href: "stage4-asc-sprint.html", label: "Stage 4: ASC Sprint", subtitle: "HPL tuning, power wall DVFS, and QiboTN qubit memory" },
    { href: "past-problems.html", label: "Past Problems", subtitle: "10 past ASC problems (C01 to C10) mapped to labs" }
  ];

  const courseTree = [
    {
      title: "Overview",
      color: "#171717",
      items: [
        { id: "kg", href: "index.html#knowledge-graph", label: "Knowledge Graph" },
        { id: "roadmap", href: "index.html#roadmap", label: "24-Week Roadmap" },
        { id: "timeline", href: "index.html#timeline", label: "ASC27 Timeline" }
      ]
    },
    {
      title: "Stage 1 · Physics",
      color: "#0B4F8A",
      items: [
        { id: "cache", href: "stage1-foundations.html#cache", label: "Cache Locality" },
        { id: "amdahl", href: "stage1-foundations.html#amdahl", label: "Amdahl & Gustafson" },
        { id: "roofline", href: "stage1-foundations.html#roofline", label: "Roofline Explorer" }
      ]
    },
    {
      title: "Stage 2 · Parallel",
      color: "#0D9488",
      items: [
        { id: "false-sharing", href: "stage2-parallelism.html#false-sharing", label: "False Sharing" },
        { id: "mpi-halo", href: "stage2-parallelism.html#mpi-halo", label: "MPI 2D Halo" },
        { id: "cuda-tile", href: "stage2-parallelism.html#cuda-tile", label: "CUDA GEMM Tiling" }
      ]
    },
    {
      title: "Stage 3 · AI Systems",
      color: "#6D28D9",
      items: [
        { id: "vram", href: "stage3-ai-systems.html#vram", label: "VRAM Budget" },
        { id: "ring", href: "stage3-ai-systems.html#ring", label: "Ring All-Reduce" },
        { id: "kv", href: "stage3-ai-systems.html#kv", label: "KV Cache & Decode" },
        { id: "amss", href: "stage3-ai-systems.html#amss", label: "AMSS-NCKU Porting" }
      ]
    },
    {
      title: "Stage 4 · ASC Sprint",
      color: "#C2410C",
      items: [
        { id: "hpl", href: "stage4-asc-sprint.html#hpl", label: "HPL Grid Tuning" },
        { id: "power", href: "stage4-asc-sprint.html#power", label: "Power Wall & DVFS" },
        { id: "qubit", href: "stage4-asc-sprint.html#qubit", label: "Qubit Memory Wall" },
        { id: "past", href: "past-problems.html", label: "Past Problems (C01–C10)" }
      ]
    }
  ];

  const page = window.location.pathname.split("/").pop() || "index.html";

  // Track visited pages/labs in localStorage for lightweight progress feedback
  let visited = {};
  try {
    visited = JSON.parse(localStorage.getItem("asc27:visited") || "{}");
  } catch (e) {}
  visited[page] = true;
  try {
    localStorage.setItem("asc27:visited", JSON.stringify(visited));
  } catch (e) {}

  const header = document.getElementById("site-header");
  if (header) {
    header.className = "topbar";
    header.innerHTML = `
      <div class="topbar-inner">
        <a class="brand" href="index.html">
          <span class="brand-dot"></span>
          <span>HKUST ASC27</span>
          <span class="brand-sub">· Interactive HPC &amp; AI Lab</span>
        </a>
        <nav class="nav" aria-label="Main navigation">
          ${navItems.map(item => `<a href="${item.href}" class="${item.href === page ? "active" : ""}">${item.label}</a>`).join("")}
        </nav>
      </div>`;
  }

  // Wrap main.container inside .app-shell with persistent Designed-to-Scale course rail
  const mainEl = document.querySelector("main.container");
  if (mainEl && !document.querySelector(".app-shell")) {
    const shell = document.createElement("div");
    shell.className = "app-shell";

    const totalPages = navItems.length;
    const donePages = navItems.filter(it => visited[it.href]).length;
    const pct = Math.round((donePages / totalPages) * 100);

    const rail = document.createElement("aside");
    rail.className = "course-rail";
    rail.setAttribute("aria-label", "Curriculum navigation");
    rail.innerHTML = `
      <div class="rail-head">
        <span class="rail-title">Curriculum</span>
        <span class="rail-pct">${donePages}/${totalPages}</span>
      </div>
      <div class="rail-bar"><span style="width:${pct}%"></span></div>
      ${courseTree.map(group => `
        <div class="rail-group">
          <div class="rail-group-btn">
            <span class="rail-dot" style="background:${group.color}"></span>
            <span>${group.title}</span>
          </div>
          <ul class="rail-list">
            ${group.items.map(item => {
              const itemPage = item.href.split("#")[0];
              const isCurrentPage = itemPage === page;
              const isDone = !!visited[itemPage];
              return `<li>
                <a href="${item.href}" class="${isCurrentPage && !item.href.includes("#") ? "is-current" : ""}" data-rail-id="${item.id}">
                  <span class="rail-check ${isDone ? "is-done" : ""}">${isDone ? "✓" : ""}</span>
                  <span>${item.label}</span>
                </a>
              </li>`;
            }).join("")}
          </ul>
        </div>
      `).join("")}
    `;

    mainEl.parentNode.insertBefore(shell, mainEl);
    shell.appendChild(rail);
    shell.appendChild(mainEl);

    // Live scroll-spy for section focus in the left course rail
    const pageLinks = Array.from(rail.querySelectorAll(".rail-list a")).filter(
      a => a.getAttribute("href").split("#")[0] === page && a.getAttribute("href").includes("#")
    );
    const sectionPairs = pageLinks
      .map(a => ({ link: a, el: document.getElementById(a.getAttribute("href").split("#")[1]) }))
      .filter(p => p.el);

    if (sectionPairs.length) {
      const setActiveSection = (activeEl) => {
        sectionPairs.forEach(({ link, el }) => {
          link.classList.toggle("is-current", el === activeEl);
          el.classList.toggle("is-focused-lab", el === activeEl);
        });
      };
      setActiveSection(sectionPairs[0].el);
      if (typeof IntersectionObserver !== "undefined") {
        const io = new IntersectionObserver((entries) => {
          const visible = entries
            .filter(e => e.isIntersecting)
            .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
          if (visible.length) setActiveSection(visible[0].target);
        }, { rootMargin: "-18% 0px -52% 0px", threshold: [0.1, 0.35, 0.65] });
        sectionPairs.forEach(({ el }) => io.observe(el));
      }
    }

    // Contextual Prev / Next stage pager at the bottom of every page
    const curIdx = navItems.findIndex(it => it.href === page);
    if (curIdx !== -1 && !mainEl.querySelector(".stage-pager")) {
      const prev = curIdx > 0 ? navItems[curIdx - 1] : null;
      const next = curIdx < navItems.length - 1 ? navItems[curIdx + 1] : null;
      const pager = document.createElement("nav");
      pager.className = "stage-pager";
      pager.setAttribute("aria-label", "Page progression");
      pager.innerHTML = `
        <div class="stage-pager-slot">
          ${prev ? `
            <a class="pager-card pager-prev" href="${prev.href}">
              <span class="pager-dir">&larr; Previous</span>
              <span class="pager-title">${prev.label}</span>
              <span class="pager-sub">${prev.subtitle}</span>
            </a>
          ` : `
            <div class="pager-card is-placeholder" aria-hidden="true">
              <span class="pager-dir">Start of curriculum</span>
              <span class="pager-title">Stage 0 · Overview</span>
              <span class="pager-sub">Explore any node or follow Stage 1 next.</span>
            </div>
          `}
        </div>
        <div class="stage-pager-step">${curIdx + 1} / ${navItems.length}</div>
        <div class="stage-pager-slot">
          ${next ? `
            <a class="pager-card pager-next" href="${next.href}">
              <span class="pager-dir">Next &rarr;</span>
              <span class="pager-title">${next.label}</span>
              <span class="pager-sub">${next.subtitle}</span>
            </a>
          ` : `
            <a class="pager-card pager-next" href="index.html">
              <span class="pager-dir">Back to map &rarr;</span>
              <span class="pager-title">Home Overview</span>
              <span class="pager-sub">Return to the Knowledge Graph and 24-week roadmap</span>
            </a>
          `}
        </div>
      `;
      const footerEl = document.getElementById("site-footer");
      if (footerEl && footerEl.parentNode === mainEl) {
        mainEl.insertBefore(pager, footerEl);
      } else {
        mainEl.appendChild(pager);
      }

      // Keyboard shortcuts: '[' for Previous page, ']' for Next page (when not typing in an input)
      document.addEventListener("keydown", (ev) => {
        const tag = (ev.target && ev.target.tagName) || "";
        if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || ev.metaKey || ev.ctrlKey || ev.altKey) return;
        if (ev.key === "[" && prev) window.location.href = prev.href;
        if (ev.key === "]" && next) window.location.href = next.href;
      });
    }

    // Add subtle interactive cue badges to lab headers and control groups
    mainEl.querySelectorAll("section.lab-card").forEach((card) => {
      const hasControls = card.querySelector("input[type='range'], button");
      const header = card.querySelector(".lab-header");
      if (hasControls && header && !header.querySelector(".cue-pill")) {
        const pill = document.createElement("span");
        pill.className = "cue-pill";
        pill.innerHTML = `<span class="cue-dot" aria-hidden="true"></span><span>Interactive · try controls</span>`;
        const badge = header.querySelector(".stage-badge");
        if (badge) {
          const wrap = document.createElement("div");
          wrap.className = "lab-header-badges";
          badge.parentNode.insertBefore(wrap, badge);
          wrap.appendChild(pill);
          wrap.appendChild(badge);
        } else {
          header.appendChild(pill);
        }
      }
    });
  }

  const footer = document.getElementById("site-footer");
  if (footer) {
    footer.className = "footer";
    footer.innerHTML = `
      <span>HKUST ASC Team · ASC27 Training Curriculum (2026-11-25 to 2027-05-11)</span>
      <span><a href="https://github.com/hkust-asc/asc27-curriculum" target="_blank" rel="noopener">GitHub Repo &amp; Slide Decks</a></span>`;
  }

  // Shared KaTeX formula renderer with interactive hover/click symbol annotations
  window.ASC27 = window.ASC27 || {};

  window.ASC27.renderMath = function (el, tex, displayMode) {
    if (!el) return;
    if (window.katex && typeof window.katex.render === "function") {
      try {
        window.katex.render(tex, el, {
          displayMode: displayMode !== false,
          throwOnError: false,
          strict: false
        });
        return;
      } catch (e) {}
    }
    el.textContent = tex;
  };

  window.ASC27.renderFormulaBox = function (container, spec) {
    if (!container || !spec) return;
    const symbols = spec.symbols || [];
    const colorCount = 5;
    const escHtml = (str) => String(str == null ? "" : str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");

    const wrapTexSymbols = (rawTex, syms) => {
      let work = rawTex;
      const placed = new Map();
      const placeholders = [];
      const indexed = syms.map((s, idx) => ({
        idx,
        candidates: [
          s.match,
          s.tex,
          s.sym,
        ].filter(Boolean)
      }));
      const ordered = indexed.sort((a, b) => {
        const la = Math.max(...a.candidates.map(c => c.length));
        const lb = Math.max(...b.candidates.map(c => c.length));
        return lb - la;
      });

      for (const item of ordered) {
        let matched = false;
        const variants = [];
        for (const c of item.candidates) {
          variants.push(c);
          if (c.includes("\\mathrm{")) variants.push(c.replace(/\\mathrm\{/g, "\\text{"));
          if (c.includes("\\text{")) variants.push(c.replace(/\\text\{/g, "\\mathrm{"));
          if (c.includes(",")) {
            variants.push(c.replace(/,\s*/g, " "));
            variants.push(c.replace(/,\s*/g, "\\,"));
          }
        }
        const seen = new Set();
        for (const v of variants) {
          if (!v || seen.has(v)) continue;
          seen.add(v);
          let start = 0;
          while (true) {
            const pos = work.indexOf(v, start);
            if (pos === -1) break;
            const prev = pos > 0 ? work[pos - 1] : "";
            const next = pos + v.length < work.length ? work[pos + v.length] : "";
            const inCmd = prev === "\\" && !v.startsWith("\\");
            const isSingle = /^[A-Za-z0-9]$/.test(v);
            const badSingle = isSingle && (/[A-Za-z_]/.test(prev) || /[A-Za-z0-9_]/.test(next));
            const isSubOrSupBare = (prev === "^" || prev === "_") && !v.startsWith("{");
            const prefixWin = work.slice(Math.max(0, pos - 12), pos);
            const lastPh = prefixWin.lastIndexOf("@@SYM");
            const insidePlaceholder = lastPh !== -1 && !prefixWin.slice(lastPh + 5).includes("@@");
            if (!inCmd && !badSingle && !insidePlaceholder) {
              const phId = placeholders.length;
              const token = `@@SYM${phId}@@`;
              const wrappedToken = isSubOrSupBare ? `{${token}}` : token;
              work = work.slice(0, pos) + wrappedToken + work.slice(pos + v.length);
              placeholders.push({ token, idx: item.idx, orig: v });
              placed.set(item.idx, v);
              matched = true;
              start = pos + wrappedToken.length;
              continue;
            }
            start = pos + 1;
          }
          if (matched) break;
        }
      }
      for (const ph of placeholders) {
        const c = ph.idx % colorCount;
        const rep = `{\\htmlClass{ft-pill ft-c${c}}{\\htmlData{sym=${ph.idx}}{${ph.orig}}}}`;
        work = work.replace(ph.token, rep);
      }
      return { tex: work, placed };
    };

    const wrapped = wrapTexSymbols(spec.tex, symbols);
    container.className = "formula-box";
    container.innerHTML = `
      <div class="formula-stage">
        ${symbols.length ? `<div class="formula-hint"><span class="formula-hint-dot" aria-hidden="true"></span>Hover or click any colored term to inspect</div>` : ""}
        <div class="formula-math"></div>
        ${symbols.length ? `
          <svg class="formula-arrows" aria-hidden="true"></svg>
          <div class="sym-cards" role="list" aria-label="Formula symbols">
            ${symbols.map((s, idx) => `
              <button type="button" class="sym-card ft-c${idx % colorCount}" data-idx="${idx}" aria-expanded="false">
                <span class="sym-card-key" data-sym-tex="${encodeURIComponent(s.tex || s.sym)}">${escHtml(s.sym)}</span>
                <span class="sym-card-short">${escHtml(s.short)}</span>
              </button>
            `).join("")}
          </div>
          <div class="sym-popover" role="region" aria-live="polite" hidden>
            <div class="sym-popover-caret"></div>
            <div class="sym-popover-sym"></div>
            <div class="sym-popover-title"></div>
            <div class="sym-popover-desc"></div>
          </div>
        ` : ""}
      </div>
    `;

    const stageEl = container.querySelector(".formula-stage");
    const mathEl = container.querySelector(".formula-math");
    if (window.katex) {
      try {
        window.katex.render(wrapped.tex, mathEl, {
          displayMode: true,
          throwOnError: false,
          strict: false,
          trust: (ctx) => ctx.command === "\\htmlClass" || ctx.command === "\\htmlData"
        });
      } catch (e) {
        window.ASC27.renderMath(mathEl, spec.tex, true);
      }
    } else {
      mathEl.textContent = spec.tex;
    }

    if (!symbols.length) return;

    const svgEl = container.querySelector(".formula-arrows");
    const cards = Array.from(container.querySelectorAll(".sym-card"));
    const popover = container.querySelector(".sym-popover");
    const popSym = popover.querySelector(".sym-popover-sym");
    const popTitle = popover.querySelector(".sym-popover-title");
    const popDesc = popover.querySelector(".sym-popover-desc");
    const popCaret = popover.querySelector(".sym-popover-caret");
    const pillGroups = new Map();

    mathEl.querySelectorAll(".ft-pill").forEach((pill) => {
      const inner = pill.querySelector("[data-sym]");
      const idx = inner ? parseInt(inner.getAttribute("data-sym"), 10) : NaN;
      if (!Number.isNaN(idx)) {
        pill.dataset.idx = String(idx);
        pill.setAttribute("tabindex", "0");
        pill.setAttribute("role", "button");
        pill.setAttribute("aria-label", `${symbols[idx].short}: ${symbols[idx].desc}`);
        if (!pillGroups.has(idx)) pillGroups.set(idx, []);
        pillGroups.get(idx).push(pill);
      }
    });

    cards.forEach((card, idx) => {
      const keyEl = card.querySelector(".sym-card-key");
      const symTex = decodeURIComponent(keyEl.dataset.symTex || "");
      if (window.katex && symTex) {
        try {
          window.katex.render(symTex, keyEl, { displayMode: false, throwOnError: false, strict: false });
        } catch (e) {}
      }
    });

    const colors = ["#2563EB", "#16A34A", "#7C3AED", "#EA580C", "#0D9488"];
    let activeIdx = -1;
    let pinnedIdx = -1;

    const fitFormulaWidth = () => {
      const katexEl = mathEl.querySelector(".katex");
      if (!katexEl) return;
      katexEl.style.fontSize = "";
      const avail = mathEl.clientWidth - 8;
      const actual = katexEl.scrollWidth;
      if (avail > 40 && actual > avail) {
        const ratio = Math.max(0.62, avail / actual);
        katexEl.style.fontSize = `${(ratio * 100).toFixed(1)}%`;
      }
    };

    const drawArrows = () => {
      fitFormulaWidth();
      const stageRect = stageEl.getBoundingClientRect();
      if (stageRect.width < 10 || stageRect.height < 10) return;
      svgEl.setAttribute("viewBox", `0 0 ${stageRect.width} ${stageRect.height}`);
      svgEl.setAttribute("width", String(stageRect.width));
      svgEl.setAttribute("height", String(stageRect.height));

      const ns = "http://www.w3.org/2000/svg";
      svgEl.innerHTML = "";
      const defs = document.createElementNS(ns, "defs");
      colors.forEach((col, ci) => {
        const marker = document.createElementNS(ns, "marker");
        marker.setAttribute("id", `ft-arr-${ci}`);
        marker.setAttribute("viewBox", "0 0 10 10");
        marker.setAttribute("refX", "7");
        marker.setAttribute("refY", "5");
        marker.setAttribute("markerWidth", "6");
        marker.setAttribute("markerHeight", "6");
        marker.setAttribute("orient", "auto-start-reverse");
        const poly = document.createElementNS(ns, "path");
        poly.setAttribute("d", "M 1 1.5 L 8.5 5 L 1 8.5 z");
        poly.setAttribute("fill", col);
        marker.appendChild(poly);
        defs.appendChild(marker);
      });
      svgEl.appendChild(defs);

      cards.forEach((card, idx) => {
        const pills = pillGroups.get(idx);
        if (!pills || !pills.length) return;
        // Pick the occurrence closest to the card horizontally (preferring lower/non-numerator terms)
        const cr = card.getBoundingClientRect();
        if (cr.width === 0) return;
        const cardCx = (cr.left + cr.right) / 2;
        let pill = pills[0];
        let bestScore = Infinity;
        for (const p of pills) {
          const r = p.getBoundingClientRect();
          if (r.width === 0) continue;
          const dx = Math.abs((r.left + r.right) / 2 - cardCx);
          const inNum = Boolean(p.closest(".mfrac > .vlist-t > .vlist-r > .vlist > span:last-child"));
          const score = dx + (inNum ? 160 : 0);
          if (score < bestScore) {
            bestScore = score;
            pill = p;
          }
        }
        const pr = pill.getBoundingClientRect();
        if (pr.width === 0) return;

        const sx = (cr.left + cr.right) / 2 - stageRect.left;
        const sy = cr.top - stageRect.top;
        const tx = (pr.left + pr.right) / 2 - stageRect.left;
        const ty = pr.bottom - stageRect.top + 4;
        if (sy <= ty + 4 || tx < 2 || tx > stageRect.width - 2) return;

        const midY = (sy + ty) / 2;
        const path = document.createElementNS(ns, "path");
        path.setAttribute("d", `M ${sx.toFixed(1)} ${sy.toFixed(1)} C ${sx.toFixed(1)} ${midY.toFixed(1)}, ${tx.toFixed(1)} ${midY.toFixed(1)}, ${tx.toFixed(1)} ${ty.toFixed(1)}`);
        path.setAttribute("fill", "none");
        path.setAttribute("stroke", colors[idx % colorCount]);
        path.setAttribute("stroke-width", activeIdx === idx ? "2.2" : "1.5");
        path.setAttribute("stroke-linecap", "round");
        path.setAttribute("opacity", activeIdx === -1 || activeIdx === idx ? "0.92" : "0.28");
        path.setAttribute("marker-end", `url(#ft-arr-${idx % colorCount})`);
        path.dataset.idx = String(idx);
        svgEl.appendChild(path);
      });
    };

    const showPopover = (idx) => {
      const s = symbols[idx];
      if (!s) return;
      activeIdx = idx;
      const c = idx % colorCount;
      cards.forEach((card, i) => {
        card.classList.toggle("is-active", i === idx);
        card.classList.toggle("is-dim", i !== idx);
        card.setAttribute("aria-expanded", String(i === idx));
      });
      pillGroups.forEach((pills, i) => {
        pills.forEach((pill) => {
          pill.classList.toggle("is-active", i === idx);
          pill.classList.toggle("is-dim", i !== idx);
        });
      });
      popover.className = `sym-popover ft-c${c}`;
      if (window.katex && (s.tex || s.sym)) {
        try {
          window.katex.render(s.tex || s.sym, popSym, { displayMode: false, throwOnError: false, strict: false });
        } catch (e) {
          popSym.textContent = s.sym;
        }
      } else {
        popSym.textContent = s.sym;
      }
      popTitle.textContent = s.short;
      popDesc.textContent = s.desc;
      popover.hidden = false;

      const stageRect = stageEl.getBoundingClientRect();
      const anchor = cards[idx];
      const anchorRect = anchor.getBoundingClientRect();
      const popW = Math.min(280, stageRect.width - 12);
      const centerX = (anchorRect.left + anchorRect.right) / 2 - stageRect.left;
      const left = Math.max(6, Math.min(stageRect.width - popW - 6, centerX - popW / 2));
      const top = anchorRect.bottom - stageRect.top + 8;
      popover.style.width = `${popW}px`;
      popover.style.left = `${left}px`;
      popover.style.top = `${top}px`;
      const caretX = Math.max(18, Math.min(popW - 18, centerX - left));
      popCaret.style.left = `${caretX}px`;
      drawArrows();
    };

    const hidePopover = () => {
      if (pinnedIdx !== -1) return;
      activeIdx = -1;
      popover.hidden = true;
      cards.forEach((card) => {
        card.classList.remove("is-active", "is-dim");
        card.setAttribute("aria-expanded", "false");
      });
      pillGroups.forEach((pills) => {
        pills.forEach((pill) => pill.classList.remove("is-active", "is-dim"));
      });
      drawArrows();
    };

    const bindTarget = (el, idx) => {
      el.addEventListener("mouseenter", () => showPopover(idx));
      el.addEventListener("focus", () => showPopover(idx));
      el.addEventListener("click", (ev) => {
        ev.stopPropagation();
        if (pinnedIdx === idx) {
          pinnedIdx = -1;
          hidePopover();
        } else {
          pinnedIdx = idx;
          showPopover(idx);
        }
      });
      el.addEventListener("keydown", (ev) => {
        if (ev.key === "Enter" || ev.key === " ") {
          ev.preventDefault();
          el.click();
        } else if (ev.key === "Escape") {
          pinnedIdx = -1;
          hidePopover();
        }
      });
    };

    cards.forEach((card, idx) => bindTarget(card, idx));
    pillGroups.forEach((pills, idx) => pills.forEach((pill) => bindTarget(pill, idx)));

    stageEl.addEventListener("mouseleave", () => {
      if (pinnedIdx === -1) hidePopover();
    });
    document.addEventListener("click", (ev) => {
      if (pinnedIdx !== -1 && !stageEl.contains(ev.target)) {
        pinnedIdx = -1;
        hidePopover();
      }
    });

    const scheduleArrows = () => window.requestAnimationFrame(drawArrows);
    scheduleArrows();
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(scheduleArrows);
    }
    if (typeof ResizeObserver !== "undefined") {
      const ro = new ResizeObserver(scheduleArrows);
      ro.observe(stageEl);
    } else {
      window.addEventListener("resize", scheduleArrows);
    }
  };
})();
