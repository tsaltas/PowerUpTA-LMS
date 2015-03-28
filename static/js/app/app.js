'strict';

var app = angular.module('lms.app', [
    'lms.api'
    , 'ui.bootstrap'
    , 'lms.directives'
    , 'lms.controllers'
]);

// Don't strip trailing slashes from calculated URLs
// The Django API expects slashes
app.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});