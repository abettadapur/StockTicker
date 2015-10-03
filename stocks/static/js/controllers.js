function HomeController ($scope, StockReport) 
{
    var postsQuery = StockReport.GetReport({stock:"MSFT"}, function (report) {
        $scope.report = report;
    });
}

