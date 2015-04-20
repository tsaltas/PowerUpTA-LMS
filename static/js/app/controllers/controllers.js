'use strict';

/* Lessons Module Controllers */

var lessonsControllers = angular.module('lms.controllers', [
    , 'resourceControllers'
    , 'stepControllers'
    , 'materialControllers'
    , 'tagControllers'
    , 'activityControllers'
    , 'curriculumControllers'
    , 'lms.services'
]);

lessonsControllers.controller('AppCtrl', ['$scope'
  , '$modal'
  , 'Curriculum'
  , 'Tag'
  , 'Activity'
  , 'Step'
  , 'addActivityService'
  , 'utilitiesService'
  , 'inheritTagsService'
  , function ($scope
    , $modal
    , Curriculum
    , Tag
    , Activity
    , Step
    , addActivityService
    , utilitiesService
    , inheritTagsService
  ){

    // List of curricula for main app page
    $scope.curricula = Curriculum.query(inheritTagsService.getCurriculaTags);

    // List of tags to add tag to lesson
    $scope.tags = Tag.query();

    // List of activities to add activity to curriculum
    $scope.activities = Activity.query();

    // Function to check whether objects in the HTML template are defined
    // Some objects we want to hide are actually undefined
    // Others are empty lists or empty strings, so x.length checks those
    $scope.notEmpty = function(x) {
        if (typeof(x) != "undefined") {
            return (x.length > 0);
        }
        else return false;

    };

    // Accordion will only display one curriculum at a time
    $scope.oneAtATime = true;

    // open modal window to create new curriculum
    $scope.newCurriculum = function (size) {
        console.log("Inside new curriculum function.");
        console.log("Creating new curriculum modal window.");

        var modalInstance = $modal.open({
            templateUrl: 'static/partials/new-curriculum.html',
            controller: 'NewCurrModalCtrl',
            size: size
        });

        // add newly created curriculum to list on the page (without refresh)
        modalInstance.result.then(function (newCurriculum) {
            console.log("Successfully created new curriculum:");
            console.log(newCurriculum);
            console.log("Adding to curriculum list on page");
            $scope.curricula.push(newCurriculum)
        });
    };

    // open modal window to create new activity
    $scope.newActivity = function (curriculum, addActivity, size) {
        console.log("Inside new activity function.");
        
        // If an existing activity was selected in drop-down menu (it's not undefined)
        if (addActivity) {
            console.log("Adding existing activity to curriculum.");
            curriculum = addActivityService.addActivity(curriculum, addActivity)
        }
        // If user selected "create new activity" (addActivity was undefined)
        // Then open modal window with new activity form
        else {
            console.log("Creating new activity modal window.");

            var modalInstance = $modal.open({
                templateUrl: 'static/partials/new-activity.html',
                controller: 'NewActivityModalCtrl',
                size: size,
                resolve: {
                    curriculumID: function () {
                        return curriculum.id;
                    },
                    number: function() {
                        return curriculum.activities.length + 1;
                    }
                }
            });

            modalInstance.result.then(function (newActivity) {
                console.log("Successfully created new activity:");
                console.log(newActivity);

                // Add newly created activity to curriculum (without page refresh)  
                console.log("Adding new activity to curriculum.");
                curriculum = addActivityService.addActivity(curriculum, newActivity)
            }); 
        }
    };
    
    // open modal window to edit activity
    $scope.editActivity = function (activity, size) {
        console.log("Inside edit activity function.");
        
        // Open modal window with edit activity form
        console.log("Creating modal window to edit activity.");

        var modalInstance = $modal.open({
            templateUrl: 'static/partials/edit-activity.html',
            controller: 'EditActivityModalCtrl',
            size: size,
            resolve: {
                activity: function () {
                    return activity;
                }
            }
        });

        modalInstance.result.then(function (updatedActivity) {
            console.log("Successfully updated activity:");
            console.log(updatedActivity);

            // TODO? Update activity wherever it appears on the page  
        }); 
    };

    // open modal window to create new tag 
    $scope.newTag = function (curriculum, activity, addTag, size) {
        
        // Function to submit PATCH request to API adding a new tag to an activity
        function addTagActivity(activity, newTag) {
            // Create new list of tag IDs for activity
            var tagList = [newTag.id]
            _.each(activity.tags, function (value, key, list) {
                tagList.push(value.id);
            });

            // Add tag to lesson on back-end (custom "PATCH" request to API)
            // Also update tags of activity displayed on front-end
            Activity.update({ id:activity.id }, {'tag_IDs': tagList}, function(response) {
                activity.tags = response.tags;
            });

            // Return updated activity with new tag
            return activity;
        }

        // if an existing tag was selected in drop-down menu (it's not undefined)
        if (addTag) {
            // add tag to curriculum
            curriculum = inheritTagsService.addTagToCurriculum(curriculum, addTag);
            // Add tag to activity
            activity = addTagActivity(activity, addTag)
        }

        // if user selected "create new tag" (addTag was undefined)
        // then open modal window with new tag form
        else {
            var modalInstance = $modal.open({
                templateUrl: 'static/partials/new-tag.html',
                controller: 'NewTagModalCtrl',
                size: size,
                resolve: {
                    activityID: function () {
                        return activity.id;
                    }
                }
            });
            
            modalInstance.result.then(function (newTag) {
                // Add new tag to curriculum
                curriculum = inheritTagsService.addTagToCurriculum(curriculum, newTag);
                // Add new tag to activity (back-end and front-end)
                activity = addTagActivity(activity, newTag);
                // Add to the drop-down selection menu
                $scope.tags.push(newTag);
            });
        }
    };
    // open modal window to view activity resources
    $scope.activityResources = function (activityID, resources, size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/activity-resources.html',
            controller: 'ActivityResourcesModalCtrl',
            size: size,
            resolve: {
                resources: function () {
                    return resources;
                },
                activityID: function () {
                    return activityID;
                }
            }
        });
    };
    // open modal window to view activity materials
    $scope.activityMaterials = function (activityID, materials, size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/activity-materials.html',
            controller: 'ActivityMaterialsModalCtrl',
            size: size,
            resolve: {
                materials: function () {
                    return materials;
                },
                activityID: function () {
                    return activityID;
                }
            }
        });
    };
    // open modal window to view activity steps
    $scope.activitySteps = function (activityID, steps, size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/activity-steps.html',
            controller: 'ActivityStepsModalCtrl',
            size: size,
            resolve: {
                steps: function () {
                    return steps;
                },
                activityID: function () {
                    return activityID;
                }
            }
        });
    };
    /*
    // TODO: open modal window to view related activities
    $scope.relatedActivities = function (relatedActivities, size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/related-activities.html',
            controller: 'RelatedActivitiesModalCtrl',
            size: size,
            resolve: {
                relatedActivities: function () {
                    return relatedActivities;
                }
            }
        });
    };
    */
}]);

lessonsControllers.controller('DropdownCtrl', ['$scope', function ($scope) {
  // initialize navbar to collapsed state
  $scope.navbarCollapsed = true;

  $scope.status = {
    isopen: false,
  };

  $scope.toggleDropdown = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.status.isopen = !$scope.status.isopen;
  };
}]);