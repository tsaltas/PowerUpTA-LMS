
app = angular.module('lms.app.curricula', ['lms.api', 'ui.bootstrap']);

// Don't strip trailing slashes from calculated URLs
// The Django API expects slashes
app.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});

app.controller('CurriculumCtrl', ['$scope'
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
        for (i = 0; i < curricula.length; i++) {
            curricula[i].tags = [];
            curr = curricula[i];
            tagNames = []
            for (j = 0; j < curr.activities.length; j++) {
                activity = curr.activities[j].activity;
                for (k = 0; k < activity.tags.length; k++) {
                    tag = activity.tags[k];
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
            console.log("Querying for updated curriculum");
            updatedCurricula = Curriculum.query(function() {
                console.log("Adding new activity to curriculum currently displayed on the page.");
                for (var i = 0; i < $scope.curricula.length; i++) {
                    if ($scope.curricula[i].id != updatedCurricula[i].id) {
                        $scope.curricula.push(updatedCurricula[i]);
                    }
                }
            });  
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

app.controller('NewCurrModalCtrl', ['$scope'
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
    for (i = 1; i <= 12; i++) { 
        newGrade = {
            id: i,
            value: i.toString()
        };
        $scope.grades.push(newGrade);
    };
    
    $scope.newCurriculum = new Curriculum();

    $scope.save = function() {
        console.log("Saving new curriculum to database.");
        // if the user selected an activity in the input form, let's assign it as the 1st activity in the curriculum
        if ($scope.newCurriculum.activities) {
            console.log("Associating first activity with new curriculum.");
            $scope.newCurriculum.activities = [{"activity":$scope.newCurriculum.activities, "number":1}];
        };

        return $scope.newCurriculum.$save().then(function(result) {
            // change grades on new curriculum from DB storage value to display value
            result.lower_grade = $scope.grades[result.lower_grade].value;
            result.upper_grade = $scope.grades[result.upper_grade].value;
            // return new curriculum to main controller to update display on page and close the modal window
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

app.controller('NewActivityModalCtrl', ['$scope'
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

app.controller('NewResourceModalCtrl', ['$scope'
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

app.controller('NewMaterialModalCtrl', ['$scope'
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

app.controller('NewTagModalCtrl', ['$scope'
    , '$modalInstance'
    , '$http'
    , 'activityID'
    , 'Tag'
    , function ($scope
        , $modalInstance
        , $http
        , activityID
        , Tag
    ) {

    $scope.newTag = new Tag();

    // list of possible categories for new tag form
    $scope.categories = ["Language", "Technology", "Concept", "Difficulty", "Length"];

    $scope.save = function() {
        // assign correct activity to the new tag
        console.log("Saving new tag.");
        $scope.newTag.activities = [activityID];

        console.log("New tag object: ");
        console.log($scope.newTag);

        // Create multipart/form-data so we can submit the image with the tag
        var fd = new FormData();
        // Use underscore library to loop through properties in the newTag object
        _.each($scope.newTag, function (value, key, list) {
            fd.append(key, list[key]);
        });

        console.log("Submitting HTTP post request: ");

        // Make custom POST request to make sure image is uploaded
        // Cannot use ng-resource request factory for multipart/form-data
        $http({
            method: 'POST',
            url: '/api/tags/',
            data: fd,
            transformRequest: angular.identity,
            // browser will automatically fill in 'multipart/form-data'
            // browser will also supply the boundary parameter
            // manually setting 'multipart/form-data' will fail to add boundary parameter
            headers: {
                'Content-Type': undefined
            }
        }).success(function (result) {
            console.log("Successfully created new Tag!:");
            console.log(result);
            $modalInstance.close(result);
            $scope.newTag = new Tag();
            return $scope.errors = null;
        }).error(function(rejection) {
            console.log("Failed to create new Tag!:");
            console.log(rejection);
            return $scope.errors = rejection;
        });
    };
    
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);

app.controller('ActivityResourcesModalCtrl', ['$scope'
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

app.controller('ActivityMaterialsModalCtrl', ['$scope'
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

app.controller('RelatedActivitiesModalCtrl', ['$scope', '$modalInstance', 'Activity', function ($scope, $modalInstance, Activity) {
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);

app.controller('DropdownCtrl', ['$scope', function ($scope) {
  
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

// File upload directive
// Angular's ng-model does not work on inputs with type='file'
// Gets the file bound to 'my-file-model' in the HTML form into the controller's scope
app.directive('myFileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        // link function listens for changes to the content of the file upload element
        // changes the value of the scope variable appropriately
        link: function(scope, element, attrs) {
            var model = $parse(attrs.myFileModel);
            var modelSetter = model.assign;
            
            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

// File upload service
// Makes the HTTP POST request to the server
app.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl){
        var fd = new FormData();
        fd.append('file', file);
        $http.post(uploadUrl, fd, {
            // override default transformRequest function
            // by default, angular serializes the request to JSON data
            // we want to leave the file data intact so use the identify function
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(){
        })
        .error(function(){
        });
    }
}]);