app = angular.module('lms.app.editor', ['lms.api']);

app.controller('ActivityCtrl', ['$scope', 'Activity', function($scope, Activity){
	return $scope.activities = Activity.query();
}]);

app.controller('CurriculumCtrl', ['$scope', 'Curriculum', function($scope, Curriculum){
	return $scope.curricula = Curriculum.query();
}]);