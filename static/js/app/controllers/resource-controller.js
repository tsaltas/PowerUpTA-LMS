'use strict';

/* Resources Module Controllers */

var resourceControllers = angular.module('resourceControllers', []);

resourceControllers.controller('NewResourceModalCtrl', ['$scope'
    , '$modalInstance'
    , 'activityID'
    , 'Resource'
    , function ($scope
        , $modalInstance
        , activityID
        , Resource
    ) {

    $scope.newResource = new Resource();

    $scope.save = function() {
        // assign new resource object to the correct activity
        $scope.newResource.activities = [activityID];

        return $scope.newResource.$save().then(function(result) {
            $modalInstance.close(result);
        }).then(function() {
            return $scope.newResource = new Resource();
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