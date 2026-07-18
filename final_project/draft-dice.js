class Dice{
    result = 0

    constructor(sidesList, type, price, color){
        this.sidesList = sidesList;
        this.type = type;
        this.price = price;
        this.color = color;
    }

    getInfo(){
        return `Sides: ${this.sidesList}, Type: ${this.type}, Price: ${this.price}`
    }

    getSides(){
        return this.sidesList;
    }

    changeSides(newSidesList){
        this.sidesList = newSidesList;
    }

    getType(){
        return this.type;
    }

    changeType(newType){
        this.type = newType;
    }

    getPrice(){
        return this.price;
    }

    getColor(){
        return this.color;
    }

    rollSelf(){
        this.result = this.sidesList[Math.floor(Math.random() * this.sidesList.length)];
        return this.result;
    }

    getResult(){
        return this.result;
    }
}

class GameManager{
    dungeon = 1;
    floor = 1;
    roundMod = 1;

    constructor(player, monster, shop, battle) {
        this.player = player;
        this.monster = monster;
        this.shop = shop;
        this.battle = battle;
        this.dungeon = 1;
        this.floor = 1;
        this.currentScreen = 'main-menu';
        this.isDiceBagOpen = false;
    }

    changeScreen(screenId){
        this.currentScreen = screenId;

        const screens = document.querySelectorAll('.screen');
        screens.forEach(screen => screen.classList.add('hidden'));

        const activeScreen = document.getElementById(`screen-${screenId}`);
        activeScreen.classList.remove('hidden');

        this.onScreenLoad(screenId);
    }

    onScreenLoad(screenId){
        if(screenId === 'battle'){
            this.player.pullHandFromBag();
            this.player.rollHand();
            this.monster.setHealth((100 + (this.floor * 10)) * this.dungeon);
            this.renderBattle(this.player.getHand());
        }
        else if(screenId === 'shop'){
            this.shop.restock();
            this.renderShop();
        }
    }

    toggleDiceBag(forceOpen = null) {
        if (forceOpen !== null) {
            this.isDiceBagOpen = forceOpen;
        } else {
            this.isDiceBagOpen = !this.isDiceBagOpen;
        }

        const modal = document.getElementById('dice-bag-modal');

        if (this.isDiceBagOpen) {
            modal.classList.remove('hidden');
            this.renderDiceBag();
        } else {
            modal.classList.add('hidden');
        }
    }

    renderDiceBag() {
        const listContainer = document.getElementById('modal-dice-list');
        listContainer.innerHTML = "";

        const playerBag = this.player.diceBag;

        if (playerBag.length === 0) {
            listContainer.innerHTML = "<p>Your bag is empty.</p>";
            return;
        }

    playerBag.forEach((dice, index) => {
        const diceRow = document.createElement('div');
        diceRow.className = 'bag-dice-item';

        const textElement = document.createElement('span');
        textElement.textContent = `Die ${index + 1}: ${dice.getType()} (${dice.getSides().length}-sided) - Value: ${dice.getPrice()}g`;

        const colorSwatch = document.createElement('div');
        colorSwatch.className = 'dice-color-swatch';
        colorSwatch.style.backgroundColor = dice.getColor(); 

        diceRow.appendChild(textElement);
        diceRow.appendChild(colorSwatch);

        listContainer.appendChild(diceRow);
    });
    }

    goUpFloor() {
        if(this.floor + 1 == 4){
            this.dungeon += 1;
            this.floor = 1;
            this.roundMod += .25;
        }else{
            this.floor += 1;
        }
    }

    getDungeon(){
        return this.dungeon;
    }

    getFloor(){
        return this.floor;
    }

    getRoundMod(){
        return this.roundMod;
    }

    renderShop() {
        const shopScreen = document.querySelector("#screen-shop");
        
        shopScreen.innerHTML = `
            <h1>Merchant</h1>
            <h3 id="shop-gold-display">Your Gold: ${this.player.getGold()}</h3>
            <p id="shop-message"></p>
            <div class="shop-dice"></div>
            <button class="dice-bag-button">Open Dice Bag</button>
            <button class="main-menu-button">Back</button>
        `; 

        shopScreen.querySelector(".dice-bag-button").addEventListener("click", () => this.toggleDiceBag(true));
        shopScreen.querySelector(".main-menu-button").addEventListener("click", () => this.changeScreen("main-menu"));

        const currentStock = this.shop.getInventory();

        if (currentStock.length === 0) {
            shopScreen.innerHTML += `<p>The merchant is sold out!</p>`;
            shopScreen.querySelector(".dice-bag-button").addEventListener("click", () => this.toggleDiceBag(true));
            shopScreen.querySelector(".main-menu-button").addEventListener("click", () => this.changeScreen("main-menu"));
            return;
        }

        currentStock.forEach((dice, index) => {
            const newDice = document.createElement('div');
            newDice.classList.add('dice');
            
            newDice.innerHTML = `
                <h3>${dice.getType()} Die</h3>
                <p>Sides:</p>
                <p>${dice.getSides()}</p>
                <p>Cost: ${dice.getPrice()} Gold</p>
            `;
            
            const buyBtn = document.createElement('button');
            buyBtn.textContent = "Buy";
            
            buyBtn.addEventListener("click", () => {
                const success = this.shop.attemptPurchase(index, this.player);
                
                if (success) {
                    this.renderShop(); 
                } else {
                    document.getElementById('shop-message').innerText = "Not enough gold!";
                    document.getElementById('shop-message').style.color = "red";
                }
            });
            
            newDice.appendChild(buyBtn);

            const shopDiceSection = document.querySelector(".shop-dice");
            shopDiceSection.appendChild(newDice);
        });
    }

    renderBattle(diceHand) {
        const battleScreen = document.querySelector('#screen-battle');
        battleScreen.innerHTML = `
        <h1>Dungeon: ${this.dungeon}, Floor: ${this.floor}</h1>
        <h2>Monster: ${this.monster.getName()}, ${this.monster.getHealth()}</h2>
        <h2>Player Health: ${this.player.getHealth()}</h2>
        <div id="dice-hand-section">
        </div>
        <div id="score-section">
        </div>
        <button id="reroll-button">Reroll</button>
        <button id="attack-button">Attack</button>
        <button class="dice-bag-button">Open Dice Bag</button>
        <button class="main-menu-button">Back</button>`

        battleScreen.querySelector(".dice-bag-button").addEventListener("click", () => this.toggleDiceBag(true));
        battleScreen.querySelector(".main-menu-button").addEventListener("click", () => this.changeScreen("main-menu"));
        battleScreen.querySelector("#attack-button").addEventListener("click", () => this.renderDamage());
        battleScreen.querySelector('#reroll-button').addEventListener("click", () => this.rerollHand());

        const diceSection = battleScreen.querySelector("#dice-hand-section");
        const scoreSection = document.querySelector("#score-section");

        diceHand.forEach(dice => {

            const newDice = document.createElement('div');
            newDice.classList.add('battle-dice');
            newDice.style.backgroundColor = dice.getColor();
            newDice.innerHTML = `
            <h3>${dice.getResult()}</h3>
            <p>${dice.getType()}</p>`;

            diceSection.appendChild(newDice);
        })

        scoreSection.innerHTML = `Score: ${this.player.getScore()}`;
    }

    renderDamage(){
        this.battle.attackPhase();

        if(this.monster.getHealth() <= 0){
            this.player.changeGold(3);
            this.changeScreen("main-menu");
            this.goUpFloor();
        }else{
            this.player.pullHandFromBag();
            this.player.rollHand();
            this.renderBattle(this.player.getHand());
        }
    }

    rerollHand(){
        this.player.rollHand();
        this.renderBattle(this.player.getHand());
    }

}

class Player{
    health = 100;
    max_rolls = 3;
    gold = 5;
    diceHand = [];

    constructor(){
        this.diceBag = [new Dice([1, 2, 3, 4, 5, 6], "Basic", 1), new Dice([1, 2, 3, 4, 5, 6], "Basic", 1), new Dice([1, 2, 3, 4, 5, 6], "Basic", 1), new Dice([1, 2, 3, 4, 5, 6], "Basic", 1), new Dice([1, 2, 3, 4, 5, 6], "Basic", 1)];
    }

    getHealth(){
        return this.health;
    }

    takeDamage(amount){
        this.health -= amount;
    }

    heal(amount){
        this.health += amount;
    }

    getMaxRolls(){
        return this.max_rolls;
    }

    getGold(){
        return this.gold;
    }

    changeGold(amount){
        this.gold += amount;
    }

    pullHandFromBag(){
        const shuffledBag = [...this.diceBag];

        for (let i = shuffledBag.length - 1; i > shuffledBag.length - 1 - 5; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffledBag[i], shuffledBag[j]] = [shuffledBag[j], shuffledBag[i]];
        }

        this.diceHand = shuffledBag.slice(-5);
    }

    addDiceToBag(dice){
        this.diceBag.push(dice)
    }

    getHand(){
        return this.diceHand;
    }

    rollHand(){
        this.diceHand.forEach(dice => {
            dice.rollSelf();
        })
    }

    getResults(){
        const resultsList = [];
        this.diceHand.forEach(dice => {
            resultsList.push(dice.getResult());
        })
        return resultsList;
    }

    getScore(){
        let score = 0;
        this.diceHand.forEach(dice => {
            score += dice.getResult();
        })
        return score;
    }

    getRoll(){
        const resultsList = [];
        this.diceHand.forEach(dice => {
            resultsList.push(`${dice.getType()}: ${dice.getResult()}`);
        })
        return resultsList;
    }
}

class Monster{
    nameList = ["Goblin", "Troll", "Slime", "Orc", "Wraith"];
    name = "Goblin";
    health = 100;
    damage = 10;
    value = 2;

    constructor(health, damage){
        this.name = this.nameList[Math.floor(Math.random() * this.nameList.length)];
        this.health = health;
        this.damage = damage;
    }

    getName(){
        return this.name;
    }

    getHealth(){
        return this.health;
    }

    setHealth(amount){
        this.health = amount;
    }

    takeDamage(amount){
        this.health -= amount;
    }

    dealDamage(){
        return this.damage;
    }

    getValue(){
        return this.value;
    }
}

class Shop {
    constructor() {
        this.inventory = [];
        this.restock();
    }

    restock() {
        this.inventory = [
            new Dice([1, 2, 3, 4, 5, 6], "Basic", 2, "white"), 
            new Dice([7, 7, 7, 7, 7, 7], "Iron", 1, "#EAEAEA"),
            new Dice([4, 4, 4, 4, 4, 4], "Gold", 1, "#FFE787"),
            new Dice([13, 13, 13, 13, 13, 13], "Cursed", 1, "#7A6174")
        ];
    }

    getInventory() {
        return this.inventory;
    }

    attemptPurchase(diceIndex, player) {
        const selectedDice = this.inventory[diceIndex];

        if (player.getGold() >= selectedDice.getPrice()) {
            
            player.changeGold(-selectedDice.getPrice());
            
            player.addDiceToBag(selectedDice);
            
            this.inventory.splice(diceIndex, 1);
            
            return true;
        } else {
            return false;
        }
    }
}

class Battle {
    constructor(monster, player){
        this.monster = monster;
        this.player = player;
    }

    attackPhase(){
        const playerDamage = this.player.getScore();

        if(playerDamage >= this.monster.getHealth()){
            this.monster.takeDamage(playerDamage);
        }else{
            this.monster.takeDamage(playerDamage);
            this.player.takeDamage(this.monster.dealDamage());
        }
    }
}

function attachButtonListeners(gM){
    document.querySelector("#battle-button").addEventListener("click", () => gM.changeScreen("battle"));
    document.querySelector("#shop-button").addEventListener("click", () => gM.changeScreen("shop"));

    const openBagButtons = document.querySelectorAll(".dice-bag-button");
    const mainMenuButtons = document.querySelectorAll(".main-menu-button");

    openBagButtons.forEach(button => {
        button.addEventListener("click", () => gM.toggleDiceBag(true));
    });

    document.querySelector(".close-button").addEventListener("click", () => gM.toggleDiceBag(false));
}









function init(){
    const player = new Player();
    const monster = new Monster(100, 10);
    const shop = new Shop();
    const battle = new Battle(monster, player);
    const gM = new GameManager(player, monster, shop, battle);
    attachButtonListeners(gM);

    console.log(gM.getDungeon());
    console.log(player.getHealth());
}



init();