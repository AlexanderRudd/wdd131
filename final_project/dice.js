const diceTypes = [
    {
        name: "Basic",
        sides: [1, 2, 3, 4, 5, 6],
        color: "#E7E5E5"
    },

    {
        name: "Uncommon",
        sides: [7, 8, 9, 10, 11, 12],
        color: "#7BE0AD"
    }
]




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
    }
}

diceColors = ["#D3F9B5", "#DDFC74", "#BF6900", "#3D0C11"]

document.querySelector(".reroll").addEventListener("click", function () {
    diceBox.reroll();
    diceBox.getSum();
});

document.querySelector(".add_button").addEventListener("click", function () {
    const newDice = document.createElement('p');
    newDice.className = 'dice';
    newDice.innerHTML = "6";
    newDice.style.backgroundColor = diceColors[Math.floor(Math.random() * diceColors.length)]

    document.querySelector(".dice_section").appendChild(newDice);
    diceBox.getSum();
})

