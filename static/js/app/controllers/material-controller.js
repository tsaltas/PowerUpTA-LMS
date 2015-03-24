'use strict';

/* Materials Module Controllers */

var materialControllers = angular.module('materialControllers', []);

materialControllers.controller('NewMaterialModalCtrl', ['$scope'
    , '$modalInstance'
    , 'activityID'
    , 'Material'
    , function ($scope
        , $modalInstance
        , activityID
        , Material
    ) {

    $scope.newMaterial = new Material();

    $scope.save = function() {
        // assign new material object to the correct activity
        $scope.newMaterial.activities = [activityID];

        return $scope.newMaterial.$save().then(function(result) {
            $modalInstance.close(result);
        }).then(function() {
            return $scope.newMaterial = new Material();
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