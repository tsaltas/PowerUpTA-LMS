'use strict';

/* Activity Module Controllers */

var activityControllers = angular.module('activityControllers', []);

activityControllers.controller('NewActivityModalCtrl', ['$scope'
    , '$modalInstance'
    , '$modal'
    , 'Activity'
    , 'Tag'
    , 'curriculumID'
    , 'number'
    , function ($scope
        , $modalInstance
        , $modal
        , Activity
        , Tag
        , curriculumID
        , number
    ) {

    console.log("Inside new activity modal window controller.");
    // list of tags for new activity form
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
        console.log("Saving new activity to database.");
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

    // open modal window to create new tag 
    $scope.newTag = function (size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/new-tag.html',
            controller: 'NewTagModalCtrl',
            size: size,
            resolve: {
                activityID: function () {
                    return null;
                }
            }
        });
        
        modalInstance.result.then(function (newTag) {
            // Add to the drop-down selection menu
            $scope.tags.push(newTag);
        });
    };
}]);

activityControllers.controller('EditActivityModalCtrl', ['$scope'
    , '$modalInstance'
    , '$modal'
    , 'Activity'
    , 'Tag'
    , 'activity'
    , function ($scope
        , $modalInstance
        , $modal
        , Activity
        , Tag
        , activity
    ) {

    console.log("Inside edit activity modal window controller.");
    // list of tags for new activity form
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
        
    $scope.activity = activity;

    $scope.save = function() {
        // TODO: Update ordering within curriculum

        // Make PATCH request to update activity
        // Update activity object on front-end
        console.log("Saving updated activity to database.");
        Activity.update({ id:activity.id }, {
            'name': activity.name
            , 'tag_IDs': activity.tag_IDs
            , 'teaching_notes': activity.teaching_notes
            , 'video_url': activity.video_url
            , 'category': activity.category

        }, function(response) {
            activity = response;
        });

        // Return updated activity
        return activity;
        // TODO: Handle errors (like when creating a new object)
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    $scope.delete = function () {
        // TODO
    };

    // open modal window to create new tag 
    $scope.newTag = function (size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/new-tag.html',
            controller: 'NewTagModalCtrl',
            size: size,
            resolve: {
                activityID: function () {
                    return null;
                }
            }
        });
        
        modalInstance.result.then(function (newTag) {
            // Add to the drop-down selection menu
            $scope.tags.push(newTag);
        });
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

activityControllers.controller('ActivityStepsModalCtrl', ['$scope'
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

activityControllers.controller('RelatedActivitiesModalCtrl', ['$scope', '$modalInstance', 'Activity', function ($scope, $modalInstance, Activity) {
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);