footnum = 1
footnotequeue = "";

function addFootnote(message)  {
  document.write("<a href=\"#footnote" + footnum + "\"><sup>[" + footnum + "]</sup></a>");
  console.log("<a href=\"#footnote" + footnum + "\"><sup>[" + footnum + "]</sup></a>");
  footnotequeue = footnotequeue + "<p><a name=\"footnote" + footnum + "\">[" + footnum + "]</a>: " + message + "</p>\r\n"
  console.log(footnotequeue);
  footnum = footnum + 1;
  console.log(footnum);
}
$(document).ready(function()  {
  $("#footnotes").append(footnotequeue);
  footnotequeue = "";
});
