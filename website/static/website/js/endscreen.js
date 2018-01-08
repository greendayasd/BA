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

        score = this.add.text();
    },

    go: function(){
        this.state.start('Game');
    }
}