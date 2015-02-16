app = angular.module('lms.app.curricula', ['lms.api']);

app.controller('CurriculumCtrl', ['$scope', 'Curriculum', function($scope, Curriculum){
	return $scope.curricula = Curriculum.query();
}]);