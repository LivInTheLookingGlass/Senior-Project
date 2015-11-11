footnum = 1

function addFootnote(message)  {
  document.write("<a href=\"footnote" + footnum + "\"><sup>" + footnum + "</sup></a>");
  console.log("<a href=\"footnote" + footnum + "\"><sup>" + footnum + "</sup></a>");
  $("#footnotes").append("<a name=\"footnote" + footnum + "\">" + footnum + "</a>: <p>" + message + "</p>");
  console.log("<a name=\"footnote" + footnum + "\">" + footnum + "</a>: <p>" + message + "</p>");
  footnum = footnum + 1;
  console.log(footnum);
}
