// 将 Markdown 中抽取出的公式批量渲染为 KaTeX HTML。
// 用法：node math_render.js < input.json > output.json
// 输入：{"items":[{"tex":"...","display":true|false}, ...]}
// 输出：{"html":["<span class=\"katex\">...</span>", ...]}

const fs = require('fs');
const path = require('path');

const katex = require(path.join(__dirname, 'vendor', 'package', 'dist', 'katex.js'));

const raw = fs.readFileSync(0, 'utf8');
let payload;
try {
  payload = JSON.parse(raw);
} catch (e) {
  process.stderr.write('invalid json input\n');
  process.exit(2);
}

const macros = {
  '\\R': '\\mathbb{R}',
  '\\C': '\\mathbb{C}',
  '\\E': '\\mathbb{E}',
  '\\dd': '\\mathrm{d}',
};

const out = payload.items.map((item) => {
  try {
    return katex.renderToString(item.tex, {
      displayMode: !!item.display,
      throwOnError: false,
      strict: false,
      trust: false,
      macros,
      output: 'html',
    });
  } catch (err) {
    return '<span class="katex-error">' + String(err.message || err) + '</span>';
  }
});

fs.writeFileSync(1, JSON.stringify({ html: out }));
