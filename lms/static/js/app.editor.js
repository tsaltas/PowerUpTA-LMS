app = angular.module('lms.app.editor', ['lms.api', 'lms.app.curricula', 'lms.app.activities']);

app.controller('EditorCtrl', ['$scope', 'Curriculum', 'Activity', function($scope, Curriculum, Activity) {
    // TODO: Make this pull options from Django model instead of hard-coding them
    $scope.grades = [{
        id: 0,
        value: "K",
    }, {
    	id: 1,
        value: "First",
    }, {
        id: 2,
        value: "Second",
    }, {
        id: 3,
        value: "Third",
    },{
        id: 4,
        value: "Fourth",
    },{
        id: 5,
        value: "Fifth",
	},{
        id: 6,
        value: "Sixth",
    },{
        id: 7,
        value: "Seventh",
    },{
        id: 8,
        value: "Eighth",
	},{
        id: 9,
        value: "Ninth",
    },{
        id: 10,
        value: "Tenth",
    },{
        id: 11,
        value: "Eleventh",
    },{
        id: 12,
        value: "Twelfth",
    }]; 

    $scope.activities = []
    $scope.activities = Activity.query();

    $scope.newCurriculum = new Curriculum();
    return $scope.save = function() {
      return $scope.newCurriculum.$save().then(function(result) {
        return $scope.curricula.push(result);
      }).then(function() {
        return $scope.newCurriculum = new Curriculum();
      }).then(function() {
        return $scope.errors = null;
      }, function(rejection) {
        return $scope.errors = rejection.data;
      });
    };
  }
]);