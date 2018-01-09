var Crowdjump = Crowdjump || {};

Crowdjump.Menu = function(game){
    var startGame;
    var logo;
};

Crowdjump.Menu.prototype = {
    create:function () {
        this.game.stage.backgroundColor = '#1948cd';


        logo = this.add.sprite(this.world.centerX,
                               this.world.centerY -80, 'logo');
        logo.anchor.set(0.5);

        startGame = this.add.sprite(this.world.centerX,
                               this.world.centerY + 40, 'play');
        startGame.anchor.set(0.5);
        startGame.inputEnabled = true;
        startGame.events.onInputDown.add(this.phasergame,this)

    },

    phasergame: function () {

        game.state.start('Game');
    },

    endscreen: function (){

    }
}