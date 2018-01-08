var Crowdjump = {};

Crowdjump.Menu = function(game){
    var startGame;
    var endGame;
};

Crowdjump.Menu.prototype = {
    create: function(){
        logo = this.add.sprite(this.world.centerX,
                               this.world.centerY -80, 'logo');
        logo.anchor.set(0.5);
        logo.inputEnabled = true;
        logo.events.onInputDown.add(this.start, {'points': 1}, this);


        startGame = this.add.text(this.world.centerX - 50, this.world.centerY + 30, 'My score is 0', {fill: '#ffffff'});
        startGame.inputEnabled = true;
        startGame.events.onInputDown.add(this.start, {'points': 1}, this);

        this.game.stage.backgroundColor = '#1948cd';
    },
    start: function(){
        startGame.text = 'My score is '+this.points++;
   },
    update: function(){
    },

    phasergame: function () {

        this.state.start('Game');
    },

    endscreen: function (){
        this.state.start('Endscreen');
    }
}