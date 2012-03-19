var rpc = require('../src/jsonrpc');
var events = require('events');

var server = new rpc.Server();

server.enableAuth("myuser", "secret123");

/* Create two simple functions */
function add(args, opts, callback) {
  callback(null, args[0]+args[1]);
}

function multiply(args, opts, callback) {
  callback(null, args[0]*args[1]);
}

/* Expose those methods */
server.expose('add', add);
server.expose('multiply', multiply);

/* We can expose entire modules easily */
var math = {
  power: function(args, opts, callback) {
    callback(null, Math.pow(args[0], args[1]));
  },
  sqrt: function(args, opts, callback) {
    callback(null, Math.sqrt(args[0]));
  }
};
server.exposeModule('math', math);

/* By using a callback, we can delay our response indefinitely, leaving the
 request hanging until the callback emits success. */
var delayed = {
  echo: function(args, opts, callback) {
    var data = args[0];
    var delay = args[1];
    setTimeout(function() {
      callback(null, data);
    }, delay);
  },

  add: function(args, opts, callback) {
    var first = args[0];
    var second = args[1];
    var delay = args[2];
    setTimeout(function() {
      callback(null, first + second);
    }, delay);
  }
}

server.exposeModule('delayed', delayed);

// Create a message bus with random events on it
var firehose = new events.EventEmitter();
(function emitFirehoseEvent() {
  firehose.emit('foobar', {data: 'random '+Math.random()});
  setTimeout(arguments.callee, 200+Math.random()*3000);
})();

var listen = function (args, opts, callback) {
  function handleFirehoseEvent(event) {
    opts.call('event', event.data);
  };
  firehose.on('foobar', handleFirehoseEvent);
  opts.stream(function () {
    console.log('connection ended');
    firehose.removeListener('foobar', handleFirehoseEvent);
  });
  callback(null);
};

server.expose('listen', listen);

/* HTTP server on port 8088 */
server.listen(8088, 'localhost');

/* Raw socket server on port 8089 */
server.listenRaw(8089, 'localhost');
