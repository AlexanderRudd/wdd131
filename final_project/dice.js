const diceBox = {
    sides : [1, 2, 3, 4, 5, 6],
    result : 0,

    reroll: function(){
        var diceList = document.querySelectorAll(".dice");
        diceList.forEach(dice => {
            this.result = this.sides[Math.floor(Math.random() * this.sides.length)]
            dice.innerHTML = `${this.result}`;
        });
    },

    getSum: function(){
        sum = 0
        var diceList = document.querySelectorAll(".dice");
        diceList.forEach(dice => {
            num1 = parseInt(dice.innerHTML, 10);
            sum += num1;
            document.querySelector(".result_box").innerHTML = `${sum}`;
        });
    },

    getCount: function(){
        countList = [0, 0, 0, 0, 0, 0]

        var diceList = document.querySelectorAll(".dice");
        diceList.forEach(dice => {
            if(dice.innerHTML == "1"){
                countList[0] ++;
            }else if(dice.innerHTML == "2"){
                countList[1] ++;
            }else if(dice.innerHTML == "3"){
                countList[2] ++;
            }else if(dice.innerHTML == "4"){
                countList[3] ++;
            }else if(dice.innerHTML == "5"){
                countList[4] ++;
            }else{
                countList[5] ++;
            }
        })

        document.querySelector(".count_section").innerHTML = `
        <p>One's : ${countList[0]}</p>
        <p>Two's : ${countList[1]}</p>
        <p>Three's : ${countList[2]}</p>
        <p>Four's : ${countList[3]}</p>
        <p>Five's : ${countList[4]}</p>
        <p>Six's : ${countList[5]}</p>`
    },

    checkForHandTypes: function(){
        countList = [0, 0, 0, 0, 0, 0]

        var diceList = document.querySelectorAll(".dice");
        diceList.forEach(dice => {
            if(dice.innerHTML == "1"){
                countList[0] ++;
            }else if(dice.innerHTML == "2"){
                countList[1] ++;
            }else if(dice.innerHTML == "3"){
                countList[2] ++;
            }else if(dice.innerHTML == "4"){
                countList[3] ++;
            }else if(dice.innerHTML == "5"){
                countList[4] ++;
            }else{
                countList[5] ++;
            }
        })

        handType = "Chance"

        countList.forEach(count => {
            if(count >= 5){
                handType = "Five of A Kind"
            }else if(count == 4){
                handType = "Four of A Kind"
            }else if(count == 3){
                handType = "Three of A Kind"
            }else if(count == 2){
                handType = "Two of A Kind"
            }else{
                handType = "Chance"
            }
        }
        )

        document.querySelector(".hand_section").innerHTML = `
        <p>Hand Type: ${handType}</p>
        `
    }
}

diceColors = ["#DDD8B8", "#B3CBB9", "#84A9C0", "#6A66A3", "#542E71", "#bisque"]

document.querySelector(".reroll").addEventListener("click", function () {
    diceBox.reroll();
    diceBox.getSum();
    diceBox.getCount();
    diceBox.checkForHandTypes();
});

document.querySelector(".add_button").addEventListener("click", function () {
    const newDice = document.createElement('p');
    newDice.className = 'dice';
    newDice.innerHTML = "6";
    newDice.style.backgroundColor = diceColors[Math.floor(Math.random() * diceColors.length)]

    document.querySelector(".dice_section").appendChild(newDice);
    diceBox.getSum();
    diceBox.getCount();
    diceBox.checkForHandTypes();
})

