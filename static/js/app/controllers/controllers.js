'use strict';

var lessonsControllers = angular.module('lms.controllers', [
    , 'resourceControllers'
    , 'materialControllers'
    , 'tagControllers'
    , 'activityControllers'
    , 'curriculumControllers'
]);

lessonsControllers.controller('DropdownCtrl', ['$scope', function ($scope) {
  
  // initialize navbar to collapsed state
  $scope.navbarCollapsed = true;

  $scope.status = {
    isopen: false,
  };

  $scope.toggleDropdown = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.status.isopen = !$scope.status.isopen;
  };
  
}]);