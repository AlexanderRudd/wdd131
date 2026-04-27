const title = document.querySelector('h1');
title.textContent = 'Web Page Components';

console.log(title);

const topic = document.querySelector('#topics');
topic.style.color = 'purple';

const wrapper = document.getElementById('content');

wrapper.style.backgroundColor = "lightblue";

const list = document.querySelector(".list");

list.style.border = "3px solid black";

const paragraph = document.querySelector("p");

paragraph.style.fontSize = '2em';

paragraph.classList.add('background');

const image = document.querySelector('img');

image.setAttribute('src', 'images/newLogo.jpeg');