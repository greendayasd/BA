// Global Variables
var game = new Phaser.Game(960, 600, Phaser.AUTO)
game.state.add('Startmenu', Crowdjump.Menu);
game.state.add('Game', Crowdjump.Game);
game.state.add('Endscreen', Crowdjump.Endscreen);


var Crowdjump = {};

Crowdjump.Main = function(game){
    var logo;
    var text;
};

Crowdjump.Main.prototype = {
   preload: function(){
      var files = '/static/website/gamefiles/';
      var level = '/static/website/level/';
      var audio = '/static/website/audio/';
      var images = '/static/website/images/';

      this.load.image('logo', images + 'logo.png');
   },
   create: function(){
        logo = this.add.sprite(this.world.centerX,
                               this.world.centerY, 'logo');
        logo.anchor.set(0.5);
        text = this.add.text(100, 10, 'My score is 0', {fill: '#ffffff'});
        logo.inputEnabled = true;
        logo.events.onInputDown.add(this.score, {'points': 1}, this);
    },
    score: function(){
        text.text = 'My score is '+this.points++;
   },
    update: function(){
       logo.rotation += 0.01;
    }
};


// game.state.start('Startmenu');