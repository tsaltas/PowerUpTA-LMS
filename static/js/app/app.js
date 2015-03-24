'use strict';

/* App Module */

var app = angular.module('lms.app', [
    'lms.api'
    , 'ui.bootstrap'
    , 'lessonsControllers'
    // , 'ngRoute' //uncomment for routing
]);

// Don't strip trailing slashes from calculated URLs
// The DRF API expects slashes
app.config(['$resourceProvider',
    function($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

/*
Routing Example

phonecatApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/phones', {
        templateUrl: 'partials/phone-list.html',
        controller: 'PhoneListCtrl'
      }).
      when('/phones/:phoneId', {
        templateUrl: 'partials/phone-detail.html',
        controller: 'PhoneDetailCtrl'
      }).
      otherwise({
        redirectTo: '/phones'
      });
  }]);

 */