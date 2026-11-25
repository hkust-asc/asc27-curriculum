(function () {
  const navItems = [
    { href: "index.html", label: "Home" },
    { href: "stage1-foundations.html", label: "Stage 1: Physics" },
    { href: "stage2-parallelism.html", label: "Stage 2: Parallel" },
    { href: "stage3-ai-systems.html", label: "Stage 3: AI & Porting" },
    { href: "stage4-asc-sprint.html", label: "Stage 4: ASC Sprint" },
    { href: "past-problems.html", label: "Past Problems" }
  ];

  const page = window.location.pathname.split("/").pop() || "index.html";
  const header = document.getElementById("site-header");
  if (header) {
    header.className = "topbar";
    header.innerHTML = `
      <div class="topbar-inner">
        <a class="brand" href="index.html"><span class="brand-dot"></span>HKUST ASC27 Interactive Lab</a>
        <nav class="nav" aria-label="Main navigation">
          ${navItems.map(item => `<a href="${item.href}" class="${item.href === page ? "active" : ""}">${item.label}</a>`).join("")}
        </nav>
      </div>`;
  }

  const footer = document.getElementById("site-footer");
  if (footer) {
    footer.className = "footer";
    footer.innerHTML = `
      <span>HKUST ASC Team · ASC27 Training Curriculum (2026-11-25 to 2027-05-11)</span>
      <span><a href="https://github.com/hkust-asc/asc27-curriculum" target="_blank" rel="noopener">GitHub Repo &amp; Slide Decks</a></span>`;
  }
})();
