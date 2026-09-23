const vscode = require('vscode');
const http = require('http');
const https = require('https');

function postJson(url, body) {
  return new Promise((resolve, reject) => {
    const target = new URL(url);
    const transport = target.protocol === 'https:' ? https : http;
    const payload = JSON.stringify(body);
    const req = transport.request(target, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) }
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (res.statusCode >= 400) reject(new Error(parsed.error || 'Backend error'));
          else resolve(parsed);
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

function languageFromDocument(document) {
  const map = { c: 'C', cpp: 'C++', 'c++': 'C++', java: 'Java' };
  return map[document.languageId] || document.languageId;
}

async function run(endpoint, title) {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return vscode.window.showWarningMessage('Open a source file and select code first.');
  const selection = editor.selection;
  const code = editor.document.getText(selection).trim() || editor.document.getText().trim();
  const language = languageFromDocument(editor.document);
  try {
    const base = vscode.workspace.getConfiguration('codeguard').get('backendUrl');
    const result = await postJson(`${base}${endpoint}`, { code, language });
    const panel = vscode.window.createWebviewPanel('codeguardResult', title, vscode.ViewColumn.Beside, {});
    panel.webview.html = `<html><body><h2>${title}</h2><pre>${escapeHtml(JSON.stringify(result, null, 2))}</pre></body></html>`;
  } catch (error) {
    vscode.window.showErrorMessage(`CodeGuard: ${error.message}`);
  }
}

function escapeHtml(value) {
  return value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand('codeguard.analyzeSelection', () => run('/analyze', 'CodeGuard Analysis')),
    vscode.commands.registerCommand('codeguard.remediateSelection', () => run('/remediate', 'CodeGuard Remediation'))
  );
}

function deactivate() {}
module.exports = { activate, deactivate };
