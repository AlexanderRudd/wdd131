const menu = document.querySelector('nav');
const btn = document.querySelector('.menu-btn');

btn.addEventListener('click', toggleMenu);

function toggleMenu(){
    menu.classList.toggle('hide')
    btn.classList.toggle('change')
}