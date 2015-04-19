'use strict';

/* Lessons Services Module */

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

// Some utility services
lessonsServices.service('utilitiesService', function() {
    // Function to determine if object is in a list
    // Checks objects by id
    this.containsObject = function(list, obj) {
        var res = _.find(list, function(val){return obj.id == val.id});
        return (_.isUndefined(res))? false:true;
    };
});

lessonsServices.service('inheritTagsService', [
    'utilitiesService'
    , function(
        utilitiesService
    ){
    
    // Function takes a curriculum and activity and inherits tags
    this.getTagsFromActivity = function(curriculum, activity) {
        if (!curriculum.tags) curriculum.tags = [];

        _.each(activity.tags, function (tag, index, list) {
            // only inherit language and technology tags
            if (tag.category == "Language" | tag.category == "Technology") {
                // do not add duplicates to list
                if (!utilitiesService.containsObject(curriculum.tags, tag)) {
                    curriculum.tags.push(tag);
                }
            }
        });
        return curriculum;
    };

    // Function adds a tag to curriculum if tag has the right type
    this.addTagToCurriculum = function(curriculum, tag) {
        if (!curriculum.tags) curriculum.tags = [];
        if (tag.category == "Language" | tag.category == "Technology") {
            // do not add duplicates to list
            if (!utilitiesService.containsObject(curriculum.tags, tag)) {
                curriculum.tags.push(tag);
            }
        }
        return curriculum;
    };

   // Function takes a list of curricula and inherits tags from activities
    this.getCurriculaTags = function(curricula) {
        _.each(curricula, function (curriculum, index, list) {
        curriculum.tags = []
            _.each(curriculum.activities, function (activity, index, list) {
                _.each(activity.tags, function (tag, index, list) {
                    // only inherit language and technology tags
                    if (tag.category == "Language" | tag.category == "Technology") {
                        // do not add duplicates to list
                        if (!utilitiesService.containsObject(curriculum.tags, tag)) {
                            curriculum.tags.push(tag);
                        }
                    }
                });
            });
        });
    };
}]);


// Submit PATCH request to API adding a new activity to a curriculum
lessonsServices.service('addActivityService', [
    'Curriculum'
    , 'utilitiesService'
    , 'inheritTagsService'
    , function (
        Curriculum
        , utilitiesService
        , inheritTagsService
    ){
    this.addActivity = function(curriculum, newActivity) {
        console.log("Checking if activity is already on curriculum.");
        if (utilitiesService.containsObject(curriculum.activities, newActivity)) {
            return curriculum;
        }

        console.log("Creating list of activities to update curriculum:");
        // Create new list of activity IDs for curriculum
        var activityList = []
        _.each(curriculum.activities, function (activity, index, list) {
            activityList.push(
                {
                    'activityID': activity.id
                    , 'number': index + 1 // indices start at 1
                }
            );
        });
        activityList.push(
            {
                'activityID': newActivity.id
                , 'number': activityList.length + 1 // indices start at 1
            }
        );
        console.log(activityList);

        // Add activity to curriculum on back-end (custom "PATCH" request to API)
        // Also update activities of curriculum displayed on front-end
        console.log("Making PATCH request to add new activity to curriculum:");
        Curriculum.update({ id:curriculum.id }, {'activity_rels': activityList}, function(response) {
            curriculum.activities = response.activities;
        });

        // Update curriculum tags
        console.log("Updating curriculum tags.");

        // Inherit tags from activities
        curriculum = inheritTagsService.getTagsFromActivity(curriculum, newActivity);

        console.log("Returning updated curriculum:");
        // Return updated curriculum with new activity
        return curriculum;
    }
}]);