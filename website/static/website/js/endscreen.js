var Crowdjump = {};

Crowdjump.Endscreen = function(game){
    var replay;
    var score;
    var info;
};

Crowdjump.Endscreen.prototype = {
    create: function () {
        replay = this.add.text(this.world.centerX,
                                this.world.centerY, 'Replay?', {fill: '#000000'});
        replay.inputEnabled = true;
        replay.events.onInputDown.add(this.go, this);

        var scoreText = "Congratulations, you beat the level in " + this.game.time.totalElapsedSeconds() + " seconds!";
        score = this.add.text(30,30, scoreText);
    },

    go: function(){
        this.state.start('Game');
    }
}