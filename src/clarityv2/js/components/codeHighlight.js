import Prism from "prismjs";
import "prismjs/components/prism-javascript.min.js";
import "prismjs/components/prism-typescript.min.js";
import "prismjs/components/prism-python.min.js";
import "prismjs/components/prism-css.min.js";
import "prismjs/components/prism-handlebars.min.js";
import "prismjs/components/prism-markup-templating.min.js";
import "prismjs/themes/prism.css";
import 'prismjs/components/prism-jsx.min';

export const initHighlight = () => Prism.highlightAll();