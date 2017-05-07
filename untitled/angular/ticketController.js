var ticketApp=angular.module("ticketApp", []);

var isDefined = angular.isDefined,
    isUndefined = angular.isUndefined,
    isFunction = angular.isFunction,
    isString = angular.isString,
    isNumber = angular.isNumber,
    isObject = angular.isObject,
    isArray = angular.isArray,
    forEach = angular.forEach,
    extend = angular.extend,
    copy = angular.copy,
    equals = angular.equals;


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

ticketApp.filter('filterBy', ['$parse', function( $parse ) {
        return function(collection, properties, search, strict) {
            var comparator;

            search = (isString(search) || isNumber(search)) ?
                String(search).toLowerCase() : undefined;

            collection = isObject(collection) ? toArray(collection) : collection;

            if(!isArray(collection) || isUndefined(search)) {
                return collection;
            }

            return collection.filter(function(elm) {
                return properties.some(function(prop) {

                    /**
                     * check if there is concatenate properties
                     * example:
                     * object: { first: 'foo', last:'bar' }
                     * filterBy: ['first + last'] => search by full name(i.e 'foo bar')
                     */
                    if(!~prop.indexOf('+')) {
                        comparator = $parse(prop)(elm)
                    } else {
                        var propList = prop.replace(/\s+/g, '').split('+');
                        comparator = propList
                            .map(function(prop) { return $parse(prop)(elm); })
                            .join(' ');
                    }

                    if (!isString(comparator) && !isNumber(comparator)) {
                        return false;
                    }

                    comparator = String(comparator).toLowerCase();

                    return strict ? comparator === search : comparator.contains(search);
                });
            });
        }
    }]);
ticketApp.filter('fuzzy', function () {
        return function (collection, search, csensitive) {
            var sensitive = csensitive || false;
            collection = isObject(collection) ? toArray(collection) : collection;

            if(!isArray(collection) || isUndefined(search)) {
                return collection;
            }

            search = (sensitive) ? search : search.toLowerCase();

            return collection.filter(function(elm) {
                if(isString(elm)) {
                    elm = (sensitive) ? elm : elm.toLowerCase();
                    return hasApproxPattern(elm, search) !== false
                }
                return (isObject(elm)) ? _hasApproximateKey(elm, search) : false;
            });

            /**
             * checks if object has key{string} that match
             * to fuzzy search pattern
             * @param object
             * @param search
             * @returns {boolean}
             * @private
             */
            function _hasApproximateKey(object, search) {
                var properties = Object.keys(object),
                    prop, flag;
                return 0 < properties.filter(function (elm) {
                        prop = object[elm];

                        //avoid iteration if we found some key that equal[performance]
                        if(flag) return true;

                        if (isString(prop)) {
                            prop = (sensitive) ? prop : prop.toLowerCase();
                            return flag = (hasApproxPattern(prop, search) !== false);
                        }

                        return false;

                    }).length;
            }
        }
    });

ticketApp.filter('where', function() {
        return function (collection, object) {
            if(isUndefined(object)) return collection;
            collection = isObject(collection)
                ? toArray(collection)
                : collection;

            return collection.filter(function (elm) {
                return objectContains(object, elm);
            });
        }
    });