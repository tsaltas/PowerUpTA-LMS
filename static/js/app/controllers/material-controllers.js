'use strict';

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

materialControllers.controller('ActivityMaterialsModalCtrl', ['$scope'
    , '$modalInstance'
    , '$modal'
    , 'Material'
    , 'activityID'
    , 'materials'
    , function ($scope
        , $modalInstance
        , $modal
        , Material
        , activityID
        , materials
    ) {
        
    // resources associated with the appropriate activity
    $scope.materials = materials;

    // open modal window to create new material
    $scope.newMaterial = function (size) {
            var modalInstance = $modal.open({
            templateUrl: 'static/partials/new-material.html',
            controller: 'NewMaterialModalCtrl',
            size: size,
            resolve: {
                activityID: function () {
                    return activityID;
                }
            }
        });

        // add newly created material to list on the page (without refresh)
        modalInstance.result.then(function (newMaterial) {
            $scope.materials.push(newMaterial);
        });
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);