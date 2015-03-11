
app = angular.module('lms.app.curricula', ['lms.api', 'ui.bootstrap']);

app.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});

app.controller('CurriculumCtrl', ['$scope', '$modal', 'Curriculum', function($scope, $modal, Curriculum){
	$scope.curricula = [];

    // curricula accordion expands to display one curriculum at a time
    $scope.oneAtATime = true;

    // query API for curricula and inherit tags from nested activities
	$scope.curricula = Curriculum.query(function() {
        // curriculum inherits tags from activities
        for (i = 0; i < $scope.curricula.length; i++) {
            $scope.curricula[i].tags = [];
            curr = $scope.curricula[i];
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
                            $scope.curricula[i].tags.push(tag);
                            tagNames.push(tag.name);
                        }
                    }
                }
            }
        } 
    });

    // function to check whether objects in the HTML template are defined
    // we are checking URLS as strings to avoid javascript parse errors
    // also checking lists
    $scope.notEmpty = function(x) {
      return (x.length > 0);
    };

    // open modal window to create new curriculum
    $scope.newCurriculum = function (size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/new-curriculum.html',
            controller: 'NewCurrModalCtrl',
            size: size
        });

        // add newly created curriculum to list on the page (without refresh)
        modalInstance.result.then(function (newCurriculum) {
            $scope.curricula.push(newCurriculum);
        });
    };

    // open modal window to create new activity
    $scope.newActivity = function (size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/new-activity.html',
            controller: 'NewActivityModalCtrl',
            size: size
        });
    };
    // open modal window to view activity resources
    $scope.activityResources = function (size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/activity-resources.html',
            controller: 'ActivityResourcesModalCtrl',
            size: size
        });
    };
    // open modal window to view activity materials
    $scope.activityMaterials = function (size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/activity-materials.html',
            controller: 'ActivityMaterialsModalCtrl',
            size: size
        });
    };
    // open modal window to view related activities
    $scope.relatedActivities = function (size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/related-activities.html',
            controller: 'RelatedActivitiesModalCtrl',
            size: size
        });
    };
}]);

app.controller('NewCurrModalCtrl', ['$scope', '$modalInstance', 'Curriculum', 'Activity', function ($scope, $modalInstance, Curriculum, Activity) {
    
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
        // if the user selected an activity in the input form, let's assign it as the 1st activity in the curriculum
        if ($scope.newCurriculum.activities) {
            $scope.newCurriculum.activities = [{"activity":$scope.newCurriculum.activities, "number":1}];
        };

        return $scope.newCurriculum.$save().then(function(result) {
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

app.controller('NewActivityModalCtrl', ['$scope', '$modalInstance', 'Activity', 'Tag', function ($scope, $modalInstance, Activity, Tag) {
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

app.controller('ActivityResourcesModalCtrl', ['$scope', '$modalInstance', 'Resource', function ($scope, $modalInstance, Resource) {
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);

app.controller('ActivityMaterialsModalCtrl', ['$scope', '$modalInstance', 'Material', function ($scope, $modalInstance, Material) {
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