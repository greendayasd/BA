// Global Variables

var game = new Phaser.Game(960, 600, Phaser.AUTO);



    const CONST_DOUBLE_JUMP = false;
    const CONST_COINS = false;
    const CONST_ENEMIES = false;
    const CONST_ANIMATE_CHARACTER = false;
    const CONST_TIME = false;

    const LEVEL_COUNT = 1;

    game.state.add('Boot', Crowdjump.Boot);
    game.state.add('Preloader', Crowdjump.Preloader);
    game.state.add('Startmenu', Crowdjump.Menu);
    game.state.add('Game', Crowdjump.Game);
    game.state.start('Boot');

// var Crowdjump = {};
//
//
// Crowdjump.Main = function(game){
//     var logo;
//     var startGame;
//     game.state.add('Startmenu', Crowdjump.Menu);
//     game.state.add('Game', Crowdjump.Game);
//     game.state.add('Endscreen', Crowdjump.Endscreen);
// };
//
//
// Crowdjump.Main.prototype = {
//    preload: function(){
//       var files = '/static/website/gamefiles/';
//       var level = '/static/website/level/';
//       var audio = '/static/website/audio/';
//       var images = '/static/website/images/';
//
//       this.load.image('logo', images + 'logo.png');
//    },
//    create: function(){
//         logo = this.add.sprite(this.world.centerX,
//                                this.world.centerY -80, 'logo');
//         logo.anchor.set(0.5);
//         logo.inputEnabled = true;
//         logo.events.onInputDown.add(this.start, {'points': 1}, this);
//
//
//         startGame = this.add.text(this.world.centerX - 50, this.world.centerY + 30, 'My score is 0', {fill: '#ffffff'});
//         startGame.inputEnabled = true;
//         startGame.events.onInputDown.add(this.start, {'points': 1}, this);
//
//         this.game.stage.backgroundColor = '#1948cd';
//     },
//     start: function(){
//         startGame.text = 'My score is '+this.points++;
//    },
//     update: function(){
//     }
// };
//
