'use strict';

/* Activity Module Controllers */

var activityControllers = angular.module('activityControllers', []);

activityControllers.controller('NewActivityModalCtrl', ['$scope'
    , '$modalInstance'
    , 'Activity'
    , 'Tag'
    , 'curriculumID'
    , 'number'
    , function ($scope
        , $modalInstance
        , Activity
        , Tag
        , curriculumID
        , number
    ) {

    console.log("Inside new activity modal window controller.");
    // list of tags for new activity form
    $scope.tags = [];
    $scope.tags = Tag.query();

    // list of possible categories for new activity form
    $scope.categories = [
        {
            code: "OFF"
            , type: "Offline"
        }
        , {
            code: "ONL"
          , type: "Online"  
        }
        , {
            code: "DIS"
            , type: "Discussion"
        }
        , {
            code: "EXT"
            , type: "Extension"
        }
    ];
        
    $scope.newActivity = new Activity();

    $scope.save = function() {
        // Add curriculum and number to new activity object
        $scope.newActivity.curriculum_rels = [
            {
               curriculumID: curriculumID
               , number: number
            }
        
        ];
        // Save new activity to DB
        console.log("Saving new activity to database.")
        return $scope.newActivity.$save().then(function(result) {
            $modalInstance.close(result);
        }).then(function() {
            return $scope.newActivity = new Activity();
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

activityControllers.controller('ActivityResourcesModalCtrl', ['$scope'
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

activityControllers.controller('ActivityMaterialsModalCtrl', ['$scope'
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

activityControllers.controller('RelatedActivitiesModalCtrl', ['$scope', '$modalInstance', 'Activity', function ($scope, $modalInstance, Activity) {
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);