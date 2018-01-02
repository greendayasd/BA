var Splash = function () {};

Splash.prototype = {

  loadScripts: function () {

    var path = '/static/website/js/';
    game.load.script('WebFont', path + 'webfontloader.js');
    game.load.script('gamemenu',path + 'gamemenu.js');
    game.load.script('game', path + 'game.js');
    game.load.script('gameover', path + 'gameover.js');
  },

  loadBgm: function () {
    // thanks Kevin Macleod at http://incompetech.com/
    var path = '/static/website/audio/';
  },


  loadImages: function () {
    var path = '/static/website/gamefiles/';
    game.load.image('menu-bg', path + 'background.png');
    game.load.image('gameover-bg', path + 'background.png');
  },

  loadFonts: function () {
    var path = '/static/website/css/';
    // WebFontConfig = {
    //   custom: {
    //     families: ['TheMinion'],
    //     urls: ['assets/style/theminion.css']
    //   }
    // }
  },

  init: function () {
    this.loadingBar = game.make.sprite(game.world.centerX-(387/2), 400, "loading");
    this.status     = game.make.text(game.world.centerX, 380, 'Loading...', {fill: 'white'});
  },

  preload: function () {
    game.add.existing(this.loadingBar);
    game.add.existing(this.status);
    this.load.setPreloadSprite(this.loadingBar);

    this.loadScripts();
    this.loadImages();
    this.loadFonts();
    this.loadBgm();

  },

  addGameStates: function () {

    game.state.add("gamemenu",gamemenu);
    game.state.add("game",game);
    game.state.add("gameover",gameover);
  },

  addGameMusic: function () {
    // music = game.add.audio('dangerous');
    // music.loop = true;
    // music.play();
  },

  create: function() {
    this.status.setText('Ready!');
    this.addGameStates();
    this.addGameMusic();

    setTimeout(function () {
      game.state.start("GameMenu");
    }, 1000);
  }
};
