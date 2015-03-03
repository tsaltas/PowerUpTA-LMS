app = angular.module('lms.app.editor', ['lms.api', 'ui.bootstrap']);

app.controller('NewCurrCtrl', ['$scope', '$modal', '$log', 'Activity', function ($scope, $modal, $log, Activity) {

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

    $scope.open = function (size) {
        var modalInstance = $modal.open({
            templateUrl: 'myModalContent.html',
            controller: 'NewCurrModalCtrl',
            size: size,
            resolve: {
                activities: function () {
                    return $scope.activities;
                },
                grades: function () {
                    return $scope.grades;
                },
                curricula: function () {
                    return $scope.curricula;
                }
            }
        });

        modalInstance.result.then(function (curricula) {
            $scope.curricula = curricula;
        });
    };
}]);

app.controller('NewCurrModalCtrl', ['$scope', '$modalInstance', 'Curriculum', 'activities', 'grades', 'curricula', function ($scope, $modalInstance, Curriculum, activities, grades, curricula) {
    
    $scope.activities = activities;
    $scope.grades = grades;
    $scope.curricula = curricula;
    
    $scope.newCurriculum = new Curriculum();

    $scope.save = function() {
        // if the user selected an activity in the input form, let's assign it as the 1st activity in the curriculum
        if ($scope.newCurriculum.activities) {
            $scope.newCurriculum.activities = [{"activity":$scope.newCurriculum.activities, "number":1}];
        };

        return $scope.newCurriculum.$save().then(function(result) {
            $modalInstance.close($scope.curricula.push(result));
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