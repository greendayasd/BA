
// =============================================================================
// globals
// =============================================================================

const CONST_DOUBLE_JUMP = false;
const CONST_COINS = false;
const CONST_ENEMIES = false;
const CONST_ANIMATE_CHARACTER = false;
const CONST_TIME = false;

const LEVEL_COUNT = 1;

var second_jump = true;

// =============================================================================
// sprites
// =============================================================================

//
// hero sprite
//
function Hero(game, x, y) {
    // call Phaser.Sprite constructor
    Phaser.Sprite.call(this, game, x, y, 'hero');
    this.anchor.set(0.5, 0.5);

    // physic properties
    this.game.physics.enable(this);
    this.body.collideWorldBounds = true;

    this.animations.add('stop', [0]);
    this.animations.add('run', [1, 2], 8, true); // 8fps looped
    this.animations.add('jump', [3]);
    this.animations.add('fall', [4]);
}


// inherit from Phaser.Sprite
Hero.prototype = Object.create(Phaser.Sprite.prototype);
Hero.prototype.constructor = Hero;

Hero.prototype.move = function (direction) {
    const SPEED = 200;
    this.body.velocity.x = direction * SPEED;

    // update image flipping & animations
    if (this.body.velocity.x < 0) {
        this.scale.x = -1;
    }
    else if (this.body.velocity.x > 0) {
        this.scale.x = 1;
    }
};

Hero.prototype.jump = function () {
    const JUMP_SPEED = 700;
    let canJump = this.body.touching.down;

    if (this.body.touching.down){
        second_jump = true;
    }

    if (canJump) {
        this.body.velocity.y = -JUMP_SPEED;
    } else{
        if(second_jump && CONST_DOUBLE_JUMP){
            this.body.velocity.y = -(JUMP_SPEED*0.8);
            second_jump = false;
            return true;
        }
    }

    return canJump;
};

Hero.prototype.bounce = function () {
    const BOUNCE_SPEED = 200;
    this.body.velocity.y = -BOUNCE_SPEED;
};

Hero.prototype.update = function () {
    // update sprite animation, if it needs changing
    if (CONST_ANIMATE_CHARACTER){
        let animationName = this._getAnimationName();
        if (this.animations.name !== animationName) {
            this.animations.play(animationName);
        }
    }
};

Hero.prototype._getAnimationName = function () {
    let name = 'stop'; // default animation

    // jumping
    if (this.body.velocity.y < 0) {
        name = 'jump';
    }
    // falling
    else if (this.body.velocity.y >= 0 && !this.body.touching.down) {
        name = 'fall';
    }
    else if (this.body.velocity.x !== 0 && this.body.touching.down) {
        name = 'run';
    }

    return name;
};


//
// Spider (enemy)
//
function Spider(game, x, y) {
    Phaser.Sprite.call(this, game, x, y, 'spider');

    // anchor
    this.anchor.set(0.5);
    // animation
    this.animations.add('crawl', [0, 1, 2], 8, true); // 8fps, looped
    this.animations.add('die', [0, 4, 0, 4, 0, 4, 3, 3, 3, 3, 3, 3], 12);
    this.animations.play('crawl');

    // physic properties
    this.game.physics.enable(this);
    this.body.collideWorldBounds = true;
    this.body.velocity.x = Spider.SPEED;
}

Spider.SPEED = 100;

// inherit from Phaser.Sprite
Spider.prototype = Object.create(Phaser.Sprite.prototype);
Spider.prototype.constructor = Spider;

Spider.prototype.update = function () {
    // check against walls and reverse direction if necessary
    if (this.body.touching.right || this.body.blocked.right) {
        this.body.velocity.x = -Spider.SPEED; // turn left
    }
    else if (this.body.touching.left || this.body.blocked.left) {
        this.body.velocity.x = Spider.SPEED; // turn right
    }
};

Spider.prototype.die = function () {
    this.body.enable = false;

    this.animations.play('die').onComplete.addOnce(function () {
        this.kill();
    }, this);
};

// =============================================================================
// game states
// =============================================================================

PlayState = {};
var files = '/static/website/gamefiles/';
var level = '/static/website/level/';
var audio = '/static/website/audio/';


PlayState.init = function (data) {
    this.game.renderer.renderSession.roundPixels = true;

    this.keys = this.game.input.keyboard.addKeys({
        left: Phaser.KeyCode.LEFT,
        right: Phaser.KeyCode.RIGHT,
        space: Phaser.KeyCode.SPACEBAR,
        up: Phaser.KeyCode.UP
    });

    jump = function () {
        let didJump = this.hero.jump();
        if (didJump) {
            this.sfx.jump.play();
        }
    };

    this.keys.up.onDown.add(jump, this);
    this.keys.space.onDown.add(jump, this);

    this.coinPickupCount = 0;


    this.level = (data.level || 0) % LEVEL_COUNT;
};

// load game assets here
PlayState.preload = function () {
    this.game.load.json('level:0', level + 'level00.json');
    this.game.load.json('level:1', level + 'level01.json');

    //files
    this.game.load.image('background', files + 'background.png');
    this.game.load.image('ground', files + 'ground.png');
    this.game.load.image('grass:8x1', files + 'grass_8x1.png');
    this.game.load.image('grass:6x1', files + 'grass_6x1.png');
    this.game.load.image('grass:4x1', files + 'grass_4x1.png');
    this.game.load.image('grass:2x1', files + 'grass_2x1.png');
    this.game.load.image('grass:1x1', files + 'grass_1x1.png');
    this.game.load.image('invisible-wall', files + 'invisible_wall.png');
    this.game.load.image('icon:coin', files + 'coin_icon.png');

    //character
    if (CONST_ANIMATE_CHARACTER){
       this.game.load.spritesheet('hero', files + 'hero.png', 36, 42);
    }
    else{
        this.game.load.image('hero', files + 'hero_stopped.png');
    }

    //audio
    this.game.load.audio('sfx:jump', audio + 'jump.wav');
    this.game.load.audio('sfx:jump', audio + 'coin.wav');
    this.game.load.audio('sfx:stomp', audio + 'stomp.wav');
    this.game.load.audio('sfx:flag', audio + 'flag.wav');

    //sprites
    this.game.load.spritesheet('coin', files + 'coin_animated.png', 22, 22);
    this.game.load.spritesheet('spider', files + 'spider.png', 42, 32);
    this.game.load.spritesheet('flag', files + 'flag.png', 42, 66);

    //fonts
    this.game.load.image('font:numbers', files + 'numbers.png');
};

// create game entities and set up world here
PlayState.create = function () {
    // create sound entities
    this.sfx = {
        jump: this.game.add.audio('sfx:jump'),
        coin: this.game.add.audio('sfx:coin'),
        stomp: this.game.add.audio('sfx:stomp'),
        flag: this.game.add.audio('sfx:flag'),
    };

    this.game.add.image(0, 0, 'background');
    this._loadLevel(this.game.cache.getJSON(`level:${this.level}`));

    this._createHud();
};

PlayState.update = function () {
    this._handleCollisions();
    this._handleInput();

    var elapsedTime = Math.floor(this.game.time.totalElapsedSeconds());

    this.timeFont.text = `${elapsedTime}`;
    this.coinFont.text = `x${this.coinPickupCount}`;
};

PlayState._handleCollisions = function () {
    this.game.physics.arcade.collide(this.spiders, this.platforms);
    this.game.physics.arcade.collide(this.spiders, this.enemyWalls);
    this.game.physics.arcade.collide(this.hero, this.platforms);

    this.game.physics.arcade.overlap(this.hero, this.coins, this._onHeroVsCoin,
        null, this);
    this.game.physics.arcade.overlap(this.hero, this.spiders,
        this._onHeroVsEnemy, null, this);

    this.game.physics.arcade.overlap(this.hero, this.flag, this._onHeroVsFlag,
        // ignore if there is no key or the player is on air
        function (hero, flag) {
            return hero.body.touching.down;
        }, this);
};

PlayState._handleInput = function () {
    if (this.keys.left.isDown) { // move hero left
        this.hero.move(-1);
    }
    else if (this.keys.right.isDown) { // move hero right
        this.hero.move(1);
    }
    else { // stop
        this.hero.move(0);
    }
};

PlayState._loadLevel = function (data) {
    // create all the groups/layers that we need

    this.bgDecoration = this.game.add.group();
    this.platforms = this.game.add.group();

    this.coins = this.game.add.group();

    this.spiders = this.game.add.group();

    this.enemyWalls = this.game.add.group();
    this.enemyWalls.visible = false;

    // spawn all platforms
    data.platforms.forEach(this._spawnPlatform, this);

    // spawn hero and enemies
    this._spawnCharacters({hero: data.hero, spiders: data.spiders});


    // spawn important objects
    if (CONST_COINS){
      data.coins.forEach(this._spawnCoin, this);
    }

    this._spawnFlag(data.flag.x, data.flag.y);

    // enable gravity
    const GRAVITY = 1400;
    this.game.physics.arcade.gravity.y = GRAVITY;
};

PlayState._spawnPlatform = function (platform) {
    let sprite = this.platforms.create(
        platform.x, platform.y, platform.image);

    this.game.physics.enable(sprite);
    sprite.body.allowGravity = false;
    sprite.body.immovable = true;

    this._spawnEnemyWall(platform.x, platform.y, 'left');
    this._spawnEnemyWall(platform.x + sprite.width, platform.y, 'right');
};

PlayState._spawnEnemyWall = function (x, y, side) {
    let sprite = this.enemyWalls.create(x, y, 'invisible-wall');
    // anchor and y displacement
    sprite.anchor.set(side === 'left' ? 1 : 0, 1);

    // physic properties
    this.game.physics.enable(sprite);
    sprite.body.immovable = true;
    sprite.body.allowGravity = false;
};

PlayState._spawnCharacters = function (data) {


    if (CONST_ENEMIES) {
        // spawn spiders
        data.spiders.forEach(function (spider) {
            let sprite = new Spider(this.game, spider.x, spider.y);
            this.spiders.add(sprite);
        }, this);
    }
    // spawn hero
    this.hero = new Hero(this.game, data.hero.x, data.hero.y);
    this.game.add.existing(this.hero);
};

PlayState._spawnCoin = function (coin) {
    let sprite = this.coins.create(coin.x, coin.y, 'coin');
    sprite.anchor.set(0.5, 0.5);

    this.game.physics.enable(sprite);
    sprite.body.allowGravity = false;

    sprite.animations.add('rotate', [0, 1, 2, 1], 6, true); // 6fps, looped
    sprite.animations.play('rotate');
};

PlayState._onHeroVsCoin = function (hero, coin) {
    this.sfx.coin.play();
    coin.kill();
    this.coinPickupCount++;
};

PlayState._onHeroVsEnemy = function (hero, enemy) {
    if (hero.body.velocity.y > 0) { // kill enemies when hero is falling
        hero.bounce();
        enemy.die();
        this.sfx.stomp.play();
    }
    else { // game over -> restart the game
        this.sfx.stomp.play();
        this.game.state.restart(true, false, {level: this.level});
    }
};

PlayState._onHeroVsFlag = function (hero, flag) {
    this.sfx.flag.play();
    this.game.state.restart(true, false, { level: this.level + 1 });
    // TODO: Winscreen

};

PlayState._createHud = function () {
    const NUMBERS_STR = '0123456789X ';
    this.timeFont = this.game.add.retroFont('font:numbers', 20, 26,
        NUMBERS_STR, 6);

    this.coinFont = this.game.add.retroFont('font:numbers', 20, 26,
        NUMBERS_STR, 6);


    let coinIcon = this.game.make.image(0, 0, 'icon:coin');
    let coinScoreImg = this.game.make.image(coinIcon.x + coinIcon.width,
        coinIcon.height / 2, this.coinFont);
    coinScoreImg.anchor.set(0, 0.5);

    this.hud = this.game.add.group();
    var space = 0;
    if (CONST_COINS){
        this.hud.add(coinIcon);
        this.hud.add(coinScoreImg);
        space += coinIcon.x + coinIcon.width + 65;
    }

    if (CONST_TIME){
        let timeImg = this.game.make.image(space,
        coinIcon.height / 2, this.timeFont);
        timeImg.anchor.set(0, 0.5);

        this.hud.add(timeImg);

    }

    this.hud.position.set(10, 10);
};

PlayState._spawnFlag = function (x, y) {
    this.flag = this.bgDecoration.create(x, y, 'flag');
    this.flag.anchor.setTo(0.5, 1);
    this.game.physics.enable(this.flag);
    this.flag.body.allowGravity = false;
};


// =============================================================================
// entry point
// =============================================================================

window.onload = function () {
    var game = new Phaser.Game(960, 600, Phaser.AUTO, 'crowdjump');
    game.state.add('play', PlayState);
    game.state.start('play', true, false, {level: 0});
};