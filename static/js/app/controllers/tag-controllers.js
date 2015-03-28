'use strict';

/* Tag Module Controllers */

var tagControllers = angular.module('tagControllers', []);

tagControllers.controller('NewTagModalCtrl', ['$scope'
    , '$modalInstance'
    , '$http'
    , 'activityID'
    , 'Tag'
    , function ($scope
        , $modalInstance
        , $http
        , activityID
        , Tag
    ) {

    $scope.newTag = new Tag();

    // list of possible categories for new tag form
    $scope.categories = ["Language", "Technology", "Concept", "Difficulty", "Length"];

    $scope.save = function() {
        // assign correct activity to the new tag
        console.log("Saving new tag.");
        $scope.newTag.activities = [activityID];

        console.log("New tag object: ");
        console.log($scope.newTag);

        // Create multipart/form-data so we can submit the image with the tag
        var fd = new FormData();
        // Use underscore library to loop through properties in the newTag object
        _.each($scope.newTag, function (value, key, list) {
            fd.append(key, list[key]);
        });

        console.log("Submitting HTTP post request: ");

        // Make custom POST request to make sure image is uploaded
        // Cannot use ng-resource request factory for multipart/form-data
        $http({
            method: 'POST',
            url: '/api/tags/',
            data: fd,
            transformRequest: angular.identity,
            // browser will automatically fill in 'multipart/form-data'
            // browser will also supply the boundary parameter
            // manually setting 'multipart/form-data' will fail to add boundary parameter
            headers: {
                'Content-Type': undefined
            }
        }).success(function (result) {
            console.log("Successfully created new Tag!:");
            console.log(result);
            $modalInstance.close(result);
            $scope.newTag = new Tag();
            return $scope.errors = null;
        }).error(function(rejection) {
            console.log("Failed to create new Tag!:");
            console.log(rejection);
            return $scope.errors = rejection;
        });
    };
    
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);