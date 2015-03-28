'use strict';

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

resourceControllers.controller('ActivityResourcesModalCtrl', ['$scope'
    , '$modalInstance'
    , '$modal'
    , 'Resource'
    , 'activityID'
    , 'resources'
    , function ($scope
        , $modalInstance
        , $modal
        , Resource
        , activityID
        , resources
    ) {
        
    // resources associated with the appropriate activity
    $scope.resources = resources;

    // open modal window to create new resource
    $scope.newResource = function (size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/new-resource.html',
            controller: 'NewResourceModalCtrl',
            size: size,
            resolve: {
                activityID: function () {
                    return activityID;
                }
            }
        });

        // add newly created resource to list on the page (without refresh)
        modalInstance.result.then(function (newResource) {
            $scope.resources.push(newResource);
        });
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);