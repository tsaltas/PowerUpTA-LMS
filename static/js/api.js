// Uses Angular-Resource to make calls to the API
// Allows us to avoid hard-coding aspects of the API including constructing URLs
app = angular.module('lms.api', ['ngResource']);

app.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});

app.factory('Activity', ['$resource', function($resource) {
	return $resource('/api/activities/:id', {id:'@id'});
}]);

app.factory('Curriculum', ['$resource', function($resource) {
	return $resource('/api/curricula/:id', {id:'@id'});
}]);

app.factory('Resource', ['$resource', function($resource) {
	return $resource('/api/resources/:id', {id:'@id'});
}]);

app.factory('Material', ['$resource', function($resource) {
	return $resource('/api/materials/:id', {id:'@id'});
}]);

app.factory('Tag', ['$resource', function($resource) {
	return $resource('/api/tags/:id', {id:'@id'}, {
		'save': {
			method: 'POST'
			, transformRequest: angular.identity
			//, headers: {
			//	'Content-Type': undefined
			//}
		}
	});
}]);