$(document).ready(function() {

  // Remove a header in a table if a header is null
  const tables = document.getElementsByTagName('table');
  for (let table of tables) {
    let isnull = true;
    for (let th of table.getElementsByTagName('th')) {
      if (th.innerText) {
        isnull = false;
        break;
      }
    }
    if (isnull) {
      let thead = table.getElementsByTagName('thead');
      if (thead.length > 0) {
        thead[0].remove();
      }
    }
  }

  // Enable Tooltip
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
});
