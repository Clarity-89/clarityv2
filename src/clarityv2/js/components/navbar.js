/**
 * Basic actions for navbar
 */
export default class Navbar {
    static init() {
        let nav = document.querySelector(".navbar__collapse");
        let navToggle = document.querySelector(".navbar__toggle");
        let navIcon = document.getElementById("nav-icon");

        if (navToggle) {
            navToggle.addEventListener("click", () => {
                let isCollapsed = nav.classList.contains(
                    "navbar__collapse--collapsed"
                );
                nav.classList.toggle(
                    "navbar__collapse--collapsed",
                    !isCollapsed
                );
                navIcon.classList.toggle("open");
            });
        }
    }
}
