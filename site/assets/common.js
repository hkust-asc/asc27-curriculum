(function () {
  const navItems = [
    { href: "index.html", label: "Home" },
    { href: "stage1-foundations.html", label: "Stage 1: Physics" },
    { href: "stage2-parallelism.html", label: "Stage 2: Parallel" },
    { href: "stage3-ai-systems.html", label: "Stage 3: AI & Porting" },
    { href: "stage4-asc-sprint.html", label: "Stage 4: ASC Sprint" },
    { href: "past-problems.html", label: "Past Problems" }
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
    container.className = "formula-box";
    container.innerHTML = `
      <div class="formula-math"></div>
      ${symbols.length ? `
        <div class="sym-strip" role="list" aria-label="Formula symbols">
          ${symbols.map((s, idx) => `
            <button type="button" class="sym-chip ${idx === 0 ? "is-active" : ""}" data-idx="${idx}" title="${s.desc}">
              <span class="sym-chip-key" data-sym-tex="${encodeURIComponent(s.tex || s.sym)}">${s.sym}</span>
              <span class="sym-chip-short">${s.short}</span>
            </button>
          `).join("")}
        </div>
        <div class="sym-readout"></div>
      ` : ""}
    `;

    const mathEl = container.querySelector(".formula-math");
    window.ASC27.renderMath(mathEl, spec.tex, true);

    if (symbols.length) {
      const readout = container.querySelector(".sym-readout");
      const chips = Array.from(container.querySelectorAll(".sym-chip"));

      chips.forEach((chip, idx) => {
        const keyEl = chip.querySelector(".sym-chip-key");
        const symTex = decodeURIComponent(keyEl.dataset.symTex || "");
        if (window.katex && symTex) {
          try {
            window.katex.render(symTex, keyEl, { displayMode: false, throwOnError: false });
          } catch (e) {}
        }
        const activate = () => {
          chips.forEach(c => c.classList.remove("is-active"));
          chip.classList.add("is-active");
          const s = symbols[idx];
          readout.innerHTML = `<strong>${s.short}:</strong> ${s.desc}`;
        };
        chip.addEventListener("mouseenter", activate);
        chip.addEventListener("focus", activate);
        chip.addEventListener("click", activate);
      });

      readout.innerHTML = `<strong>${symbols[0].short}:</strong> ${symbols[0].desc}`;
    }
  };
})();
