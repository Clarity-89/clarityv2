import React from 'react';
import ReactDOM from 'react-dom';
import {Test} from './components/HelloWorld'
import './views/index';

// SCSS
import '../sass/screen.scss';
import '../sass/style.scss';
import '../sass/print.scss';

window.addEventListener('DOMContentLoaded', () => {
    ReactDOM.render(
        <Test/>,
        document.getElementById('react-test')
    );

    console.log('test', document.getElementById('react-test'))

});
