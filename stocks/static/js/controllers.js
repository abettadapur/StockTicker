function HomeController ($scope, StockReport) 
{
    var postsQuery = StockReport.GetReport({}, function (report) {
        $scope.report = report;
    });
}

