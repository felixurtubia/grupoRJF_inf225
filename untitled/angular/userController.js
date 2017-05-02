var userApp=angular.module("userApp", []);
userApp.controller("UserController",function ($scope,$http) {
    $scope.users = [];
    $scope.formData = {text:""};
    $http.get('/api/usuarios')
        .success(function(data){
            $scope.users = data;
        });
    $scope.delete = function (id) {
        $scope.formData.text="DELETE";
        $http.post('/api/usuarios'+id,$scope.formData)
            .success(function(data){
                $scope.users = data;
            })
    };
});