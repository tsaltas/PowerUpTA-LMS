app = angular.module('lms.app.basic', []);

app.controller('AppController', ['$scope', '$http', function($scope, $http){
    $scope.activities = [];

    $http.get('/api/activities').success(function(data) {
    	$scope.activities = data;
    });
}]);