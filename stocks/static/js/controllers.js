'use strict';
var stockApp = angular.module('StockTrackerApp', ['ngRoute']);

stockApp.config(function ($routeProvider) {
    $routeProvider.when('/', {
        templateUrl: 'static/pages/home.html',
        controller: 'homeController'
    });
});

stockApp.controller('homeController', function ($scope, $http) {
    $http.get('/api/stocks/AAPL/report')
        .success(function (response) {
            $scope.particularStock =
                response;
        });
});