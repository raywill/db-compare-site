(function () {
'use strict';

/* 导航顺序归一化：首页、维度对比、AI选型、场景案例、用户吐槽、方法论。同步执行（nav 已解析），老页面无需重推即可收敛，无闪烁 */
(function () {
var nav = document.querySelector('nav.mainnav');
if (!nav) return;
var order = ['index.html', 'compare.html', 'advisor.html', 'cases.html', 'rants.html', 'methodology.html'];
var links = nav.querySelectorAll('a'), byHref = {}, i;
for (i = 0; i < links.length; i++) byHref[links[i].getAttribute('href')] = links[i];
for (i = 0; i < order.length; i++) { if (byHref[order[i]]) nav.appendChild(byHref[order[i]]); }
/* 移动端下拉导航：跳转 */
var nsel = document.getElementById('nav-select');
if (nsel) nsel.addEventListener('change', function () { if (nsel.value) location.href = nsel.value; });
})();

/* ---------------- 语言 ---------------- */
var KEY = 'dbcompare-lang';
function getLang() {
var nav = '';
try { nav = (navigator.language || '').toLowerCase(); } catch (e) {}
var dflt = nav.indexOf('zh') === 0 ? 'zh' : 'en';
try { return localStorage.getItem(KEY) || dflt;}
catch (e) { return dflt;}
}
function escHtml(s) {
return String(s).replace(/[&<>"']/g, function (c) {
return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c];
});
}
function paintLabels(lang) {
var lab = document.querySelectorAll('[data-zh]');
for (var k = 0; k < lab.length; k++) {
var el = lab[k];
el.textContent = (lang === 'zh')? el.getAttribute('data-zh'): el.getAttribute('data-en');
}
}

/* ---------------- AI 跳转 / 复制（顶层作用域：PK 按钮与档案页深挖按钮都在 DOMContentLoaded 之外调用） ---------------- */
var AI_URLS = {
chatgpt: 'https://chatgpt.com/?q=',
grok: 'https://grok.com/?q=',
claude: 'https://claude.ai/new?q='
};
function aiOpenService(service, prompt) {
var base = AI_URLS[service];
if (!base ||!prompt) return;
window.open(base + encodeURIComponent(prompt), '_blank', 'noopener');
}
function flashCopy(btn, msg) {
var span = btn.querySelector('span') || btn;
var old = span.textContent;
span.textContent = msg;
setTimeout(function () { span.textContent = old;}, 1200);
}
function copyPromptText(text, btn) {
function done(ok) {
flashCopy(btn, getLang() === 'zh'? (ok? '已复制': '复制失败'): (ok? 'Copied': 'Copy failed'));
}
if (navigator.clipboard && navigator.clipboard.writeText) {
navigator.clipboard.writeText(text).then(function () { done(true);}, function () { done(false);});
} else {
var ta = document.createElement('textarea');
ta.value = text;
ta.style.position = 'fixed';
ta.style.opacity = '0';
document.body.appendChild(ta);
ta.select();
try { document.execCommand('copy'); done(true);}
catch (e) { done(false);}
document.body.removeChild(ta);
}
}
/* 对比页：一键复制当前可见对比结果为 Markdown（尊重领域/已选筛选与当前语言） */
function htmlToPlain(root) {
var out = [];
function walk(n) {
if (n.nodeType === 3) { out.push(n.nodeValue); return;}
if (n.nodeType !== 1) return;
var tag = n.tagName.toLowerCase(), i;
if (tag === 'br') { out.push('\n'); return;}
if (tag === 'li') out.push('- ');
for (i = 0; i < n.childNodes.length; i++) walk(n.childNodes[i]);
if (tag === 'p' || tag === 'div' || tag === 'li' ||
tag === 'h1' || tag === 'h2' || tag === 'h3' || tag === 'h4' || tag === 'tr') out.push('\n');
}
walk(root);
return out.join('').replace(/[ 	 　]+/g, ' ').replace(/ *\n */g, '\n').replace(/\n{3,}/g, '\n\n');
}
function cmpCellText(cell, lang) {
var blk = cell.querySelector('.lang-block.lang-' + lang);
if (!blk) return {verdict: '', body: ''};
var v = blk.querySelector('.verdict');
var verdict = v? v.textContent.trim(): '';
var full = blk.querySelector('.full'), src;
if (full && full.innerHTML.trim()) {
src = full.cloneNode(true);
} else {
src = document.createElement('div');
var sn = blk.querySelector('.snippet');
if (sn) src.appendChild(sn.cloneNode(true));
}
var chips = src.querySelectorAll('.verdict'), i;
for (i = 0; i < chips.length; i++) chips[i].parentNode.removeChild(chips[i]);
return {verdict: verdict, body: htmlToPlain(src).trim()};
}
function buildCompareMarkdown() {
var lang = getLang(), zh = lang === 'zh', i, r;
var rows = [], all = document.querySelectorAll('.cmp-table > tbody > tr');
for (i = 0; i < all.length; i++) if (all[i].style.display !== 'none') rows.push(all[i]);
var ths = document.querySelectorAll('.cmp-table > thead th'), dims = [];
for (i = 1; i < ths.length; i++) {
var ds = ths[i].querySelector(zh? '.dim-h-zh': '.dim-h-en');
dims.push(ds? ds.textContent.trim(): ths[i].textContent.trim());
}
var names = rows.map(function (row) {
var s = row.querySelector('.row-head [data-zh]');
return s? (zh? s.getAttribute('data-zh'): s.getAttribute('data-en')): '';
});
var dt = new Date();
var dstr = dt.getFullYear() + '-' + ('0' + (dt.getMonth() + 1)).slice(-2) + '-' + ('0' + dt.getDate()).slice(-2);
var L = [];
L.push(zh? '# 数据库维度对比': '# Database Comparison');
L.push('> ' + (zh? '产品': 'Products') + '：' + names.join(zh? '、': ', ') +
'（' + rows.length + (zh? ' 款': ' products') + '）｜' +
(zh? '维度': 'Dimensions') + '：' + dims.length + '｜' +
(zh? '导出': 'Exported') + '：' + dstr);
L.push('> ' + (zh? '来源 db-compare-site；本对比不做综合总分、不做排名。'
: 'Source: db-compare-site; no aggregate scores, no rankings.'));
L.push('');
for (i = 0; i < dims.length; i++) {
L.push('## ' + (i + 1) + '. ' + dims[i]);
L.push('');
for (r = 0; r < rows.length; r++) {
var cells = rows[r].querySelectorAll('td.cmp-cell');
if (i >= cells.length) continue;
var cm = cmpCellText(cells[i], lang);
L.push('**' + names[r] + '**' + (cm.verdict? ' —— ' + cm.verdict: ''));
if (cm.body) L.push(cm.body);
L.push('');
}
}
return L.join('\n').replace(/\n{3,}/g, '\n\n').trim() + '\n';
}
function cardPromptText(card) {
var pre = card.querySelector('.prompt-text.lang-' + getLang());
if (!pre) pre = card.querySelector('.prompt-text');
return pre? pre.textContent: '';
}

/* ---------------- 全局对比选型：顶栏托盘，跨页持久（localStorage），最多 4 款 ---------------- */
var SEL_KEY = 'dbcompare-selection';
var MAX_SEL = 4;
function catalog() { return window.DB_CATALOG || [];}
function prodName(slug) {
var c = catalog();
for (var i = 0; i < c.length; i++) if (c[i].slug === slug) return getLang() === 'zh'? c[i].name: (c[i].name_en || c[i].name);
return slug;
}
function getSelection() {
var out = [];
try {
var raw = localStorage.getItem(SEL_KEY);
var arr = raw? JSON.parse(raw): [];
var ok = {}, c = catalog(), i, j;
for (i = 0; i < c.length; i++) ok[c[i].slug] = 1;
for (j = 0; j < arr.length && out.length < MAX_SEL; j++) {
if (ok[arr[j]] && out.indexOf(arr[j]) < 0) out.push(arr[j]);
}
} catch (e) {}
return out;
}
function selNames() {
var s = getSelection(), r = [], i;
for (i = 0; i < s.length; i++) r.push(prodName(s[i]));
return r;
}
function toggleSelect(slug) {
var sel = getSelection();
var i = sel.indexOf(slug);
if (i >= 0) { sel.splice(i, 1);}
else {
if (sel.length >= MAX_SEL) return 'full';
sel.push(slug);
}
try { localStorage.setItem(SEL_KEY, JSON.stringify(sel));} catch (e) {}
applySelection();
return 'ok';
}
function clearSelection() {
try { localStorage.removeItem(SEL_KEY);} catch (e) {}
var _nb = document.getElementById('cmp-sel-names');
if (_nb) _nb.textContent = '';
applySelection();
}

function renderTray() {
var lang = getLang(), sel = getSelection(), i, k;
var count = document.getElementById('cmp-count');
if (count) count.textContent = sel.length;
var trayBtn = document.getElementById('cmp-tray-btn');
if (trayBtn) trayBtn.classList.toggle('tray-empty', sel.length === 0);
var box = document.getElementById('cmp-selected');
if (box) {
if (!sel.length) {
box.innerHTML = '<span class="tray-empty" data-zh="还没选，去点卡片上的「＋ 对比」" data-en="Nothing yet — hit “+ Compare” on a card"></span>';
} else {
var h = '';
for (i = 0; i < sel.length; i++) {
h += '<span class="sel-chip">' + escHtml(prodName(sel[i])) +
'<button type="button" data-unsel="' + sel[i] + '" aria-label="remove">×</button></span>';
}
box.innerHTML = h;
}
}
var list = document.getElementById('cmp-list');
if (list) {
var domains = window.DB_DOMAINS || {};
var order = ['oltp', 'kvdoc', 'olap', 'aidb'];
var c = catalog(), h2 = '';
for (var d = 0; d < order.length; d++) {
var dk = order[d];
var dn = domains[dk]? (lang === 'zh'? domains[dk].zh: domains[dk].en): dk;
var items = '';
for (k = 0; k < c.length; k++) {
var _dm = c[k].domains || [c[k].domain];
if (_dm.indexOf(dk) < 0) continue;
var on = sel.indexOf(c[k].slug) >= 0;
var dis = (!on && sel.length >= MAX_SEL)? ' disabled': '';
items += '<button type="button" class="tray-item' + (on? ' on': '') +
'" data-sel-toggle="' + c[k].slug + '"' + dis + '>' +
'<span class="tick">' + (on? '✓': '＋') + '</span>' + escHtml(prodName(c[k].slug)) + '</button>';
}
if (items) h2 += '<div class="tray-group"><div class="tray-group-h">' + escHtml(dn) + '</div>' + items + '</div>';
}
list.innerHTML = h2;
}
paintLabels(lang);
var coBar = document.getElementById('cmp-sel-actions');
if (coBar) {
coBar.hidden = sel.length === 0;
var coLab = document.getElementById('cmp-checkout-label');
if (coLab) coLab.textContent = (lang === 'zh'? '去对比（' + sel.length + ' 款）→': 'Compare (' + sel.length + ') →');
var coLink = document.getElementById('cmp-checkout');
if (coLink) coLink.href = 'compare.html?sel=' + sel.join(',');
}
}

function paintAddCmpButtons() {
var lang = getLang(), sel = getSelection();
var btns = document.querySelectorAll('[data-addcmp]');
for (var i = 0; i < btns.length; i++) {
var on = sel.indexOf(btns[i].getAttribute('data-addcmp')) >= 0;
btns[i].classList.toggle('on', on);
var lab = btns[i].querySelector('.addcmp-label');
if (lab) lab.textContent = on
? (lang === 'zh'? '✓ 已选': '✓ Selected')
: (lang === 'zh'? '＋ 对比': '＋ Compare');
}
}

/* 加入对比：飞入托盘动画（电商加购风格），落袋后才真正选中 */
var _flying = {};
function flyToTray(fromEl, done) {
var trayBtn = document.getElementById('cmp-tray-btn');
if (!trayBtn || !fromEl || window.matchMedia('(prefers-reduced-motion: reduce)').matches) { done(); return;}
var r1 = fromEl.getBoundingClientRect(), r2 = trayBtn.getBoundingClientRect();
var x0 = r1.left + r1.width / 2, y0 = r1.top + r1.height / 2;
var x1 = r2.left + r2.width / 2, y1 = r2.top + r2.height / 2;
var dot = document.createElement('div');
dot.className = 'fly-dot';
dot.style.transform = 'translate(' + x0 + 'px,' + y0 + 'px) translate(-50%,-50%)';
document.body.appendChild(dot);
var dur = 620, t0 = null;
function frame(ts) {
if (!t0) t0 = ts;
var t = Math.min(1, (ts - t0) / dur);
var x = x0 + (x1 - x0) * t;
var y = y0 + (y1 - y0) * t - Math.sin(t * Math.PI) * 110;
var s = 1 - .55 * t;
dot.style.transform = 'translate(' + x + 'px,' + y + 'px) translate(-50%,-50%) scale(' + s + ')';
dot.style.opacity = String(1 - .25 * t);
if (t < 1) requestAnimationFrame(frame);
else { dot.remove(); popTray(); done();}
}
requestAnimationFrame(frame);
}
function popTray() {
var b = document.getElementById('cmp-tray-btn');
if (!b) return;
b.classList.remove('tray-pop');
void b.offsetWidth;
b.classList.add('tray-pop');
setTimeout(function () { b.classList.remove('tray-pop');}, 500);
}

/* 对比页：有选择时只显示已选产品行，并禁用领域筛选 */
var cmpDomain = 'all';
/* 对比页：表格上方工具条的可见数量提示（复制范围 = 当前可见行 × 维度） */
/* URL 分享：?sel=slug1,slug2 —— 打开时校验后覆盖本地选择（?sel= 空值=清空） */
function applySelFromUrl() {
var m = /[?&]sel=([^&#]*)/.exec(window.location.search || '');
if (!m) return;
var valid = {}, c = catalog(), i;
for (i = 0; i < c.length; i++) valid[c[i].slug] = 1;
var raw = m[1];
try { raw = decodeURIComponent(raw.replace(/\+/g, ' ')); } catch (e) {}
var out = [], seen = {}, s, parts = raw.split(',');
for (i = 0; i < parts.length && out.length < MAX_SEL; i++) {
s = parts[i].trim().toLowerCase();
if (s && valid[s] && !seen[s]) { seen[s] = 1; out.push(s); }
}
try { localStorage.setItem(SEL_KEY, JSON.stringify(out)); } catch (e2) {}
}
function buildShareUrl() {
var base = (window.location.href || '').split('#')[0].split('?')[0];
return base + '?sel=' + getSelection().join(',');
}
function shareSelection(btn) {
var lang = getLang(), sel = getSelection();
if (!sel.length) {
flashCopy(btn, lang === 'zh'? '先选几款数据库': 'Select databases first');
return;
}
copyPromptText(buildShareUrl(), btn);
}
function updateCmpCount() {
var el = document.getElementById('cmp-visible-count');
if (!el) return;
var rows = document.querySelectorAll('.cmp-table > tbody > tr'), n = 0, i;
for (i = 0; i < rows.length; i++) if (rows[i].style.display !== 'none') n++;
var ths = document.querySelectorAll('.cmp-table > thead th');
var dims = ths.length > 0 ? ths.length - 1 : 0;
el.textContent = getLang() === 'zh'
? '当前可见：' + n + ' 款 × ' + dims + ' 维'
: 'Showing: ' + n + ' products × ' + dims + ' dimensions';
}
function applyCompareFilter() {
var rows = document.querySelectorAll('.cmp-table > tbody > tr');
if (!rows.length) return;
var sel = getSelection(), i, r;
var fbtns = document.querySelectorAll('.cmp-filter-btn');
var notice = document.getElementById('cmp-sel-notice');
if (sel.length) {
for (r = 0; r < rows.length; r++) {
rows[r].style.display = (sel.indexOf(rows[r].getAttribute('data-slug')) >= 0)? '': 'none';
}
for (i = 0; i < fbtns.length; i++) {
fbtns[i].classList.add('disabled');
fbtns[i].setAttribute('disabled', 'disabled');
}
if (notice) {
notice.hidden = false;
var nb = document.getElementById('cmp-sel-names');
if (nb) nb.textContent = selNames().join(getLang() === 'zh'? '、': ', ');
}
} else {
for (i = 0; i < fbtns.length; i++) {
fbtns[i].classList.remove('disabled');
fbtns[i].removeAttribute('disabled');
}
for (r = 0; r < rows.length; r++) {
var _dd = (rows[r].getAttribute('data-domains') || '').split(' ');
rows[r].style.display = (cmpDomain === 'all' || _dd.indexOf(cmpDomain) >= 0)? '': 'none';
}
if (notice) notice.hidden = true;
}
updateCmpCount();
}

/* PK 下拉框：中英文各一对，按当前语言取可见的那对 */
function pkSelects() {
var en = getLang() !== 'zh';
return [document.getElementById(en? 'pk-a-en': 'pk-a'), document.getElementById(en? 'pk-b-en': 'pk-b')];
}
function pkNoteEl() {
return document.getElementById(getLang() !== 'zh'? 'pk-note-en': 'pk-note');
}
/* AI 选型页 PK 区：选了 ≥2 款就用已选库，否则用下拉框 */
function paintPkNote() {
var note = pkNoteEl();
var _pp = pkSelects(), sa = _pp[0], sb = _pp[1];
if (!note ||!sa ||!sb) return;
var sel = getSelection(), lang = getLang();
if (sel.length >= 2) {
sa.disabled = true; sb.disabled = true;
sa.classList.add('dimmed'); sb.classList.add('dimmed');
var names = selNames().join(lang === 'zh'? '、': ', ');
note.hidden = false;
note.textContent = lang === 'zh'
? '已选 ' + sel.length + ' 款（' + names + '），下面按钮将直接用它们生成对比提示词；清空选择可恢复手动下拉框。'
: sel.length + ' selected (' + names + '). The buttons below will generate the comparison prompt from them; clear the selection to use the dropdowns again.';
} else {
sa.disabled = false; sb.disabled = false;
sa.classList.remove('dimmed'); sb.classList.remove('dimmed');
note.hidden = true;
note.textContent = '';
}
}

/* 提示词特化：把 {{CANDIDATES}} 替换为已选库名（无选择时显示通用填写提示） */
function specializePrompts() {
var lang = getLang(), sel = getSelection(), names = selNames();
var cards = document.querySelectorAll('.prompt-card[data-cand]');
for (var i = 0; i < cards.length; i++) {
var card = cards[i];
var mode = card.getAttribute('data-cand');
var hint = card.getAttribute(lang === 'zh'? 'data-hint-zh': 'data-hint-en') || '';
var repl;
if (mode === 'single') {
repl = (sel.length === 1)? (''): hint;
} else if (mode === 'first') {
repl = sel.length? names[0]: hint;
} else {
repl = sel.length? names.join(lang === 'zh'? '、': ', '): hint;
}
var pres = card.querySelectorAll('.prompt-text');
for (var j = 0; j < pres.length; j++) {
var pre = pres[j];
if (pre._raw === undefined) pre._raw = pre.textContent;
if (pre._raw.indexOf('{{CANDIDATES}}') >= 0) {
pre.textContent = pre._raw.split('{{CANDIDATES}}').join(repl);
}
}
}
}

function refreshDynamicText() {
if(window.__repaintCasesBar){window.__repaintCasesBar();}
if(window.__repaintRantsBar){window.__repaintRantsBar();}
renderTray();
paintAddCmpButtons();
paintPkNote();
specializePrompts();
updateCmpCount();
}
function applySelection() {
renderTray();
applyCompareFilter();
paintPkNote();
specializePrompts();
paintAddCmpButtons();
}

function apply(lang) {
document.documentElement.setAttribute('lang', lang === 'zh'? 'zh-CN': 'en');
var _t = document.querySelector('title[data-title-en]');
if (_t) document.title = lang === 'zh'? _t.getAttribute('data-title-zh'): _t.getAttribute('data-title-en');
var zhEls = document.querySelectorAll('.lang-zh');
for (var i = 0; i < zhEls.length; i++) zhEls[i].hidden = (lang!== 'zh');
var enEls = document.querySelectorAll('.lang-en');
for (var i = 0; i < enEls.length; i++) enEls[i].hidden = (lang!== 'en');
paintLabels(lang);
var btn = document.getElementById('lang-toggle');
if (btn) btn.textContent = (lang === 'zh')? 'EN': '中文';
try { localStorage.setItem(KEY, lang);} catch (e) {}
refreshDynamicText();
}

/* 多库 PK 提示词（N = 2/3/4）；无选择时走下拉框的旧模板 */
var PK_ZH = '你是一名中立的数据库架构顾问，不代表任何厂商。请基于公开资料，对{a}和{b}做一次双库 PK 对比。输出要求：1. 按这 47 个维度逐项对比：静态加密 / TDE、TLS / 传输加密、审计、认证与权限、备份恢复、可观测性、连接模型、事务与隔离级别、复制与一致性、扩展方式、兼容性、许可证与商业模式、中文资料丰富度、性能与延迟特征、合规与认证、成熟度与社区生态、标杆用户、生态工具链、云托管与 Serverless、数据接入与摄入、外部数据访问、CDC 与下游同步、TTL 与数据生命周期管理、在线 DDL 与 Schema 演进、多租户与资源隔离、跨地域多活、高可用架构与 RTO/RPO、行级安全与数据脱敏、JSON 与半结构化能力、全文检索能力、存储效率与压缩、开源协议与厂商锁定风险、查询优化器与计划稳定性、参数调优与自治能力、静默数据损坏防护、存储过程/触发器/过程语言、约束与数据完整性、分析 SQL 完备性、被遗忘权与数据擦除、数据血缘与目录集成、存算分离 vs 存算一体、多模能力、FinOps 成本可观测性、驱动与多语言生态、物化视图、支持跨云、热点数据更新能力。2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"和"未找到证据"，不要把没查到的写成不支持。3. 每款给出：最适合的场景、最可能踩的三个坑（从机制层面解释，并说明在什么负载或故障下会触发）。4. 不做综合总分、不排名，只给带条件的判断，格式为"如果……那么……"。5. 需要我的业务场景信息才能下结论时，主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。如果候选库属于不同领域（如 OLTP 与向量库），不要硬对比：先交互式逐题确认我的真实诉求与对比口径（每题给出带字母编号的选项，我只需回复字母即可作答），再决定是对比还是纠正选型方向。6. 用中文回答。（建议：把本站这两款产品的档案页内容贴在下面，作为分析的起点）';
var PK_EN = 'You are a neutral database architecture advisor, not affiliated with any vendor. Do a head-to-head comparison of {a} vs {b} based on public information. Requirements: 1. Compare dimension by dimension across these 47 dimensions: data-at-rest encryption / TDE, TLS / transport encryption, auditing, authentication & authorization, backup & recovery, observability, connection model, transactions & isolation levels, replication & consistency, scaling, compatibility, license & business model, Chinese-language resources, performance & latency, compliance & certifications, maturity & community, notable adopters, ecosystem tooling, managed & serverless, data ingestion, external data access, CDC & downstream, TTL & data lifecycle, online DDL & schema evolution, multi-tenancy & resource isolation, cross-region active-active, HA & RTO/RPO, row-level security & masking, JSON & semi-structured, full-text search, storage efficiency & compression, OSS license & lock-in risk, optimizer & plan stability, tuning & autonomy, silent corruption protection, stored procedures & triggers, constraints & integrity, analytical SQL, right to erasure, data lineage & catalog, storage-compute architecture, multi-model, FinOps & cost observability, drivers & clients, materialized views, multi-cloud support, hotspot update handling. 2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified; strictly distinguish "verified absent" from "no evidence found". 3. For each: best-fit scenarios and the three most likely production pitfalls, explained at the mechanism level with trigger conditions. 4. No aggregate total score and no ranking; conditional verdicts only, in "if..., then..." form. 5. When you need my scenario details for a conclusion, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. If the candidates belong to different domains (e.g. OLTP vs vector DB), do not force a comparison: first interactively confirm what I actually need and the right basis of comparison, one question at a time with lettered options I can answer by replying with the letter, then decide whether to compare or to correct the selection direction. 6. Answer in English. (Tip: paste the profile pages on this site for both products below as a starting point.)';
function pkPromptN(lang, names) {
var n = names.length, i, list = '', sep = (lang === 'zh')? '、': ', ';
for (i = 0; i < n; i++) list += (i? sep: '') + names[i];
if (lang === 'zh') {
var kind = n === 2? '双库 PK': n + ' 库';
return '你是一名中立的数据库架构顾问，不代表任何厂商。请基于公开资料，对' + list + '做一次' + kind + '对比。' +
'输出要求：1. 按这 47 个维度逐项对比：静态加密 / TDE、TLS / 传输加密、审计、认证与权限、备份恢复、可观测性、连接模型、事务与隔离级别、复制与一致性、扩展方式、兼容性、许可证与商业模式、中文资料丰富度、性能与延迟特征、合规与认证、成熟度与社区生态、标杆用户、生态工具链、云托管与 Serverless、数据接入与摄入、外部数据访问、CDC 与下游同步、TTL 与数据生命周期管理、在线 DDL 与 Schema 演进、多租户与资源隔离、跨地域多活、高可用架构与 RTO/RPO、行级安全与数据脱敏、JSON 与半结构化能力、全文检索能力、存储效率与压缩、开源协议与厂商锁定风险、查询优化器与计划稳定性、参数调优与自治能力、静默数据损坏防护、存储过程/触发器/过程语言、约束与数据完整性、分析 SQL 完备性、被遗忘权与数据擦除、数据血缘与目录集成、存算分离 vs 存算一体、多模能力、FinOps 成本可观测性、驱动与多语言生态、物化视图、支持跨云、热点数据更新能力。' +
'2. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；严格区分"查证为无"和"未找到证据"，不要把没查到的写成不支持。' +
'3. 每款给出：最适合的场景、最可能踩的三个坑（从机制层面解释，并说明在什么负载或故障下会触发）。' +
'4. 不做综合总分、不排名，只给带条件的判断，格式为"如果……那么……"。' +
'5. 需要我的业务场景信息才能下结论时，主动向我提问：用交互式选择题逐题提问，一次只问一个关键问题，每个问题给出 3-4 个带字母编号的选项（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可作答；等我回答后再问下一题；不要一次把所有问题都列出来。所有关键问题问完后，再开始分析，不要编造。如果候选库属于不同领域（如 OLTP 与向量库），不要硬对比：先交互式逐题确认我的真实诉求与对比口径（每题给出带字母编号的选项，我只需回复字母即可作答），再决定是对比还是纠正选型方向。6. 用中文回答。' +
'（建议：把本站这几款产品的档案页内容贴在下面，作为分析的起点）';
}
var kindEn = n === 2? 'head-to-head': n + '-way';
return 'You are a neutral database architecture advisor, not affiliated with any vendor. Do a ' + kindEn + ' comparison of ' + list + ' based on public information. ' +
'Requirements: 1. Compare dimension by dimension across these 47 dimensions: data-at-rest encryption / TDE, TLS / transport encryption, auditing, authentication & authorization, backup & recovery, observability, connection model, transactions & isolation levels, replication & consistency, scaling, compatibility, license & business model, Chinese-language resources, performance & latency, compliance & certifications, maturity & community, notable adopters, ecosystem tooling, managed & serverless, data ingestion, external data access, CDC & downstream, TTL & data lifecycle, online DDL & schema evolution, multi-tenancy & resource isolation, cross-region active-active, HA & RTO/RPO, row-level security & masking, JSON & semi-structured, full-text search, storage efficiency & compression, OSS license & lock-in risk, optimizer & plan stability, tuning & autonomy, silent corruption protection, stored procedures & triggers, constraints & integrity, analytical SQL, right to erasure, data lineage & catalog, storage-compute architecture, multi-model, FinOps & cost observability, drivers & clients, materialized views, multi-cloud support, hotspot update handling. ' +
'2. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified; strictly distinguish "verified absent" from "no evidence found". ' +
'3. For each: best-fit scenarios and the three most likely production pitfalls, explained at the mechanism level with trigger conditions. ' +
'4. No aggregate total score and no ranking; conditional verdicts only, in "if..., then..." form. ' +
'5. When you need my scenario details for a conclusion, proactively ask me targeted interactive multiple-choice questions, one key question per turn: each with 3-4 lettered options (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; wait for my answer before asking the next question; do not list all questions at once. Start the analysis only after all key questions are answered, instead of inventing facts. If the candidates belong to different domains (e.g. OLTP vs vector DB), do not force a comparison: first interactively confirm what I actually need and the right basis of comparison, one question at a time with lettered options I can answer by replying with the letter, then decide whether to compare or to correct the selection direction. 6. Answer in English. ' +
'(Tip: paste the profile pages on this site for these products below as a starting point.)';
}

/* ---------------- 事件绑定 ---------------- */
document.addEventListener('DOMContentLoaded', function () {
apply(getLang());
var btn = document.getElementById('lang-toggle');
if (btn) btn.addEventListener('click', function () {
apply(getLang() === 'zh'? 'en': 'zh');
});
// index filter: by domain, hide empty domain sections
var fbtns = document.querySelectorAll('.filter-btn');
var cards = document.querySelectorAll('.card');
var dsecs = document.querySelectorAll('.domain-sec');
for (var i = 0; i < fbtns.length; i++) {
fbtns[i].addEventListener('click', function () {
for (var j = 0; j < fbtns.length; j++) fbtns[j].classList.remove('active');
this.classList.add('active');
var f = this.getAttribute('data-filter');
for (var c = 0; c < cards.length; c++) {
cards[c].style.display = (f === 'all' || cards[c].getAttribute('data-domain') === f)? '': 'none';
}
for (var s = 0; s < dsecs.length; s++) {
var any = false;
var cs = dsecs[s].querySelectorAll('.card');
for (var k = 0; k < cs.length; k++) {
if (cs[k].style.display!== 'none') { any = true; break;}
}
dsecs[s].style.display = any? '': 'none';
}
});
}
// compare page: filter product rows by domain (disabled while a selection is active)
var cfbtns = document.querySelectorAll('.cmp-filter-btn');
for (var i2 = 0; i2 < cfbtns.length; i2++) {
cfbtns[i2].addEventListener('click', function () {
if (this.hasAttribute('disabled')) return;
for (var j2 = 0; j2 < cfbtns.length; j2++) cfbtns[j2].classList.remove('active');
this.classList.add('active');
cmpDomain = this.getAttribute('data-filter');
applyCompareFilter();
});
}
// compare expand
document.addEventListener('click', function (ev) {
var t = ev.target;
if (t && t.classList && t.classList.contains('cell-toggle')) {
var cell = t.closest('.cmp-cell');
var block = t.closest('.lang-block');
if (!cell || !block) return;
var full = block.querySelector('.full');
var snippet = block.querySelector('.snippet');
var open = cell.classList.toggle('expanded');
if (full) full.hidden =!open;
if (snippet) snippet.hidden = open;
var label = open
? (getLang() === 'zh'? '收起': 'Collapse')
: (getLang() === 'zh'? '展开': 'Expand');
t.textContent = label;
}
});
// 全局对比选型：托盘开关 / 卡片按钮 / 面板内选择 / 清空（事件委托，面板内容是动态渲染的）
document.addEventListener('click', function (ev) {
var t = ev.target;
if (!t ||!t.closest) return;
var add = t.closest('[data-addcmp]');
if (add) {
var _slug = add.getAttribute('data-addcmp');
var _sel = getSelection();
if (_sel.indexOf(_slug) < 0 && _sel.length >= MAX_SEL) {
flashCopy(add, getLang() === 'zh'? '最多选 4 款': 'Up to 4');
} else if (_sel.indexOf(_slug) < 0) {
if (!_flying[_slug]) {
_flying[_slug] = true;
flyToTray(add, function () { _flying[_slug] = false; toggleSelect(_slug);});
}
} else {
toggleSelect(_slug);
}
return;
}
var un = t.closest('[data-unsel]');
if (un) { toggleSelect(un.getAttribute('data-unsel')); return;}
var tg = t.closest('[data-sel-toggle]');
if (tg) { if (!tg.disabled) toggleSelect(tg.getAttribute('data-sel-toggle')); return;}
if (t.closest('#cmp-clear') || t.closest('#cmp-sel-clear')) { clearSelection(); return;}
var cpc = t.closest('#cmp-copy');
if (cpc) { copyPromptText(buildCompareMarkdown(), cpc); return;}
var shl = t.closest('#cmp-share');
if (shl) { shareSelection(shl); return;}
var panel = document.getElementById('cmp-panel');
var trayBtn = t.closest('#cmp-tray-btn');
if (trayBtn && panel) {
var open = panel.hidden;
panel.hidden =!open;
trayBtn.setAttribute('aria-expanded', open? 'true': 'false');
return;
}
if (panel &&!panel.hidden &&!t.closest('.cmp-tray')) panel.hidden = true;
});
document.addEventListener('keydown', function (ev) {
if (ev.key === 'Escape') {
var panel = document.getElementById('cmp-panel');
if (panel &&!panel.hidden) panel.hidden = true;
}
});
// AI 选型：提示词卡片跳转外部 AI（读取的是特化后的文本）
document.addEventListener('click', function (ev) {
var t = ev.target;
if (!t ||!t.closest) return;
var b = t.closest('.ai-btn[data-act]');
if (!b) return;
var card = b.closest('.prompt-card');
if (!card) return;
var act = b.getAttribute('data-act');
var text = cardPromptText(card);
if (act === 'copy') copyPromptText(text, b);
else aiOpenService(act, text);
});
// 多库 PK：一键生成对比提示词（优先用托盘已选库，否则用下拉框）
document.addEventListener('click', function (ev) {
var t = ev.target;
if (!t ||!t.closest) return;
var b = t.closest('.ai-btn[data-pkact]');
if (!b) return;
var lang = getLang(), sel = getSelection(), tpl;
if (sel.length >= 2) {
tpl = pkPromptN(lang, selNames());
} else {
var _pp2 = pkSelects(), sa = _pp2[0], sb = _pp2[1];
var an = sa? sa.value: '';
var bn = sb? sb.value: '';
if (!an ||!bn) {
flashCopy(b, lang === 'zh'? '请先选两款库': 'Pick two first');
return;
}
tpl = (lang === 'zh'? PK_ZH: PK_EN).split('{a}').join(an).split('{b}').join(bn);
}
var act = b.getAttribute('data-pkact');
if (act === 'copy') copyPromptText(tpl, b);
else aiOpenService(act, tpl);
});
applySelFromUrl();
applySelection();
});

// 档案页"用 AI 深挖这款"：全局函数，供行内 onclick 调用
var DIVE_ZH = '你是一名中立的数据库架构顾问，专长是把系统推到极限。请深入分析{name}：\n\n1. 它的核心机制是什么？在什么负载、异常或故障下，这个机制会最先崩？\n2. 列出 3 个最可能在生产环境踩到的坑，从机制层面解释，并说明触发条件。\n3. 哪些场景是它的"甜蜜点"，哪些场景是"禁区"？为什么？\n4. 每个关键结论标注证据等级：官方文档、厂商口径、社区实测、社区共识、待验证；不确定的请明确说不知道，不要编造。\n5. 开始前先用一道交互式选择题问我最关心的 3-5 个维度：从 47 维中给出 3-4 组带字母编号的典型组合（A/B/C/D，外加 E. 其他，请说明），我只需回复字母即可勾选；等我回答后，再针对性深挖。不要一次抛出大段文字，也不要面面俱到地平铺。\n6. 不做综合评分。用中文回答。\n（建议：把本站该产品的档案页内容贴在下面，作为分析的起点）';
var DIVE_EN = 'You are a neutral database architecture advisor who specializes in pushing systems to their limits. Analyze {name} in depth:\n\n1. What is its core mechanism? Under what load, anomaly, or failure does this mechanism break first?\n2. List the 3 most likely production pitfalls, explain them at the mechanism level, and state their trigger conditions.\n3. Which scenarios are its sweet spot, and which are no-go zones? Why?\n4. Tag each key claim with an evidence level: official docs, vendor claim, community-tested, community consensus, to-be-verified. Say "I don\'t know" explicitly where uncertain instead of inventing facts.\n5. Before starting, ask me which 3-5 dimensions I care about most with one interactive multiple-choice question: offer 3-4 lettered bundles of typical dimension combinations (A/B/C/D plus E. Other, please specify) that I can answer by simply replying with the letter; go deep on those only after I answer. Do not dump a wall of text, and do not go a mile wide and an inch deep.\n6. No aggregate score. Answer in English.\n(Tip: paste this site\'s profile page for the product below as a starting point for the analysis.)';
window.aiDeepDive = function (service, btn) {
var row = (btn && btn.closest)? btn.closest('.ai-dive-row'): null;
var name = row? row.getAttribute('data-product'): '';
var tpl = getLang() === 'zh'? DIVE_ZH: DIVE_EN;
var base = AI_URLS[service];
if (!base) return;
window.open(base + encodeURIComponent(tpl.split('{name}').join(name)), '_blank', 'noopener');
};
})();
