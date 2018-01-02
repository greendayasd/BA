// Global Variables
var
  game = new Phaser.Game(960, 600, Phaser.AUTO, 'crowdjump'),
  Main = function () {},
  gameOptions = {
    playSound: true,
    playMusic: true
  },
  musicPlayer;




Main.prototype = {

  preload: function () {

    var scripts = '/static/website/js/';
    var files = '/static/website/gamefiles/';
    var libs = '/static/website/libs/';

    game.load.image('loading',  files + 'loading.png');
    game.load.script('splash',  scripts + 'splash.js');

    game.load.script('polyfill',   libs + 'polyfill.js');
    game.load.script('utils',   lib  + 'utils.js');
  },

  create: function () {
    game.state.add('splash', splash);
    game.state.start('splash');
  }

};

game.state.add('Main', Main);
game.state.start('Main');
