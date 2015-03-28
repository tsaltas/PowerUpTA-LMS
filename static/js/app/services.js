'use strict';

/* Lessons Module Controllers */

var lessonsServices = angular.module('lms.services', []);

// File upload service
// Makes the HTTP POST request to the server
lessonsServices.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl){
        var fd = new FormData();
        fd.append('file', file);
        $http.post(uploadUrl, fd, {
            // override default transformRequest function
            // by default, angular serializes the request to JSON data
            // we want to leave the file data intact so use the identify function
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(){
        })
        .error(function(){
        });
    }
}]);