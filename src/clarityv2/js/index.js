import { initNavbar } from "./components/navbar";
import { initHighlight } from "./components/codeHighlight";
import { initEmail } from "./components/email";

window.addEventListener("DOMContentLoaded", () => {
  initNavbar();
  initHighlight();
  initEmail();
});
