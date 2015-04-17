'use strict';

/* Curriculum Module Controllers */

var curriculumControllers = angular.module('curriculumControllers', []);

curriculumControllers.controller('CurriculumCtrl', ['$scope'
    , '$modal'
    , 'Curriculum'
    , 'Activity'
    , 'Tag'
    , function($scope
        , $modal
        , Curriculum
        , Activity
        , Tag
    ){

	$scope.curricula = [];

    // curricula accordion expands to display one curriculum at a time
    $scope.oneAtATime = true;

    // curriculum inherits tags from nested activities
    var getCurriculumTags = function(curricula) {
        // curriculum inherits tags from activities
        for (var i = 0; i < curricula.length; i++) {
            curricula[i].tags = [];
            var curr = curricula[i];
            var tagNames = []
            for (var j = 0; j < curr.activities.length; j++) {
                var activity = curr.activities[j].activity;
                for (var k = 0; k < activity.tags.length; k++) {
                    var tag = activity.tags[k];
                    // only inherit language and technology tags
                    if (tag.category == "Language" | tag.category == "Technology") {
                        // do not add duplicates to list
                        // tag names should be unique (enforced by API)
                        if (tagNames.indexOf(tag.name) == -1) {
                            curricula[i].tags.push(tag);
                            tagNames.push(tag.name);
                        }
                    }
                }
            }
        } 
    };

    // query API for curricula
	$scope.curricula = Curriculum.query(getCurriculumTags);

    // Function to check whether objects in the HTML template are defined
    // Some objects we want to hide are actually undefined
    // Others are empty lists or empty strings, so x.length checks those
    $scope.notEmpty = function(x) {
        if (typeof(x) != "undefined") {
            return (x.length > 0);
        }
        else return false;

    };

    // Function to determine if object is in a list
    // Checks objects by id
    function containsObject(list, obj) {
        var res = _.find(list, function(val){return obj.id == val.id});
        return (_.isUndefined(res))? false:true;
    };

    // list of tags to add tag to lesson
    $scope.tags = [];
    $scope.tags = Tag.query();

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
    $scope.newActivity = function (curriculum, size) {
        console.log("Inside new activity function.");
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
        
        // Add newly created activity to list on the page (without refresh)
        modalInstance.result.then(function (newActivity) {
            console.log("Successfully created new activity:");
            console.log(newActivity);

            console.log("Querying for updated curriculum");
            curriculum = Curriculum.get({ id:curriculum.id }, function() {
                // update curriculum scope variable with new activity
                console.log("Updating scope variable");
                for (var i = 0; i < $scope.curricula.length; i++) {
                    if ($scope.curricula[i].id == curriculum.id) {
                        $scope.curricula[i].activities.push(curriculum.activities[curriculum.activities.length - 1]);
                        // update curriculum tags with tags on activity
                        _.each(newActivity.tags, function (value, key, list) {
                            if (containsObject($scope.curricula[i].tags, value) == false) {
                                $scope.curricula[i].tags.push(value);
                            }
                        });
                    }
                }
            });
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
            // add tag to curriculum (on front-end)
            if (containsObject(curriculum.tags, addTag) == false) {
                curriculum.tags.push(addTag);
            }

            // Add tag to activity (back-end and front-end)
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
            
            // Add new tag to curriculum (front-end)
            // Add new tag to activity (back-end and front-end)
            // Add to the drop-down selection menu
            modalInstance.result.then(function (newTag) {
                curriculum.tags.push(newTag);
                activity = addTagActivity(activity, newTag);
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
}]);

curriculumControllers.controller('NewCurrModalCtrl', ['$scope'
    , '$modalInstance'
    , 'Curriculum'
    , 'Activity'
    , function ($scope
        , $modalInstance
        , Curriculum
        , Activity
    ) {
    console.log("Inside new curriculum modal window controller.");
    // list of activities for new curriculum form
    $scope.activities = [];
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
        // If the user selected an activity in the input form, assign it as the 1st activity in the curriculum
        if ($scope.newCurriculum.activity_rels) {
            console.log("Associating first activity with new curriculum.");
            $scope.newCurriculum.activity_rels = [
                {
                    "activityID":$scope.newCurriculum.activity_rels
                    , "number":1
                }
            ];
        }
        console.log("Saving new curriculum to database.");
        return $scope.newCurriculum.$save().then(function(result) {
            // change grades on new curriculum from DB storage value to display value
            result.lower_grade = $scope.grades[result.lower_grade].value;
            result.upper_grade = $scope.grades[result.upper_grade].value;
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