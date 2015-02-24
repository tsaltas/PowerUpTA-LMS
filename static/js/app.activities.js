app = angular.module('lms.app.activities', ['lms.api']);

app.controller('ActivityCtrl', ['$scope', 'Activity', function($scope, Activity){
	return $scope.activities = Activity.query();
}]);