// Uses Angular-Resource to make calls to the API
// Allows us to avoid hard-coding aspects of the API including constructing URLs
app = angular.module('lms.api', ['ngResource']);

app.factory('Activity', ['$resource', function($resource) {
	$resource('/api/activities/:id', {id:'@id'});
}]);

app.factory('Curriculum', ['$resource', function($resource) {
	$resource('/api/curricula/:id', {id:'@id'});
}]);

app.factory('Resource', ['$resource', function($resource) {
	$resource('/api/resources/:id', {id:'@id'});
}]);

app.factory('Material', ['$resource', function($resource) {
	$resource('/api/materials/:id', {id:'@id'});
}]);