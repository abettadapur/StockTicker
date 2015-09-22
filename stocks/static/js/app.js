
'use strict';
var StockTrackerApp = angular.module('StockTrackerApp', []);

StockTrackerApp.controller('StockTrackerCtrl1', function ($scope, $http) {
  $http.get('api/stocks').success(function(data) {
    $scope.stocks = data;
  });
});
