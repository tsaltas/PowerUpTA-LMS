
app = angular.module('lms.app.curricula', ['lms.api', 'ui.bootstrap']);

app.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});

app.controller('CurriculumCtrl', ['$scope', '$modal', 'Curriculum', 'Activity', function($scope, $modal, Curriculum, Activity){
	$scope.curricula = [];

	$scope.curricula = Curriculum.query(function() {
        // curriculum inherits tags from activities
        for (i = 0; i < $scope.curricula.length; i++) {
            $scope.curricula[i].tags = [];
            curr = $scope.curricula[i];
            for (j = 0; j < curr.activities.length; j++) {
                activity = curr.activities[j].activity;
                for (k = 0; k < activity.tags.length; k++) {
                    tag = activity.tags[k];
                    category = tag.category;
                    // only inherit language and technology tags
                    if (category == "Language" | category == "Technology") {
                        if ( $scope.curricula[i].tags.indexOf(tag) == -1) {
                            $scope.curricula[i].tags.push(tag);
                        }
                    }
                }
            }
        } 
    });

    // TODO: remove duplicate tags in curriculum

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

    // list of activities for new curriculum form
    $scope.activities = [];
    $scope.activities = Activity.query();

    // open modal window to create new curriculum
    $scope.open = function (size) {
        var modalInstance = $modal.open({
            templateUrl: 'static/partials/new-curriculum.html',
            controller: 'NewCurrModalCtrl',
            size: size,
            resolve: {
                activities: function () {
                    return $scope.activities;
                },
                grades: function () {
                    return $scope.grades;
                }
            }
        });

        // add newly created curriculum to list on the page (without refresh)
        modalInstance.result.then(function (newCurriculum) {
            $scope.curricula.push(newCurriculum);
        });
    };

    // accordion interface options for expanding curricula
    $scope.oneAtATime = true;
}]);

app.controller('NewCurrModalCtrl', ['$scope', '$modalInstance', 'Curriculum', 'activities', 'grades', function ($scope, $modalInstance, Curriculum, activities, grades) {
    
    $scope.activities = activities;
    $scope.grades = grades;
    
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

app.controller('DropdownCtrl', ['$scope', function ($scope) {
  
  $scope.status = {
    isopen: false,
  };

  $scope.toggleDropdown = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.status.isopen = !$scope.status.isopen;
  };
  
}]);