function KeyboardInputManager() {
  this.events = {};

  if (window.navigator.msPointerEnabled) {
    //Internet Explorer 10 style
    this.eventTouchstart    = "MSPointerDown";
    this.eventTouchmove     = "MSPointerMove";
    this.eventTouchend      = "MSPointerUp";
  } else {
    this.eventTouchstart    = "touchstart";
    this.eventTouchmove     = "touchmove";
    this.eventTouchend      = "touchend";
  }

  this.moves = [];
  this.pseudoRandTiles = [];
  this.logLoaded = false;
  this.logI = 0;

  var url = new URL(window.location.href);
  var logfilepath = url.searchParams.get("log");

  this.speed = parseInt(url.searchParams.get("speed"));

  Papa.parse("/" + logfilepath, {
                  download: true,
                  header: true,
                  complete: (function(results) {
                      log = results.data
                      for (var i = 0, len = log.length; i < len; i++) {

                        if(i == 0) {
                          for(var j = 0; j < 16; j++) {
                            var value = parseInt(parseInt(log[i]["Val" + j]));
                            var x = j % 4;
                            var y = Math.floor(j / 4);
                            if (value != 0) {
                              this.emit("addPseudoRandomTile", {cell: { x: x, y: y }, value:value});
                            }
                          }
                        }

                        var move = -1;
                        if (log[i].Move == "UP") {
                          move = 0;
                        } else if (log[i].Move == "RIGHT") {
                          move = 1;
                        } else if (log[i].Move == "DOWN") {
                          move = 2;
                        } else {
                          move = 3;
                        }
                        this.moves.push(move);

                        var pos = parseInt(log[i].RandTilePos);
                        var x = pos % 4;
                        var y = Math.floor(pos / 4);
                        this.pseudoRandTiles.push({x: x, y:y, value: parseInt(log[i]["Val" + log[i].RandTilePos])});
                      }
                      this.logLoaded = true;

                  }).bind(this)
              });
  
  setInterval(this.nextStep.bind(this), this.speed);
  this.listen();
}

KeyboardInputManager.prototype.on = function (event, callback) {
  if (!this.events[event]) {
    this.events[event] = [];
  }
  this.events[event].push(callback);
};

KeyboardInputManager.prototype.emit = function (event, data) {
  var callbacks = this.events[event];
  if (callbacks) {
    callbacks.forEach(function (callback) {
      callback(data);
    });
  }
};

KeyboardInputManager.prototype.nextStep = function() {

  var self = this;

  if (self.logLoaded) {
    if(self.logI == 0) {
      // self.emit("addPseudoRandomTile", {cell: { x: 3, y: 3 }, value:2});
    } else {
      console.log({x: self.pseudoRandTiles[self.logI].x, y: self.pseudoRandTiles[self.logI].y}, self.pseudoRandTiles[self.logI].value)
      self.emit("moveAndAddPseudoRandomTile", {direction: self.moves[self.logI-1], randCell:{x: self.pseudoRandTiles[self.logI].x, y: self.pseudoRandTiles[self.logI].y}, randValue: self.pseudoRandTiles[self.logI].value});
    }
    self.logI += 1;
  }

};

KeyboardInputManager.prototype.listen = function () {
  var self = this;

  var map = {
    38: 0, // Up
    39: 1, // Right
    40: 2, // Down
    37: 3, // Left
    75: 0, // Vim up
    76: 1, // Vim right
    74: 2, // Vim down
    72: 3, // Vim left
    87: 0, // W
    68: 1, // D
    83: 2, // S
    65: 3  // A
  };

  // Respond to direction keys
  document.addEventListener("keydown", function (event) {
    var modifiers = event.altKey || event.ctrlKey || event.metaKey ||
                    event.shiftKey;
    var mapped    = map[event.which];

    if (!modifiers) {
      if (mapped !== undefined) {
        event.preventDefault();
        self.nextStep();

      }
    }

    // R key restarts the game
    if (!modifiers && event.which === 82) {
      self.restart.call(self, event);
    }
  });

  // Respond to button presses
  this.bindButtonPress(".retry-button", this.restart);
  this.bindButtonPress(".restart-button", this.restart);
  this.bindButtonPress(".keep-playing-button", this.keepPlaying);

  // Respond to swipe events
  var touchStartClientX, touchStartClientY;
  var gameContainer = document.getElementsByClassName("game-container")[0];

  gameContainer.addEventListener(this.eventTouchstart, function (event) {
    if ((!window.navigator.msPointerEnabled && event.touches.length > 1) ||
        event.targetTouches.length > 1) {
      return; // Ignore if touching with more than 1 finger
    }

    if (window.navigator.msPointerEnabled) {
      touchStartClientX = event.pageX;
      touchStartClientY = event.pageY;
    } else {
      touchStartClientX = event.touches[0].clientX;
      touchStartClientY = event.touches[0].clientY;
    }

    event.preventDefault();
  });

  gameContainer.addEventListener(this.eventTouchmove, function (event) {
    event.preventDefault();
  });

  gameContainer.addEventListener(this.eventTouchend, function (event) {
    if ((!window.navigator.msPointerEnabled && event.touches.length > 0) ||
        event.targetTouches.length > 0) {
      return; // Ignore if still touching with one or more fingers
    }

    var touchEndClientX, touchEndClientY;

    if (window.navigator.msPointerEnabled) {
      touchEndClientX = event.pageX;
      touchEndClientY = event.pageY;
    } else {
      touchEndClientX = event.changedTouches[0].clientX;
      touchEndClientY = event.changedTouches[0].clientY;
    }

    var dx = touchEndClientX - touchStartClientX;
    var absDx = Math.abs(dx);

    var dy = touchEndClientY - touchStartClientY;
    var absDy = Math.abs(dy);

    if (Math.max(absDx, absDy) > 10) {
      // (right : left) : (down : up)
      self.emit("move", absDx > absDy ? (dx > 0 ? 1 : 3) : (dy > 0 ? 2 : 0));
    }
  });
};

KeyboardInputManager.prototype.restart = function (event) {
  event.preventDefault();
  this.emit("restart");
};

KeyboardInputManager.prototype.keepPlaying = function (event) {
  event.preventDefault();
  this.emit("keepPlaying");
};

KeyboardInputManager.prototype.bindButtonPress = function (selector, fn) {
  var button = document.querySelector(selector);
  button.addEventListener("click", fn.bind(this));
  button.addEventListener(this.eventTouchend, fn.bind(this));
};