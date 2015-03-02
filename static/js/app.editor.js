app = angular.module('lms.app.editor', ['lms.api', 'lms.app.curricula']);

app.controller('EditorCtrl', ['$scope', 'Curriculum', 'Activity', function($scope, Curriculum, Activity) {
    // TODO: Make this pull options from Django model instead of hard-coding them
    $scope.grades = [{
        id: 0,
        value: "K",
    }, {
    	id: 1,
        value: "1",
    }, {
        id: 2,
        value: "2",
    }, {
        id: 3,
        value: "3",
    },{
        id: 4,
        value: "4",
    },{
        id: 5,
        value: "5",
	},{
        id: 6,
        value: "6",
    },{
        id: 7,
        value: "7",
    },{
        id: 8,
        value: "8",
	},{
        id: 9,
        value: "9",
    },{
        id: 10,
        value: "10",
    },{
        id: 11,
        value: "11",
    },{
        id: 12,
        value: "12",
    }]; 

    // TODO: Initialize activities to empty list and make sure HTML does not render until the data is fetched
    // Otherwise while loading you see some empty template tags flash
    $scope.activities = Activity.query();

    $scope.newCurriculum = new Curriculum();
    return $scope.save = function() {
        // if the user selected an activity in the input form, let's assign it as the 1st activity in the curriculum
        if ($scope.newCurriculum.activities) {
            $scope.newCurriculum.activities = [{"activity":$scope.newCurriculum.activities, "number":1}];
        }

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
}]);