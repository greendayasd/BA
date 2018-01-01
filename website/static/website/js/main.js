
PlayState = {};
var files = '/static/website/gamefiles/';
var level = '/static/website/level/';

// load game assets here
PlayState.preload = function () {
    this.game.load.json('level:1', level + 'level01.json');
    this.game.load.image('background', files + 'background.png');

    this.game.load.image('ground', files + 'ground.png');
    this.game.load.image('grass:8x1', files + 'grass_8x1.png');
    this.game.load.image('grass:6x1', files + 'grass_6x1.png');
    this.game.load.image('grass:4x1', files + 'grass_4x1.png');
    this.game.load.image('grass:2x1', files + 'grass_2x1.png');
    this.game.load.image('grass:1x1', files + 'grass_1x1.png');
};

// create game entities and set up world here
PlayState.create = function () {
    this.game.add.image(0, 0, 'background');
    this._loadLevel(this.game.cache.getJSON('level:1'));
};

PlayState._loadLevel = function (data) {
    // spawn all platforms
    data.platforms.forEach(this._spawnPlatform, this);
};

PlayState._spawnPlatform = function (platform) {
    this.game.add.sprite(platform.x, platform.y, platform.image);
};

window.onload = function () {
    let game = new Phaser.Game(960, 600, Phaser.AUTO, 'game');
    game.state.add('play', PlayState);
    game.state.start('play');
};