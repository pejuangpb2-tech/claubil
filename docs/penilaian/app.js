// Misi Kata Ganti Nama Diri: maklum balas murid.
// Responses stay in this browser (localStorage) and are shown on the teacher board.
(function () {
  "use strict";

  const KEY = "misi-kgnd-maklum-balas";
  const STAR = '<svg viewBox="0 0 100 100"><path d="M50 4 L62 36 L96 38 L69 59 L78 93 L50 74 L22 93 L31 59 L4 38 L38 36 Z"/></svg>';
  const FEEL = { 3: "Seronok", 2: "Biasa", 1: "Kurang seronok" };
  const SKILL = ["Mengenal pasti", "Mengelaskan", "Menggunakan dalam ayat", "Beza kami dan kita"];

  const $ = (id) => document.getElementById(id);
  let toastTimer;
  let cur;
  function fresh() { cur = { nama: "", perasaan: 0, suka: [], bintang: [0, 0, 0, 0], belajar: "", pesanan: "" }; }
  fresh();

  // ---------- storage (falls back to memory when blocked) ----------
  let memory = [];
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return memory; }
  }
  function save(list) {
    memory = list;
    try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) { /* storage blocked: keep in memory */ }
  }

  // ---------- helpers ----------
  function show(id) {
    document.querySelectorAll(".screen").forEach((s) => s.classList.remove("on"));
    $(id).classList.add("on");
    const step = { s1: 1, s2: 2, s3: 3 }[id] || 0;
    const dots = $("progress").children;
    for (let i = 0; i < dots.length; i++) dots[i].classList.toggle("done", i < step);
    $("progress").style.display = step ? "flex" : "none";
    clearTimeout(toastTimer);
    $("toast").className = "toast";
    if (id !== "s4") document.querySelectorAll(".confetti").forEach((c) => c.remove());
  }
  function toast(msg, ok) {
    const t = $("toast");
    t.textContent = msg;
    t.className = "toast show " + (ok ? "ok" : "no");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => (t.className = "toast"), 1800);
  }
  function play(id) {
    const a = $(id);
    try { a.currentTime = 0; a.play().catch(() => {}); } catch (e) { /* audio blocked */ }
  }
  function bounce(el) { el.classList.remove("pop"); void el.offsetWidth; el.classList.add("pop"); }
  function esc(s) { return s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }
  function starsText(n) { return "★".repeat(n) + "☆".repeat(3 - n); }

  // ---------- fit the 1280x720 stage to any frame ----------
  function fit() {
    const s = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
    $("stage").style.transform = "translate(-50%, -50%) scale(" + s + ")";
  }
  window.addEventListener("resize", fit);
  fit();

  // ---------- 0: start ----------
  $("nama").addEventListener("input", (e) => { $("mula").disabled = e.target.value.trim().length < 2; });
  $("nama").addEventListener("keydown", (e) => { if (e.key === "Enter" && !$("mula").disabled) $("mula").click(); });
  $("mula").addEventListener("click", () => {
    cur.nama = $("nama").value.trim();
    show("s1");
  });
  $("ke-cikgu").addEventListener("click", () => { renderBoard(); show("sT"); });

  // ---------- 1: feelings ----------
  document.querySelectorAll(".face").forEach((b) => {
    b.addEventListener("click", () => {
      cur.perasaan = +b.dataset.v;
      document.querySelectorAll(".face").forEach((x) => x.classList.toggle("on", x === b));
      bounce(b); play("sfx-pop");
      $("next1").disabled = false;
    });
  });
  document.querySelectorAll(".like").forEach((b) => {
    b.addEventListener("click", () => {
      b.classList.toggle("on"); bounce(b); play("sfx-pop");
      cur.suka = [...document.querySelectorAll(".like.on")].map((x) => x.textContent);
    });
  });
  $("next1").addEventListener("click", () => show("s2"));

  // ---------- 2: self assessment ----------
  document.querySelectorAll(".stars").forEach((box) => {
    const q = +box.dataset.q;
    for (let k = 1; k <= 3; k++) {
      const b = document.createElement("button");
      b.innerHTML = STAR; b.setAttribute("aria-label", k + " bintang");
      b.addEventListener("click", () => {
        cur.bintang[q] = k;
        box.querySelectorAll("button").forEach((x, j) => x.classList.toggle("on", j < k));
        bounce(b); play("sfx-pop");
        $("next2").disabled = cur.bintang.some((r) => !r);
      });
      box.appendChild(b);
    }
  });
  $("next2").addEventListener("click", () => show("s3"));

  // ---------- 3: reflection ----------
  $("belajar").addEventListener("input", () => { $("hantar").disabled = $("belajar").value.trim().length < 5; });
  $("hantar").addEventListener("click", () => {
    cur.belajar = $("belajar").value.trim();
    cur.pesanan = $("pesanan").value.trim();
    cur.masa = new Date().toLocaleString("ms-MY");
    const list = load(); list.push(cur); save(list);
    $("who4").textContent = "Syabas, " + cur.nama + "!";
    $("mystars").innerHTML = cur.bintang.map((n, i) => "<div><span>" + SKILL[i] + "</span><b>" + starsText(n) + "</b></div>").join("");
    show("s4");
    play("sfx-chime");
    confetti();
  });

  // ---------- 4: next pupil ----------
  $("seterusnya").addEventListener("click", () => {
    fresh();
    $("nama").value = ""; $("mula").disabled = true;
    document.querySelectorAll(".face, .like, .stars button").forEach((x) => x.classList.remove("on"));
    $("next1").disabled = true; $("next2").disabled = true; $("hantar").disabled = true;
    $("belajar").value = ""; $("pesanan").value = "";
    show("s0");
  });

  // ---------- teacher board ----------
  function renderBoard() {
    const list = load();
    const n = list.length;
    const feel = { 3: 0, 2: 0, 1: 0 };
    const avg = [0, 0, 0, 0];
    list.forEach((r) => { feel[r.perasaan] = (feel[r.perasaan] || 0) + 1; r.bintang.forEach((b, i) => (avg[i] += b)); });
    $("summary").innerHTML =
      '<div class="tile"><b>' + n + "</b><span>maklum balas</span></div>" +
      [3, 2, 1].map((v) => '<div class="tile"><b>' + feel[v] + "</b><span>" + FEEL[v] + "</span></div>").join("") +
      SKILL.map((s, i) => '<div class="tile"><b>' + (n ? (avg[i] / n).toFixed(1) : "-") + "<small>/3</small></b><span>" + s + "</span></div>").join("");
    $("list").innerHTML = n
      ? list.slice().reverse().map((r) =>
          '<div class="item"><div class="h"><b>' + esc(r.nama) + "</b><span>" + FEEL[r.perasaan] + " · " + r.bintang.map(starsText).join(" ") + "</span></div>" +
          "<p>" + esc(r.belajar) + "</p>" +
          (r.suka.length ? '<p class="s">Suka: ' + esc(r.suka.join(", ")) + "</p>" : "") +
          (r.pesanan ? '<p class="s">Pesanan: ' + esc(r.pesanan) + "</p>" : "") + "</div>").join("")
      : '<p class="empty">Belum ada maklum balas. Murid boleh mula dari skrin utama.</p>';
  }
  $("kembali").addEventListener("click", () => show("s0"));
  $("padam").addEventListener("click", () => {
    if (!load().length) return;
    if (confirm("Padam semua maklum balas pada peranti ini?")) { save([]); renderBoard(); toast("Semua maklum balas dipadam.", true); }
  });
  $("muat-turun").addEventListener("click", () => {
    const list = load();
    if (!list.length) { toast("Belum ada maklum balas untuk dimuat turun.", false); return; }
    const head = ["Nama", "Masa", "Perasaan", "Bahagian disukai"].concat(SKILL).concat(["Saya belajar", "Pesanan"]);
    const q = (v) => '"' + String(v).replace(/"/g, '""') + '"';
    const rows = list.map((r) => [r.nama, r.masa, FEEL[r.perasaan], r.suka.join("; ")].concat(r.bintang).concat([r.belajar, r.pesanan]).map(q).join(","));
    const blob = new Blob(["﻿" + head.map(q).join(",") + "\n" + rows.join("\n")], { type: "text/csv;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = "maklum-balas-kata-ganti.csv";
    document.body.appendChild(a); a.click(); a.remove();
  });

  function confetti() {
    const colors = ["#ffd23f", "#ef6f92", "#8f6fd1", "#4fa862", "#3d82c4"];
    for (let i = 0; i < 26; i++) {
      const s = document.createElement("div");
      s.className = "confetti";
      s.innerHTML = STAR.replace("<path", '<path fill="' + colors[i % colors.length] + '"');
      s.style.left = ((i * 47) % 1240) + "px";
      s.style.top = "-30px";
      s.style.animationDelay = ((i % 7) * 0.12) + "s";
      $("stage").appendChild(s);
      setTimeout(() => s.remove(), 3400);
    }
  }
})();
