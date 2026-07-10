// ─────────── SVG icons ───────────
const ICONS = {
  dashboard: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>`,
  patients: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
  appointments: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>`,
  ehr: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M12 12v6M9 15h6"/></svg>`,
  lab: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3v6l-4 8a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-4-8V3"/><path d="M8 3h8M7 15h10"/></svg>`,
  imaging: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M4 22h16"/><path d="M10 22V4a2 2 0 0 1 2-2 2 2 0 0 1 2 2v18"/><path d="M20 22V10l-6-4"/><path d="M4 22V10l6-4"/></svg>`,
  pharmacy: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/></svg>`,
  providers: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="7" r="4"/><path d="M12 11v3M9 17v3a3 3 0 0 0 6 0v-3"/><path d="M6 14h12a2 2 0 0 1 2 2v0a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v0a2 2 0 0 1 2-2Z"/></svg>`,
  insurance: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></svg>`,
  billing: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v18l3-3 3 3 3-3 3 3V8z"/><path d="M14 2v6h6M8 12h8M8 16h4"/></svg>`,
  devices: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2h6l-1 4h-4zM9 22h6l-1-4h-4zM6 12H2M22 12h-4"/></svg>`,
  assistants: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="18" height="12" rx="2"/><path d="M8 8V6a4 4 0 0 1 8 0v2"/><circle cx="9" cy="14" r="1"/><circle cx="15" cy="14" r="1"/></svg>`,
  bell: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>`,
  close: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg>`,
  heart: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>`,
  clock: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>`,
  alert: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z"/><path d="M12 9v4M12 17h.01"/></svg>`,
  pill: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/></svg>`,
  mail: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 5L2 7"/></svg>`,
  sms: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>`,
};

// ─────────── Config / state ───────────
const NAV = [
  { section: "Overview" },
  { id: "dashboard",     label: "Dashboard",       icon: ICONS.dashboard },
  { section: "Patient care" },
  { id: "patients",      label: "Patients",        icon: ICONS.patients },
  { id: "appointments",  label: "Appointments",    icon: ICONS.appointments },
  { id: "ehr",           label: "Clinical Notes",  icon: ICONS.ehr },
  { id: "lab",           label: "Lab Results",     icon: ICONS.lab },
  { id: "imaging",       label: "Imaging",         icon: ICONS.imaging },
  { id: "pharmacy",      label: "Prescriptions",   icon: ICONS.pharmacy },
  { section: "Administration" },
  { id: "providers",     label: "Staff Directory", icon: ICONS.providers },
  { id: "insurance",     label: "Insurance",       icon: ICONS.insurance },
  { id: "invoices",      label: "Billing",         icon: ICONS.billing },
  { id: "devices",       label: "Devices",         icon: ICONS.devices },
  { id: "ai_agents",     label: "Care Assistants", icon: ICONS.assistants },
];

const AVATAR_PALETTE = [
  ["#6366f1", "#a855f7"],
  ["#0ea5e9", "#22d3ee"],
  ["#f43f5e", "#ec4899"],
  ["#f59e0b", "#f97316"],
  ["#10b981", "#14b8a6"],
  ["#8b5cf6", "#6366f1"],
];
function avatarColors(seed) {
  const s = String(seed || "");
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
  return AVATAR_PALETTE[h % AVATAR_PALETTE.length];
}

const state = {
  view: "dashboard",
  patients: {},
  providers: {},
  counts: {},
  search: "",
};

// ─────────── Helpers ───────────
async function api(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`${path} → ${res.status}`);
  return res.json();
}

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k === "onClick") node.addEventListener("click", v);
    else if (k === "html") node.innerHTML = v;
    else if (k === "style") node.setAttribute("style", v);
    else if (v === true) node.setAttribute(k, "");
    else if (v === false || v == null) {}
    else node.setAttribute(k, v);
  }
  for (const c of children.flat()) {
    if (c == null || c === false) continue;
    node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  }
  return node;
}

function fmtDate(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  if (isNaN(d)) return iso;
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}
function fmtDateShort(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d)) return iso;
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}
function fmtTime(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d)) return "";
  return d.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
}
function fmtDateTime(iso) {
  if (!iso) return "—";
  return `${fmtDate(iso)} · ${fmtTime(iso)}`;
}
function ageFromDob(dob) {
  if (!dob) return "";
  const d = new Date(dob);
  if (isNaN(d)) return "";
  const now = new Date("2026-07-10");
  let age = now.getFullYear() - d.getFullYear();
  const m = now.getMonth() - d.getMonth();
  if (m < 0 || (m === 0 && now.getDate() < d.getDate())) age--;
  return `${age} yr`;
}
function relativeTime(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d)) return "";
  const diffMs = new Date("2026-07-10T09:00:00Z") - d;
  const mins = Math.round(diffMs / 60000);
  if (mins < 60) return `${mins} min ago`;
  const hrs = Math.round(mins / 60);
  if (hrs < 24) return `${hrs} hr ago`;
  const days = Math.round(hrs / 24);
  return `${days} d ago`;
}
function initials(first, last) {
  return `${(first || "?")[0]}${(last || "")[0] || ""}`.toUpperCase();
}
function avatar(first, last, size) {
  const [a, b] = avatarColors(`${first}${last}`);
  const style = `background: linear-gradient(135deg, ${a}, ${b});` + (size ? ` width:${size}px;height:${size}px;font-size:${Math.round(size / 3)}px;` : "");
  return el("div", { class: "mini-avatar", style }, initials(first, last));
}
function patientObj(id) { return state.patients[id]; }
function patientLabel(id) {
  const p = state.patients[id];
  if (!p) return `Patient #${id}`;
  return `${p.first_name} ${p.last_name}`;
}
function patientMRN(id) { return state.patients[id]?.mrn || ""; }
function providerLabel(id) {
  const p = state.providers[id];
  if (!p) return `Provider #${id}`;
  return `Dr. ${p.last_name}`;
}
function statusPill(status) {
  const s = (status || "").toLowerCase();
  const cls =
    ["active", "sent", "paid", "completed", "deployed", "final"].includes(s) ? "ok" :
    ["scheduled", "staging", "outstanding", "pending"].includes(s) ? "warn" :
    ["cancelled", "denied", "overdue", "error"].includes(s) ? "danger" : "muted";
  return el("span", { class: `pill ${cls}` }, status || "unknown");
}

// ─────────── Sidebar ───────────
function renderNav() {
  const nav = document.getElementById("nav");
  nav.innerHTML = "";
  for (const item of NAV) {
    if (item.section) {
      nav.appendChild(el("div", { class: "nav-section" }, item.section));
      continue;
    }
    const count = state.counts[item.id];
    const btn = el("button",
      { class: `nav-item ${state.view === item.id ? "active" : ""}`, onClick: () => setView(item.id) },
      el("span", { class: "nav-icon", html: item.icon }),
      el("span", {}, item.label),
      count != null ? el("span", { class: "nav-count" }, String(count)) : null,
    );
    nav.appendChild(btn);
  }
}

function setView(id) {
  state.view = id;
  renderNav();
  render();
}

// ─────────── Router ───────────
async function render() {
  const c = document.getElementById("content");
  c.innerHTML = '<div class="loading">Loading…</div>';
  try {
    if (state.view === "dashboard") await renderDashboard(c);
    else if (state.view === "patients") await renderPatients(c);
    else if (state.view === "appointments") await renderAppointments(c);
    else if (state.view === "providers") await renderProviders(c);
    else if (state.view === "ehr") await renderEHR(c);
    else if (state.view === "lab") await renderLabs(c);
    else if (state.view === "imaging") await renderImaging(c);
    else if (state.view === "pharmacy") await renderPharmacy(c);
    else if (state.view === "insurance") await renderInsurance(c);
    else if (state.view === "invoices") await renderInvoices(c);
    else if (state.view === "devices") await renderDevices(c);
    else if (state.view === "ai_agents") await renderAssistants(c);
  } catch (e) {
    c.innerHTML = `<div class="notice">Something went wrong loading this view.</div>`;
    console.error(e);
  }
}

// ─────────── Dashboard ───────────
async function renderDashboard(c) {
  const [appts, labs, notif, rx] = await Promise.all([
    api("/api/appointments/"),
    api("/api/lab/"),
    api("/api/notifications/"),
    api("/api/pharmacy/"),
  ]);

  const today = "2026-07-10";
  const todayAppts = appts.items
    .filter(a => (a.start_time || "").startsWith(today))
    .sort((a, b) => a.start_time.localeCompare(b.start_time));
  const upcoming = appts.items
    .filter(a => a.status === "scheduled")
    .sort((a, b) => a.start_time.localeCompare(b.start_time))
    .slice(0, 6);
  const abnormalLabs = labs.items.filter(l =>
    (l.results || []).some(r => r.flag && r.flag !== "N")
  );
  const activeRx = rx.items.filter(r => r.status === "active").length;

  const now = new Date("2026-07-10");
  const hour = 9;
  const greeting = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";

  c.innerHTML = "";
  c.appendChild(el("div", { class: "hero" },
    el("div", { class: "hero-content" },
      el("h2", { class: "hero-greeting" }, greeting),
      el("div", { class: "hero-sub" },
        todayAppts.length
          ? `You have ${todayAppts.length} appointment${todayAppts.length === 1 ? "" : "s"} today · ${abnormalLabs.length} lab result${abnormalLabs.length === 1 ? "" : "s"} need review`
          : "No appointments on your calendar today."),
    ),
    el("div", { class: "hero-date" },
      el("div", { class: "day" }, now.toLocaleDateString(undefined, { weekday: "long" })),
      el("div", { class: "full" }, now.toLocaleDateString(undefined, { month: "long", day: "numeric", year: "numeric" })),
    ),
  ));

  const stats = el("div", { class: "stats-grid" });
  stats.appendChild(statCard("Patients under care", Object.keys(state.patients).length, "+2 this month", ICONS.patients, ""));
  stats.appendChild(statCard("Today's appointments", todayAppts.length, todayAppts.length ? "On schedule" : "", ICONS.appointments, "info"));
  stats.appendChild(statCard("Labs to review", abnormalLabs.length, abnormalLabs.length ? "Needs review" : "All normal", ICONS.alert, "warn", abnormalLabs.length > 0));
  stats.appendChild(statCard("Active prescriptions", activeRx, "", ICONS.pill, "accent"));
  c.appendChild(stats);

  const grid = el("div", { class: "grid-2" });

  const apptCard = el("div", { class: "card" },
    el("div", { class: "card-header" },
      el("h3", { class: "card-title" }, "Upcoming appointments"),
      el("button", { class: "card-link", onClick: () => setView("appointments") }, "View all →"),
    ),
    el("div", { class: "card-body" },
      upcoming.length === 0
        ? el("div", { class: "card-empty" }, "No upcoming appointments.")
        : upcoming.map(a => appointmentRow(a)),
    )
  );
  grid.appendChild(apptCard);

  const recent = [...notif.items]
    .sort((a, b) => (b.sent_at || "").localeCompare(a.sent_at || ""))
    .slice(0, 6);
  const activityCard = el("div", { class: "card" },
    el("div", { class: "card-header" },
      el("h3", { class: "card-title" }, "Recent activity"),
    ),
    el("div", { class: "card-body" },
      recent.length === 0
        ? el("div", { class: "card-empty" }, "No recent activity.")
        : recent.map(n => el("div", { class: "activity-item" },
            el("div", { class: `activity-icon ${n.channel === "sms" ? "info" : "ok"}`, html: n.channel === "sms" ? ICONS.sms : ICONS.mail }),
            el("div", { class: "activity-body" },
              el("div", { class: "activity-text" },
                el("strong", {}, n.subject || "Notification"),
                document.createTextNode(` · ${patientLabel(n.patient_id)}`)),
              el("div", { class: "activity-time" }, `${n.channel?.toUpperCase() || ""} · ${relativeTime(n.sent_at)}`),
            ),
          )),
    ),
  );
  grid.appendChild(activityCard);

  c.appendChild(grid);
}

function statCard(label, value, delta, icon, tint, warn) {
  return el("div", { class: `stat-card ${tint || ""}` },
    el("div", { class: "stat-icon", html: icon || "" }),
    el("div", { class: "stat-label" }, label),
    el("div", { class: "stat-value" }, String(value)),
    delta ? el("div", { class: `stat-delta ${warn ? "warn" : ""}` }, delta) : null,
  );
}

function appointmentRow(a) {
  const p = patientObj(a.patient_id);
  return el("button", { class: "row", onClick: () => openPatient(a.patient_id) },
    el("div", { class: "row-time" }, fmtTime(a.start_time)),
    el("div", { class: "row-body", style: "display:flex;align-items:center;gap:12px" },
      p ? avatar(p.first_name, p.last_name, 34) : null,
      el("div", { style: "min-width:0" },
        el("div", { class: "row-title" }, patientLabel(a.patient_id)),
        el("div", { class: "row-sub" },
          `${a.reason || "Visit"} · ${providerLabel(a.provider_id)} · ${a.location || ""}`),
      ),
    ),
    statusPill(a.status),
  );
}

// ─────────── Patients ───────────
async function renderPatients(c) {
  const data = await api("/api/patients/");
  const rows = data.items;
  c.innerHTML = "";
  c.appendChild(pageHeader("Patients", `${rows.length} in your panel`));
  const filter = el("input", { class: "grow", type: "search", placeholder: "Filter by name, MRN, phone…" });
  c.appendChild(el("div", { class: "filter-bar" }, filter));

  const card = el("div", { class: "card" });
  const tbody = el("tbody");
  const table = el("table", { class: "data-table" },
    el("thead", {}, el("tr", {},
      el("th", {}, "Patient"),
      el("th", {}, "MRN"),
      el("th", {}, "DOB / Age"),
      el("th", {}, "Sex"),
      el("th", {}, "Allergies"),
      el("th", {}, "Contact"),
    )),
    tbody,
  );

  function paint() {
    const q = filter.value.toLowerCase();
    tbody.innerHTML = "";
    const filtered = rows.filter(p =>
      !q || `${p.first_name} ${p.last_name} ${p.mrn} ${p.phone} ${p.email}`.toLowerCase().includes(q)
    );
    for (const p of filtered) {
      const tr = el("tr", { onClick: () => openPatient(p.id) },
        el("td", {},
          el("div", { class: "name-cell" },
            avatar(p.first_name, p.last_name, 36),
            el("div", {},
              el("div", { class: "cell-main" }, `${p.first_name} ${p.last_name}`),
              el("div", { class: "cell-sub" }, p.address || ""),
            ),
          ),
        ),
        el("td", {}, p.mrn || "—"),
        el("td", {},
          el("div", {}, p.dob || "—"),
          el("div", { class: "cell-sub" }, ageFromDob(p.dob)),
        ),
        el("td", {}, p.gender || "—"),
        el("td", {}, (p.allergies || []).length
          ? el("span", {}, ...p.allergies.map(a => el("span", { class: "tag" }, `⚠ ${a}`)))
          : el("span", { class: "pill muted" }, "NKDA")),
        el("td", {},
          el("div", {}, p.phone || ""),
          el("div", { class: "cell-sub" }, p.email || ""),
        ),
      );
      tbody.appendChild(tr);
    }
    if (!filtered.length) {
      tbody.appendChild(el("tr", {}, el("td", { colspan: 6, class: "card-empty" }, "No patients match.")));
    }
  }
  filter.addEventListener("input", paint);
  paint();

  card.appendChild(table);
  c.appendChild(card);
}

// ─────────── Appointments ───────────
async function renderAppointments(c) {
  const data = await api("/api/appointments/");
  const sorted = data.items.sort((a, b) => a.start_time.localeCompare(b.start_time));
  c.innerHTML = "";
  c.appendChild(pageHeader("Appointments", `${sorted.length} on the calendar`));

  const today = "2026-07-10";
  const groups = {};
  for (const a of sorted) {
    const day = fmtDate(a.start_time);
    (groups[day] = groups[day] || []).push(a);
  }

  for (const [day, appts] of Object.entries(groups)) {
    const isToday = appts[0]?.start_time?.startsWith(today);
    c.appendChild(el("div", { class: "day-heading" },
      day,
      isToday ? el("span", { class: "today-pill" }, "Today") : null,
    ));
    const card = el("div", { class: "card", style: "margin-bottom:16px" },
      el("div", { class: "card-body" }, appts.map(a => appointmentRow(a))),
    );
    c.appendChild(card);
  }
}

// ─────────── Providers ───────────
async function renderProviders(c) {
  const data = await api("/api/providers/");
  c.innerHTML = "";
  c.appendChild(pageHeader("Staff Directory", `${data.items.length} clinicians and staff`));
  const grid = el("div", { class: "cards-grid" });
  for (const p of data.items) {
    grid.appendChild(el("div", { class: "info-card" },
      el("div", { class: "info-card-head" },
        avatar(p.first_name, p.last_name, 52),
        el("div", {},
          el("div", { style: "font-weight:600;font-size:15px" }, `Dr. ${p.first_name} ${p.last_name}`),
          el("div", { class: "cell-sub" }, `${p.specialty} · ${p.department}`),
        ),
      ),
      el("div", { class: "info-card-body" },
        el("div", {}, p.email || ""),
        el("div", {}, p.phone || ""),
        el("div", {}, `NPI ${p.npi}`),
      ),
      el("div", { class: "info-card-footer" },
        el("span", {}, p.role || ""),
        p.active ? el("span", { class: "pill ok" }, "Active") : el("span", { class: "pill muted" }, "Inactive"),
      ),
    ));
  }
  c.appendChild(grid);
}

// ─────────── EHR ───────────
async function renderEHR(c) {
  const data = await api("/api/ehr/");
  c.innerHTML = "";
  c.appendChild(pageHeader("Clinical Notes", `${data.items.length} visit note${data.items.length === 1 ? "" : "s"}`));
  const card = el("div", { class: "card" });
  const rows = data.items
    .sort((a, b) => (b.visit_date || "").localeCompare(a.visit_date || ""))
    .map(e => el("button", { class: "row", onClick: () => openPatient(e.patient_id) },
      el("div", { class: "row-time" }, fmtDateShort(e.visit_date)),
      el("div", { class: "row-body" },
        el("div", { class: "row-title" }, `${patientLabel(e.patient_id)} · ${e.chief_complaint || "Visit"}`),
        el("div", { class: "row-sub" },
          `${providerLabel(e.provider_id)} · ${(e.diagnosis || []).join("; ") || "no diagnosis"}`),
      ),
      el("span", { class: "pill brand" }, "Signed"),
    ));
  card.appendChild(el("div", { class: "card-body" }, rows.length ? rows : el("div", { class: "card-empty" }, "No notes yet.")));
  c.appendChild(card);
}

// ─────────── Labs ───────────
async function renderLabs(c) {
  const data = await api("/api/lab/");
  c.innerHTML = "";
  c.appendChild(pageHeader("Lab Results", `${data.items.length} recent panel${data.items.length === 1 ? "" : "s"}`));
  const card = el("div", { class: "card" });
  const body = el("div", { class: "card-body" });
  const items = data.items.sort((a, b) => (b.collected_at || "").localeCompare(a.collected_at || ""));
  for (const l of items) {
    const abnormal = (l.results || []).filter(r => r.flag && r.flag !== "N").length;
    body.appendChild(el("button", { class: "row", onClick: () => openPatient(l.patient_id) },
      el("div", { class: "row-time" }, fmtDateShort(l.collected_at)),
      el("div", { class: "row-body" },
        el("div", { class: "row-title" }, `${patientLabel(l.patient_id)} · ${l.panel}`),
        el("div", { class: "row-sub" },
          `${(l.results || []).length} analytes · ${abnormal} out of range · ordered by ${providerLabel(l.ordered_by)}`),
      ),
      abnormal ? el("span", { class: "pill danger" }, `${abnormal} abnormal`) : el("span", { class: "pill ok" }, "Normal"),
    ));
  }
  card.appendChild(body);
  c.appendChild(card);
}

// ─────────── Imaging ───────────
async function renderImaging(c) {
  const data = await api("/api/imaging/");
  c.innerHTML = "";
  c.appendChild(pageHeader("Imaging", `${data.items.length} stud${data.items.length === 1 ? "y" : "ies"}`));
  const card = el("div", { class: "card" });
  const body = el("div", { class: "card-body" });
  for (const i of data.items.sort((a, b) => (b.study_date || "").localeCompare(a.study_date || ""))) {
    body.appendChild(el("button", { class: "row", onClick: () => openPatient(i.patient_id) },
      el("div", { class: "row-time" }, fmtDateShort(i.study_date)),
      el("div", { class: "row-body" },
        el("div", { class: "row-title" }, `${i.modality} · ${i.body_part} — ${patientLabel(i.patient_id)}`),
        el("div", { class: "row-sub" }, i.impression || i.findings || ""),
      ),
      statusPill(i.status),
    ));
  }
  card.appendChild(body);
  c.appendChild(card);
}

// ─────────── Pharmacy ───────────
async function renderPharmacy(c) {
  const data = await api("/api/pharmacy/");
  c.innerHTML = "";
  c.appendChild(pageHeader("Prescriptions", `${data.items.length} active and past prescriptions`));
  const card = el("div", { class: "card" });
  const tbody = el("tbody");
  card.appendChild(el("table", { class: "data-table" },
    el("thead", {}, el("tr", {},
      el("th", {}, "Patient"), el("th", {}, "Medication"),
      el("th", {}, "Frequency"), el("th", {}, "Prescribed"),
      el("th", { class: "num" }, "Refills"), el("th", {}, "Status"),
    )),
    tbody,
  ));
  for (const rx of data.items.sort((a, b) => (b.written_at || "").localeCompare(a.written_at || ""))) {
    const p = patientObj(rx.patient_id);
    tbody.appendChild(el("tr", { onClick: () => openPatient(rx.patient_id) },
      el("td", {},
        el("div", { class: "name-cell" },
          p ? avatar(p.first_name, p.last_name, 32) : null,
          el("div", {},
            el("div", { class: "cell-main" }, patientLabel(rx.patient_id)),
            el("div", { class: "cell-sub" }, patientMRN(rx.patient_id)),
          ),
        ),
      ),
      el("td", {},
        el("div", { class: "cell-main" }, `${rx.drug} ${rx.dose || ""}`),
        el("div", { class: "cell-sub" }, `${rx.route || ""}`),
      ),
      el("td", {}, rx.frequency || "—"),
      el("td", {}, fmtDate(rx.written_at)),
      el("td", { class: "num" }, String(rx.refills ?? 0)),
      el("td", {}, statusPill(rx.status)),
    ));
  }
  c.appendChild(card);
}

// ─────────── Insurance ───────────
async function renderInsurance(c) {
  const data = await api("/api/insurance/");
  c.innerHTML = "";
  c.appendChild(pageHeader("Insurance", `${data.items.length} policy record${data.items.length === 1 ? "" : "s"}`));
  const card = el("div", { class: "card" });
  const tbody = el("tbody");
  card.appendChild(el("table", { class: "data-table" },
    el("thead", {}, el("tr", {},
      el("th", {}, "Patient"), el("th", {}, "Carrier"),
      el("th", {}, "Plan"), el("th", {}, "Member ID"),
      el("th", {}, "Effective"), el("th", {}, "Status"),
    )),
    tbody,
  ));
  for (const p of data.items) {
    const pt = patientObj(p.patient_id);
    tbody.appendChild(el("tr", { onClick: () => openPatient(p.patient_id) },
      el("td", {},
        el("div", { class: "name-cell" },
          pt ? avatar(pt.first_name, pt.last_name, 32) : null,
          el("div", { class: "cell-main" }, patientLabel(p.patient_id)),
        ),
      ),
      el("td", {}, p.carrier),
      el("td", {}, p.plan),
      el("td", {}, p.member_id),
      el("td", {}, p.effective_date || "—"),
      el("td", {}, statusPill(p.status)),
    ));
  }
  c.appendChild(card);
}

// ─────────── Invoices ───────────
async function renderInvoices(c) {
  const data = await api("/api/invoices/");
  c.innerHTML = "";
  c.appendChild(pageHeader("Billing", `${data.items.length} invoice${data.items.length === 1 ? "" : "s"}`));
  const card = el("div", { class: "card" });
  const tbody = el("tbody");
  card.appendChild(el("table", { class: "data-table" },
    el("thead", {}, el("tr", {},
      el("th", {}, "Patient"), el("th", {}, "Issued"),
      el("th", {}, "Due"), el("th", { class: "num" }, "Total"),
      el("th", { class: "num" }, "Balance"), el("th", {}, "Status"),
    )),
    tbody,
  ));
  for (const inv of data.items) {
    const pt = patientObj(inv.patient_id);
    tbody.appendChild(el("tr", { onClick: () => openPatient(inv.patient_id) },
      el("td", {},
        el("div", { class: "name-cell" },
          pt ? avatar(pt.first_name, pt.last_name, 32) : null,
          el("div", { class: "cell-main" }, patientLabel(inv.patient_id)),
        ),
      ),
      el("td", {}, fmtDate(inv.issued_at)),
      el("td", {}, inv.due_date || "—"),
      el("td", { class: "num" }, `$${inv.total?.toFixed(2) || "0.00"}`),
      el("td", { class: "num" }, `$${inv.balance?.toFixed(2) || "0.00"}`),
      el("td", {}, statusPill(inv.status)),
    ));
  }
  c.appendChild(card);
}

// ─────────── Devices ───────────
async function renderDevices(c) {
  const data = await api("/api/devices/");
  c.innerHTML = "";
  c.appendChild(pageHeader("Connected Devices", `${data.items.length} device${data.items.length === 1 ? "" : "s"} enrolled`));
  const grid = el("div", { class: "cards-grid" });
  for (const d of data.items) {
    const p = patientObj(d.patient_id);
    grid.appendChild(el("div", { class: "info-card", onClick: () => openPatient(d.patient_id) },
      el("div", { style: "display:flex;justify-content:space-between;align-items:flex-start;gap:10px;margin-bottom:14px" },
        el("div", {},
          el("div", { style: "font-weight:600;font-size:15px" }, d.model),
          el("div", { class: "cell-sub" }, `${d.type} · SN ${d.serial}`),
        ),
        statusPill(d.status),
      ),
      el("div", { class: "info-card-body", style: "display:flex;gap:10px;align-items:center" },
        p ? avatar(p.first_name, p.last_name, 34) : null,
        el("div", {},
          el("div", { style: "font-size:12px;color:var(--muted)" }, "Assigned to"),
          el("div", { style: "font-weight:500;color:var(--text)" }, patientLabel(d.patient_id)),
        ),
      ),
      el("div", { class: "info-card-footer" },
        el("span", {}, `Enrolled ${fmtDate(d.registered_at)}`),
      ),
    ));
  }
  c.appendChild(grid);
}

// ─────────── Care Assistants ───────────
async function renderAssistants(c) {
  const data = await api("/api/ai-agents/");
  c.innerHTML = "";
  c.appendChild(pageHeader("Care Assistants", "Automated helpers integrated into your workflow"));
  const grid = el("div", { class: "cards-grid" });
  for (const a of data.items) {
    grid.appendChild(el("div", { class: "info-card" },
      el("div", { style: "display:flex;justify-content:space-between;align-items:flex-start;gap:10px" },
        el("div", { style: "display:flex;gap:12px;align-items:center" },
          el("div", { class: "activity-icon", style: "width:44px;height:44px", html: ICONS.assistants }),
          el("div", {},
            el("div", { style: "font-weight:600;font-size:15px" }, a.name),
            el("div", { class: "cell-sub" }, `Managed by ${a.owner}`),
          ),
        ),
        statusPill(a.status),
      ),
      el("p", { style: "margin:14px 0 8px;font-size:13px;color:var(--text-2)" }, a.purpose),
      el("div", { class: "info-card-footer" },
        el("span", {}, `v${a.version}`),
        el("span", {}, `Added ${fmtDate(a.created_at)}`),
      ),
    ));
  }
  c.appendChild(grid);
}

// ─────────── Patient chart modal ───────────
async function openPatient(id) {
  const modal = document.getElementById("modal-backdrop");
  const body = document.getElementById("modal-body");
  const title = document.getElementById("modal-title");
  modal.hidden = false;
  title.textContent = "Loading patient…";
  body.innerHTML = '<div class="loading">Loading patient chart…</div>';

  try {
    const s = await api(`/api/patients/${id}/summary`);
    const p = s.patient;
    title.textContent = `${p.first_name} ${p.last_name} · Chart`;

    body.innerHTML = "";
    const [c1, c2] = avatarColors(`${p.first_name}${p.last_name}`);
    body.appendChild(el("div", { class: "patient-header" },
      el("div", { class: "patient-avatar", style: `background: linear-gradient(135deg, ${c1}, ${c2});` }, initials(p.first_name, p.last_name)),
      el("div", { style: "flex:1;min-width:0" },
        el("div", { class: "name" }, `${p.first_name} ${p.last_name}`),
        el("div", { class: "meta" }, `${p.mrn} · ${ageFromDob(p.dob)} · ${p.gender || "—"} · Blood type ${p.blood_type || "unknown"}`),
        el("div", { class: "tags" },
          (p.allergies && p.allergies.length)
            ? p.allergies.map(a => el("span", { class: "tag" }, `⚠ ${a}`))
            : el("span", { class: "pill muted" }, "NKDA"),
        ),
      ),
    ));

    body.appendChild(el("div", { class: "detail-grid" },
      detailItem("Date of birth", p.dob),
      detailItem("Phone", p.phone),
      detailItem("Email", p.email),
      detailItem("Address", p.address),
      detailItem("Enrolled", fmtDate(p.created_at)),
    ));

    const latestNote = (s.ehr || []).sort((a, b) => (b.visit_date || "").localeCompare(a.visit_date || ""))[0];
    if (latestNote && latestNote.vitals) {
      body.appendChild(el("div", { class: "section-title" }, `Latest vitals · ${fmtDate(latestNote.visit_date)}`));
      const v = latestNote.vitals;
      body.appendChild(el("div", { class: "vitals-grid" },
        vital("Blood pressure", v.bp, "mmHg"),
        vital("Heart rate", v.hr, "bpm"),
        vital("Temperature", v.temp_c, "°C"),
        vital("SpO₂", v.spo2, "%"),
      ));
    }

    body.appendChild(el("div", { class: "section-title" }, "Appointments"));
    body.appendChild(miniList(s.appointments, a => ({
      main: a.reason || "Visit",
      sub: `${providerLabel(a.provider_id)} · ${a.location || ""}`,
      right: `${fmtDate(a.start_time)} · ${fmtTime(a.start_time)}`,
      pill: statusPill(a.status),
    })));

    body.appendChild(el("div", { class: "section-title" }, "Visit notes"));
    body.appendChild(miniList(s.ehr, e => ({
      main: e.chief_complaint || "Visit",
      sub: `${providerLabel(e.provider_id)} · ${(e.diagnosis || []).join("; ")}`,
      right: fmtDate(e.visit_date),
    })));

    if ((s.labs || []).length) {
      body.appendChild(el("div", { class: "section-title" }, "Lab results"));
      for (const l of s.labs) {
        body.appendChild(el("div", { class: "lab-panel" },
          el("div", { class: "lab-panel-head" },
            el("strong", {}, l.panel),
            el("span", { class: "cell-sub" }, fmtDate(l.collected_at)),
          ),
          ...(l.results || []).map(r => el("div", { class: "lab-row" },
            el("div", {}, r.analyte),
            el("div", { class: "lab-value" }, `${r.value} ${r.unit || ""}`),
            el("div", { class: `lab-flag ${r.flag || "N"}` }, r.flag || "N"),
          )),
        ));
      }
    }

    if ((s.imaging || []).length) {
      body.appendChild(el("div", { class: "section-title" }, "Imaging"));
      body.appendChild(miniList(s.imaging, i => ({
        main: `${i.modality} · ${i.body_part}`,
        sub: i.impression || i.findings || "",
        right: fmtDate(i.study_date),
      })));
    }

    body.appendChild(el("div", { class: "section-title" }, "Prescriptions"));
    body.appendChild(miniList(s.prescriptions, r => ({
      main: `${r.drug} ${r.dose || ""}`,
      sub: `${r.frequency || ""} · ${r.route || ""} · Prescribed by ${providerLabel(r.prescriber_id)}`,
      right: fmtDate(r.written_at),
      pill: statusPill(r.status),
    })));

    if ((s.insurance || []).length) {
      body.appendChild(el("div", { class: "section-title" }, "Insurance"));
      body.appendChild(miniList(s.insurance, i => ({
        main: `${i.carrier} · ${i.plan}`,
        sub: `Member ${i.member_id} · Group ${i.group_id || "—"}`,
        right: `Copay $${i.copay || 0}`,
        pill: statusPill(i.status),
      })));
    }

    if ((s.devices || []).length) {
      body.appendChild(el("div", { class: "section-title" }, "Connected devices"));
      body.appendChild(miniList(s.devices, d => ({
        main: d.model,
        sub: `${d.type} · SN ${d.serial}`,
        right: fmtDate(d.registered_at),
        pill: statusPill(d.status),
      })));
    }
  } catch (e) {
    body.innerHTML = `<div class="notice">Could not load patient chart.</div>`;
    console.error(e);
  }
}

function detailItem(label, value) {
  return el("div", { class: "detail-item" },
    el("div", { class: "label" }, label),
    el("div", { class: "value" }, value || "—"),
  );
}
function vital(label, value, unit) {
  return el("div", { class: "vital" },
    el("div", { class: "v-label" }, label),
    el("div", { class: "v-value" },
      value == null ? "—" : String(value),
      unit && value != null ? el("span", { class: "v-unit" }, ` ${unit}`) : null,
    ),
  );
}
function miniList(items, adapt) {
  if (!items || !items.length) {
    return el("div", { class: "cell-sub", style: "padding:8px 0" }, "None on file.");
  }
  const ul = el("ul", { class: "mini-list" });
  for (const it of items) {
    const a = adapt(it);
    ul.appendChild(el("li", {},
      el("div", { style: "min-width:0" },
        el("div", { class: "mini-main" }, a.main),
        a.sub ? el("div", { class: "mini-sub" }, a.sub) : null,
      ),
      el("div", { class: "mini-right" },
        a.pill || null,
        a.right ? el("div", {}, a.right) : null,
      ),
    ));
  }
  return ul;
}

function pageHeader(title, subtitle) {
  return el("div", { class: "page-header" },
    el("div", {},
      el("h2", { class: "page-title" }, title),
      subtitle ? el("div", { class: "page-sub" }, subtitle) : null,
    ),
  );
}

// ─────────── Global search ───────────
function bindGlobalSearch() {
  const input = document.getElementById("global-search");
  let t;
  input.addEventListener("input", () => {
    clearTimeout(t);
    t = setTimeout(async () => {
      const q = input.value.trim();
      if (!q) return;
      try {
        const res = await api(`/api/patients/search?q=${encodeURIComponent(q)}`);
        if (res.count === 1) {
          openPatient(res.items[0].id);
        } else if (res.count > 1) {
          setView("patients");
        }
      } catch (_) {}
    }, 400);
  });
}

async function refreshNotificationBadge() {
  try {
    const data = await api("/api/notifications/");
    const unread = data.items.filter(n => n.status !== "read").length;
    const badge = document.getElementById("notif-badge");
    if (unread > 0) {
      badge.textContent = String(unread);
      badge.hidden = false;
    } else {
      badge.hidden = true;
    }
  } catch (_) {}
}

// ─────────── Boot ───────────
async function boot() {
  const [patients, providers, health] = await Promise.all([
    api("/api/patients/"),
    api("/api/providers/"),
    api("/api/health"),
  ]);
  for (const p of patients.items) state.patients[p.id] = p;
  for (const p of providers.items) state.providers[p.id] = p;
  const raw = health.counts || {};
  state.counts = {
    patients: patients.items.length,
    appointments: raw.appointments,
    ehr: raw.ehr,
    lab: raw.lab,
    imaging: raw.imaging,
    pharmacy: raw.prescriptions,
    providers: providers.items.length,
    insurance: raw.insurance,
    invoices: raw.invoices,
    devices: raw.devices,
    ai_agents: raw.ai_agents,
  };

  // Set the topbar bell + close icons
  const notifBtn = document.getElementById("notif-btn");
  notifBtn.innerHTML = ICONS.bell + '<span class="badge" id="notif-badge" hidden>0</span>';
  document.getElementById("modal-close").innerHTML = ICONS.close;

  renderNav();
  render();
  bindGlobalSearch();
  refreshNotificationBadge();

  document.getElementById("modal-close").addEventListener("click", () => {
    document.getElementById("modal-backdrop").hidden = true;
  });
  document.getElementById("modal-backdrop").addEventListener("click", (e) => {
    if (e.target.id === "modal-backdrop") {
      document.getElementById("modal-backdrop").hidden = true;
    }
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") document.getElementById("modal-backdrop").hidden = true;
  });
}

boot();
