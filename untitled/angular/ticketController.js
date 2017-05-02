var ticketApp=angular.module("ticketApp", []);
ticketApp.controller("TicketController",function ($scope,$http) {
    $scope.tickets = [];
    $scope.formData = {text:""};
    $http.get('/api/tickets')
        .success(function(data){
            $scope.tickets = data;
        });
    $scope.delete = function (id) {
        $scope.formData.text="DELETE";
        $http.post('/api/tickets'+id,$scope.formData)
            .success(function(data){
                $scope.tickets = data;
            })
    };
});