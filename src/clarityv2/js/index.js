import React from "react";
import ReactDOM from "react-dom";
import { Test } from "./components/react/HelloWorld";
import Navbar from "./components/navbar";
import "./views/index";

window.addEventListener("DOMContentLoaded", () => {
    let el = document.getElementById("react-test");
    if (el) {
        ReactDOM.render(<Test />, el);
    }

    Navbar.init();
});
