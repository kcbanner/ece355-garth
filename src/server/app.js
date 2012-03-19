var rpc = require('jsonrpc2');

var server = new rpc.Server();
var event_log = [];

function log_event(args, opt, callback) {
  event_log.push(args[0]);
  callback(null, 'OK');
};

function get_events(args, opt, callback) {
  var event_log_json = JSON.stringify(event_log);
  callback(null, event_log_json);
};

server.expose('log_event', log_event);
server.expose('get_events', get_events);
server.listen(3000);