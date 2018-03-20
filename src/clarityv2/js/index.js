import React from 'react';
import ReactDOM from 'react-dom';
import {Test} from './components/react/HelloWorld';
import Navbar from './components/navbar';
import './views/index';

// SCSS
import '../sass/screen.scss';
import '../sass/style.scss';
import '../sass/print.scss';

window.addEventListener('DOMContentLoaded', () => {
    let el = document.getElementById('react-test');
    if (el) {
        ReactDOM.render(<Test/>, el);
    }

    Navbar.init();
});
