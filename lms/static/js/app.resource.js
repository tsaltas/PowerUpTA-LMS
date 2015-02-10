app = angular.module('lms.app.resource', ['lms.api']);

app.controller('AppController', ['$scope', 'Activity', function($scope, Activity){
	return $scope.activities = Activity.query();
}]);