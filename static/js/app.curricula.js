app = angular.module('lms.app.curricula', ['lms.api']);

app.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});

app.controller('CurriculumCtrl', ['$scope', 'Curriculum', function($scope, Curriculum){
	$scope.curricula = [];
	return $scope.curricula = Curriculum.query();
}]);