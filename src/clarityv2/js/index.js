import Navbar from "./components/navbar";
import { initHighlight } from "./components/codeHighlight";

window.addEventListener("DOMContentLoaded", () => {
    Navbar.init();
    initHighlight();
});
