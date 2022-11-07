export function initEmail() {
  const encEmail = "Y2xhcml0eWRldnNvbHV0aW9uc0BnbWFpbC5jb20=";
  const form = document.getElementById("contact");
  if (form) {
    form.setAttribute("href", "mailto:".concat(atob(encEmail)));
  }
}
