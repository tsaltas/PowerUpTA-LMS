app = angular.module('lms.app.static', []);

app.controller('AppController', ['$scope', '$http', function($scope, $http){
    $scope.activities = [
        {
	        name: "test 1",
	        description: 'This is the first sample post'
	    },
        {
        	name: "test 2",
        	description: 'This is another sample post'
        }
    ];
}]);