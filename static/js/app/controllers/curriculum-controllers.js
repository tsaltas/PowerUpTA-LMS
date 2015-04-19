'use strict';

/* Curriculum Module Controllers */

var curriculumControllers = angular.module('curriculumControllers', []);

curriculumControllers.controller('NewCurrModalCtrl', ['$scope'
    , '$modalInstance'
    , 'Curriculum'
    , 'Activity'
    , 'addActivityService'
    , function ($scope
        , $modalInstance
        , Curriculum
        , Activity
        , addActivityService
    ) {
    console.log("Inside new curriculum modal window controller.");
    // list of activities for new curriculum form
    $scope.activities = Activity.query();

    // list of possible grades for new curriculum form
    $scope.grades = [{
        id: 0,
        value: "K"
    }];
    for (var i = 1; i <= 12; i++) { 
        var newGrade = {
            id: i,
            value: i.toString()
        };
        $scope.grades.push(newGrade);
    };
    
    $scope.newCurriculum = new Curriculum();

    $scope.save = function() {
        // Save new curriculum to DB
        console.log("Saving new curriculum to database.");
        return $scope.newCurriculum.$save().then(function(result) {
            // If the user selected an activity in the input form
            if ($scope.activity_rels) {
                // Add activity to curriculum
                result = addActivityService.addActivity(result, $scope.activity_rels)
            }
            // Create empty tag list
            result.tags = [];
            $modalInstance.close(result);
        }).then(function() {
            return $scope.newCurriculum = new Curriculum();
        }).then(function() {
            return $scope.errors = null;
        }, function(rejection) {
            return $scope.errors = rejection.data;
        });
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);