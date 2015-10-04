function HomeController ($scope, StockReport) 
{
    var postsQuery = StockReport.GetReport({stock:"MSFT"}, function (report) {
        $scope.report = report;
    });
}

function ChartController($scope, StockReport)
{
    var historyQuery = StockReport.GetChart({ stock: "AAPL", from: "2015-01-01", to: "2015-10-04" }, function (points) {
        Morris.Line({
            element: "morris-area-chart",
            data: points,
            xkey: 'Date',
            ykeys: ['Close'],
            labels: ['Price'],
            pointSize: 0,
            hideHover:'auto',
            resize: true
        });
    });
    
}

