var util = require('util');

var TEST = module.exports = {
  passed: 0,
  failed: 0,
  assertions: 0,

  output: "",

  test: function (desc, block) {
    var result = '?',
        _boom = null;

    TEST.output = "";
    try {
      TEST.output += "  " + desc + " ...";
      block();
      result = '.';
    } catch(boom) {
      if ( boom == 'FAIL' ) {
        result = 'F';
      } else {
        result = 'E';
        _boom = boom;
        TEST.output += boom.toString();
      }
    }
    if ( result == '.' ) {
      process.stdout.write(TEST.output + " OK\n");
      TEST.passed += 1;
    } else {
      process.stdout.write(TEST.output + " FAIL\n");
      process.stdout.write(TEST.output.replace(/^/, "      ") + "\n");
      TEST.failed += 1;
      if ( _boom ) throw _boom;
    }
  },

  assert: function (value, desc) {
    TEST.assertions += 1;
    if ( desc ) TEST.output += "ASSERT: " + desc;
    if ( !value ) throw 'FAIL';
  },

  assert_equal: function (expect, is) {
    assert(
      expect == is,
      util.inspect(expect) + " == " + util.inspect(is)
    );
  },

  assert_boom: function (message, block) {
    var error = null;
    try { block(); }
    catch (boom) { error = boom; }

    if ( !error ) {
      TEST.output += 'NO BOOM';
      throw 'FAIL';
    }
    if ( error != message ) {
      TEST.output += 'BOOM: ' + util.inspect(error) +
                     ' [' + util.inspect(message) + ' expected]';
      throw 'FAIL';
    }
  },

  extend: function (scope) {
    Object.keys(TEST).forEach(function (key) {
      scope[key] = TEST[key];
    });
  }
};

process.addListener('exit', function (code) {
  if ( !TEST.exit ) {
    TEST.exit = true;
    console.log("" + TEST.passed + " passed, " + TEST.failed + " failed");
    if ( TEST.failed > 0 ) { process.exit(1) };
  }
});
