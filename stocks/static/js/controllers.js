function HomeController ($scope, $route, StockReport) 
{
    $scope.$route = $route;
    $scope.marketlist = [];
    $scope.filteredlist = [];
    
    StockReport.GetFilteredReports({}, function(stocks){
        $scope.filteredlist = stocks;
    })
    
    StockReport.GetRealtime({ stock: "MSFT" }, function (report) {
        $scope.marketlist.push({symbol: "MSFT", report: report, positive: ((report.change/report.open * 100.0) > 0)});
    });
    StockReport.GetRealtime({ stock: "AAPL" }, function (report) {
        $scope.marketlist.push({symbol: "AAPL", report: report, positive: ((report.change/report.open * 100.0) > 0)});
    });
    StockReport.GetRealtime({ stock: "GOOG" }, function (report) {
        $scope.marketlist.push({symbol: "GOOG", report: report, positive: ((report.change/report.open * 100.0) > 0)});
    });
    StockReport.GetRealtime({ stock: "YHOO" }, function (report) {
        $scope.marketlist.push({symbol: "YHOO", report: report, positive: ((report.change/report.open * 100.0) > 0)});
    });
}

function ChartController($scope, $route, StockReport)
{
    $scope.$route = $route;
    $('#frompicker').datetimepicker(
        {
            format: 'YYYY-MM-DD'
        });
    $('#topicker').datetimepicker(
        {
            format: 'YYYY-MM-DD',
            useCurrent: false
        });

    $('#frompicker').on("dp.change", function (e) {
        $('#topicker').data("DateTimePicker").minDate(e.date);
    });

    $('#topicker').on("dp.change", function (e) {
        $('#frompicker').data("DateTimePicker").maxDate(e.date);
    });

    $scope.chartHeading = "Enter a symbol above";
    $scope.loading = false;

    $scope.loadChart = function (symbol) {
        $scope.loading = true;
        $scope.chartHeading = "Loading...";
        fromdate = $("#frompicker").data("date");
        todate = $("#topicker").data("date");

        $("#morris-area-chart").empty();
        var historyQuery = StockReport.GetChart({ stock: symbol.toUpperCase(), from: fromdate, to: todate }, function (points) {
            Morris.Line({
                element: "morris-area-chart",
                data: points,
                xkey: 'Date',
                ykeys: ['Close'],
                labels: ['Price'],
                pointSize: 0,
                hideHover: 'auto',
                resize: true
            });
            $scope.chartHeading = "Historical data for " + symbol.toUpperCase();
            $scope.loading = false;
        });
        
    };
    
    
}

