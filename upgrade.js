var grasp = require('grasp');
var glob = require('glob');
var fs = require('fs');
var _ = require('underscore');
var inquirer = require("inquirer");
var Lazy = require("lazy");

var dir='../../../Etsyweb/htdocs/assets/js/seller-platform';


approveEdit = function(edit) {
  var targetPath = edit[0], targetResult = edit[1];
  console.log(targetPath);
  console.log(targetResult)


  inquirer.prompt(
    {
      type: "input",
      name: "change",
      message: "Accept change: [y,n,e,q]",
      validate: function(result) {
        return result.match(/[yneq]/) != null
      }
    }
  , function( answer ) {
    var change = answer.change;
    if (change == 'y') {
      console.log('will do edit');
      nextEdit();
    } else if (change == 'n') {
    } else if (change == 'e') {
    } else if (change == 'q') {
    } else {
      console.log('oops')
    }

  });
}

function nextEdit() {
  var nextResult = flatResults.shift();
  if (!nextResult) {
      return;
  }

  approveEdit(nextResult);
}

results = {};

graspResult = function(obj) {
  var targetPath = obj[0], result = obj[1];
  results[targetPath] = result;
};

graspDone = function() {
  flatResults = [];
   _.each(results, function(targetResults, targetPath) {
    flatResults = flatResults.concat(_.map(targetResults, function(targetResult) {
      return [targetPath, targetResult];
    }));
  });

  _.flatten(flatResults, 1);

  nextEdit();
};

var output = grasp({
  args: '-e "__.triggerMethod(__, _$)" -r ' + dir,
  callback: graspResult,
  data: true,
  exit: graspDone
});
