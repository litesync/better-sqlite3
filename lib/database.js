'use strict';
const fs = require('fs');
const path = require('path');
const util = require('./util');

const {
	Database: CPPDatabase,
	setErrorConstructor,
} = require('bindings')('better_sqlite3.node');

function Database(filenameGiven, options) {
	if (new.target == null) {
		return new Database(filenameGiven, options);
	}

	// Apply defaults
	let buffer;
	if (Buffer.isBuffer(filenameGiven)) {
		buffer = filenameGiven;
		filenameGiven = ':memory:';
	}
	if (filenameGiven == null) filenameGiven = '';
	if (options == null) options = {};

	// Validate arguments
	if (typeof filenameGiven !== 'string') throw new TypeError('Expected first argument to be a string');
	if (typeof options !== 'object') throw new TypeError('Expected second argument to be an options object');
	if ('readOnly' in options) throw new TypeError('Misspelled option "readOnly" should be "readonly"');
	if ('memory' in options) throw new TypeError('Option "memory" was removed in v7.0.0 (use ":memory:" filename instead)');

	// Interpret options
	const filename = filenameGiven.trim();
	const anonymous = filename === '' || filename === ':memory:';
	const readonly = util.getBooleanOption(options, 'readonly');
	const fileMustExist = util.getBooleanOption(options, 'fileMustExist');
	const timeout = 'timeout' in options ? options.timeout : 5000;
	const verbose = 'verbose' in options ? options.verbose : null;

	// Validate interpreted options
	if (readonly && anonymous && !buffer) throw new TypeError('In-memory/temporary databases cannot be readonly');
	if (!Number.isInteger(timeout) || timeout < 0) throw new TypeError('Expected the "timeout" option to be a positive integer');
	if (timeout > 0x7fffffff) throw new RangeError('Option "timeout" cannot be greater than 2147483647');
	if (verbose != null && typeof verbose !== 'function') throw new TypeError('Expected the "verbose" option to be a function');

	// Make sure the specified directory exists
	//if (!anonymous && !fs.existsSync(path.dirname(filename))) {
	//	throw new TypeError('Cannot open database because the directory does not exist');
	//}

	Object.defineProperties(this, {
		[util.cppdb]: { value: new CPPDatabase(filename, filenameGiven, anonymous, readonly, fileMustExist, timeout, verbose || null, buffer || null) },
		...wrappers.getters,
	});
}

const wrappers = require('./methods/wrappers');
Database.prototype.prepare = wrappers.prepare;
Database.prototype.transaction = require('./methods/transaction');
Database.prototype.pragma = require('./methods/pragma');
Database.prototype.backup = require('./methods/backup');
Database.prototype.serialize = require('./methods/serialize');
Database.prototype.function = require('./methods/function');
Database.prototype.aggregate = require('./methods/aggregate');
Database.prototype.table = require('./methods/table');
Database.prototype.loadExtension = wrappers.loadExtension;
Database.prototype.exec = wrappers.exec;
Database.prototype.close = wrappers.close;
Database.prototype.defaultSafeIntegers = wrappers.defaultSafeIntegers;
Database.prototype.unsafeMode = wrappers.unsafeMode;
Database.prototype[util.inspect] = require('./methods/inspect');

// LiteSync functions

const process = require('process');
const udp = require('dgram');

Database.prototype.is_ready = function() {
  var db = this;
  var res = db.prepare('PRAGMA sync_status').get();
  var status = JSON.parse(res.sync_status);
  return status.db_is_ready;
}

/*
Database.prototype.onReady = function(callback) {
  var db = this;
  const timer = setInterval(function(){
    if (db.is_ready()) {
      clearInterval(timer);
      callback();
    }
  }, 250);
}
*/

Database.prototype.on = function(name,callback) {

  var db = this

  if (!(name=='ready' || name=='sync')) {
    throw 'invalid event name: ' + name
  }

  if (!db.events) db.events = {}
  db.events['on_' + name] = callback

  if (!db.udp_socket) {
    db.udp_socket = udp.createSocket('udp4');

    db.udp_socket.on('message',function(msg,info){
      var event = msg.toString()
      var event_callback = db.events[event]
      if (event_callback) {
        event_callback()
        // the 'on_ready' callback should be called just once
        if (event=='on_ready') {
          delete db.events[event]
        }
      }
    });

    db.udp_socket.on('listening',function(){
      let address = db.udp_socket.address();
      let port = address.port;
      db.exec('PRAGMA enable_notifications="udp:' + port + '"')
    });

    db.udp_socket.on('error',function(error){
      db.udp_socket.close();
    });

    // binds to an available port
    db.udp_socket.bind(0);
  }

  if (name=='ready' && db.is_ready()) {
    process.nextTick(callback);
    // the 'on_ready' callback should be called just once
    delete db.events['on_ready']
  }

}

module.exports = Database;
setErrorConstructor(require('./sqlite-error'));
