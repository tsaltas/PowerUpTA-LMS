'use strict';

/* Lessons Directives Module */

var lessonsDirectives = angular.module('lms.directives', []);

// File upload directive
// Angular's ng-model does not work on inputs with type='file'
// Gets the file bound to 'my-file-model' in the HTML form into the controller's scope
lessonsDirectives.directive('myFileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        // link function listens for changes to the content of the file upload element
        // changes the value of the scope variable appropriately
        link: function(scope, element, attrs) {
            var model = $parse(attrs.myFileModel);
            var modelSetter = model.assign;
            
            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);