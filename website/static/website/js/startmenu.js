var Crowdjump = {};

Crowdjump.Menu = function(game){
    var startGame;
    var endGame;
};

Crowdjump.Menu.prototype = {
    create:function () {
        this.game.stage.backgroundColor = '#ffffff';
        startGame = this.add.text(10,10,'Start Game', {fill: "#000000"});
        endGame = this.add.text(10,40,'End Game', {fill: "#000000"});

        startGame.inputEnabled = true;
        startGame.events.onInputDown.add(this.phasergame,this)


        this.game.stage.backgroundColor = '#ffff00';
        endGame.inputEnabled = true;
        endGame.events.onInputDown.add(this.endscreen,this)
    },

    phasergame: function () {

        this.state.start('Game');
    },

    endscreen: function (){
        this.state.start('Endscreen');
    }
}