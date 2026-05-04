let firstPara = document.getElementById("intro");
firstPara.style.backgroundColor = "#f2c556";

let em = document.querySelector("em");
em.style.backgroundColor = "#acbfcc";
em.innerText = "USS Voyager Starship";

const addImage = document.getElementById("starship");
const newImage = document.createElement('img');

newImage.src = "https://bit.ly/3RfG4sY";
newImage.alt = "Starship Image"
newImage.setAttribute('class', 'rounded');

//addImage.appendChild(newImage);
addImage.append(newImage);