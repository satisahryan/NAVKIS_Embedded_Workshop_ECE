/**
 * NAVKIS workshop - quiz scores + gradebook (Google Apps Script)
 * 1. Google Sheet -> Extensions -> Apps Script -> paste this file -> Save.
 * 2. Deploy -> New deployment -> Web app (Execute as: Me, Who has access: Anyone)
 *    -> copy the URL into quizScriptUrl in config.js.
 * 3. After the quiz: reload the Sheet, menu "Workshop" -> "Build / update gradebook".
 *    Fill in Challenge /13 and Participation /5; correct Labs /6 if needed.
 * 4. File -> Download -> CSV of the Gradebook tab, and send it for the certificates.
 */
const WEIGHTS = { quiz: 40, labs: 30, challenge: 20, participation: 10 };   // total 100

function doPost(e) {
  const d = JSON.parse(e.postData.contents);
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sh = ss.getSheetByName('Quiz') || ss.insertSheet('Quiz');
  if (sh.getLastRow() === 0) sh.appendRow(['Time', 'Name', 'USN', 'Score', 'Total', 'Answers', 'Labs done']);
  sh.appendRow([new Date(), d.name, String(d.usn || '').trim().toUpperCase(), d.score, d.total, String(d.answers || ''), d.labs || 0]);
  return ContentService.createTextOutput('ok');
}

function onOpen() {
  SpreadsheetApp.getUi().createMenu('Workshop').addItem('Build / update gradebook', 'buildGradebook').addToUi();
}

function buildGradebook() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const quiz = ss.getSheetByName('Quiz');
  if (!quiz || quiz.getLastRow() < 2) { SpreadsheetApp.getUi().alert('No quiz responses yet.'); return; }
  let g = ss.getSheetByName('Gradebook');
  if (!g) {
    g = ss.insertSheet('Gradebook');
    g.appendRow(['S.No', 'Name', 'USN', 'Quiz /15', 'Labs /6', 'Challenge /13', 'Participation /5', 'Total', 'Rating', 'Certificate No']);
    g.getRange('A1:J1').setFontWeight('bold').setBackground('#E3F4F1');
    g.setFrozenRows(1);
  }
  const have = new Set(g.getLastRow() > 1 ? g.getRange(2, 3, g.getLastRow() - 1, 1).getValues().map(r => String(r[0]).toUpperCase()) : []);
  const rows = quiz.getRange(2, 1, quiz.getLastRow() - 1, 7).getValues();
  let added = 0;
  rows.forEach(r => {
    const usn = String(r[2]).trim().toUpperCase();
    if (!usn || have.has(usn)) return;
    have.add(usn);
    const n = g.getLastRow() + 1;               // new row number
    g.appendRow([
      n - 1, r[1], usn,
      `=IFERROR(MAXIFS(Quiz!D:D,Quiz!C:C,C${n}),0)`,                                  // best quiz attempt
      `=IFERROR(INDEX(Quiz!G:G,MATCH(C${n},Quiz!C:C,0)),0)`,                         // self-declared labs (overwrite to correct)
      0, 3,                                                                           // challenge, participation: instructor fills in
      `=ROUND(D${n}/15*${WEIGHTS.quiz}+MIN(E${n},6)/6*${WEIGHTS.labs}+F${n}/13*${WEIGHTS.challenge}+G${n}/5*${WEIGHTS.participation},1)`,
      `=IFS(H${n}>=85,"Outstanding",H${n}>=70,"Excellent",H${n}>=55,"Very Good",H${n}>=40,"Good",TRUE,"Participated")`,
      `="NAVKIS-EWS26-"&TEXT(A${n},"000")`
    ]);
    added++;
  });
  g.autoResizeColumns(1, 10);
  SpreadsheetApp.getUi().alert(added + ' student(s) added. Fill in Challenge /13 and Participation /5.');
}
