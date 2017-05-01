var userApp=angular.module("userApp", []);
userApp.controller("UserController",function ($scope,$http) {
    $scope.users = [];
    $scope.formData = {text:""};
    $scope.Roles=[];
    $http.get('/api/showUser')
        .success(function(data){
            $scope.users = data;
            $http.get('/api/Rol')
                .success(function (data) {
                    $scope.Roles=data;
                });
        });
    $scope.delete = function (id) {
        $scope.formData.text="DELETE";
        $http.post('/api/showUser/'+id,$scope.formData)
            .success(function(data){
                $scope.users = data;
            })
    };

});