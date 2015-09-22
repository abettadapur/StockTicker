
'use strict';
var StockTrackerApp = angular.module('StockTrackerApp', []);

StockTrackerApp.controller('StockTrackerCtrl1', function($scope, $http) {
    $http.get('/api/stocks/AAPL/report')
        .success(function (response) {
            $scope.particularStock =
                response;
        });
});