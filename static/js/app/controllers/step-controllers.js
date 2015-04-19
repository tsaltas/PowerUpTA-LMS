'use strict';

/* Step Module Controllers */

var stepControllers = angular.module('stepControllers', []);

stepControllers.controller('NewStepModalCtrl', ['$scope'
    , '$modalInstance'
    , 'activityID'
    , 'Step'
    , function ($scope
        , $modalInstance
        , activityID
        , Step
    ) {

    $scope.newStep = new Step();

    $scope.save = function() {
        // assign new step object to the correct activity
        $scope.newStep.activity = [activityID];

        return $scope.newStep.$save().then(function(result) {
            $modalInstance.close(result);
        }).then(function() {
            return $scope.newStep = new Step();
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

stepControllers.controller('ActivityStepsModalCtrl', ['$scope'
    , '$modalInstance'
    , '$modal'
    , 'Step'
    , 'activityID'
    , 'steps'
    , function ($scope
        , $modalInstance
        , $modal
        , Step
        , activityID
        , steps
    ) {
        
    // steps associated with the appropriate activity
    $scope.steps = steps;

    // open modal window to create new step
    $scope.newStep = function (size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/new-step.html',
            controller: 'NewStepModalCtrl',
            size: size,
            resolve: {
                activityID: function () {
                    return activityID;
                }
            }
        });

        // add newly created resource to list on the page (without refresh)
        modalInstance.result.then(function (newStep) {
            $scope.steps.push(newStep);
        });
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);