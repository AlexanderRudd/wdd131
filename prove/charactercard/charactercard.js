const character = {
    level: 5,
    health: 100,

    levelUp: function(){
        this.level ++;
        console.log(this.level)
        document.querySelector(".level").innerHTML = `Level: ${this.level}`;
    },

    attacked: function(){
        if(this.health - 20 >= 1){
            this.health -= 20;
            document.querySelector(".health").innerHTML = `Health: ${this.health}`;
        }else{
            this.health -= 20;
            document.querySelector(".health").innerHTML = `Health: ${this.health}`;
            alert("You Died");
        }
    }
}

document.querySelector(".attacked").addEventListener("click", function () {
    character.attacked();
});

document.querySelector(".level_up").addEventListener("click", function () {
    character.levelUp();
});
