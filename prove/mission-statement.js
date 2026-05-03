
let selectElem = document.querySelector('#theme-select');
let pageContent = document.querySelector('body');
const image = document.querySelector('img');

selectElem.addEventListener('change', changeTheme);

function changeTheme() {
    let current = selectElem.value;
    if (current === 'Dark') {
        pageContent.style.backgroundColor = "black";
        pageContent.style.color = "white";
        pageContent.style.borderColor = "white";
        image.setAttribute('src', 'images/byui-logo-white.png');
    } else {
        pageContent.style.backgroundColor = "white";
        pageContent.style.color = "black";
        pageContent.style.borderColor = "gray";
        image.setAttribute('src', 'images/byui-logo-blue.jpeg');
    }
}