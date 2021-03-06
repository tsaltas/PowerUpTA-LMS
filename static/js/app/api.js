'use strict';

/* Lessons API Module */

// Uses Angular-Resource to make calls to the API
// Allows us to avoid hard-coding aspects of the API including constructing URLs
var api = angular.module('lms.api', ['ngResource']);

api.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});

api.factory('Activity', ['$resource', function($resource) {
	return $resource('/api/activities/:id', {id:'@id'}, 
		// Custom PUT method called "update"
		// Usage: Activity.update({ id:$id }, {});
		{
			'update' : {
				method: 'PATCH'
				//, headers: {'Content-Type': 'application/json;charset=utf-8'}
			}
		}
	);
}]);

api.factory('Curriculum', ['$resource', function($resource) {
	return $resource('/api/curricula/:id', {id:'@id'},
		// Custom PUT method called "update"
		// Usage: Curriculum.update({ id:$id }, {});
		{
			'update' : {
				method: 'PATCH'
				//, headers: {'Content-Type': 'application/json;charset=utf-8'}
			}
		}
	);
}]);

api.factory('Resource', ['$resource', function($resource) {
	return $resource('/api/resources/:id', {id:'@id'});
}]);

api.factory('Material', ['$resource', function($resource) {
	return $resource('/api/materials/:id', {id:'@id'});
}]);

api.factory('Tag', ['$resource', function($resource) {
	return $resource('/api/tags/:id', {id:'@id'});
}]);

api.factory('Step', ['$resource', function($resource) {
	return $resource('/api/steps/:id', {id:'@id'});
}]);