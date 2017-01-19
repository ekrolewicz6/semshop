angular.module('product', ['ngRoute', 'firebase'])
 
.value('backendURL', 'http://localhost:5000/endpoints/')
// .service('fbRef', function(fbURL) {
//   return new Firebase(fbURL)
// })
// .service('fbAuth', function($q, $firebase, $firebaseAuth, fbRef) {
//   var auth;
//   return function () {
//       if (auth) return $q.when(auth);
//       var authObj = $firebaseAuth(fbRef);
//       if (authObj.$getAuth()) {
//         return $q.when(auth = authObj.$getAuth());
//       }
//       var deferred = $q.defer();
//       authObj.$authAnonymously().then(function(authData) {
//           auth = authData;
//           deferred.resolve(authData);
//       });
//       return deferred.promise;
//   }
// })
 
.service('Products', function($q, $http) {
  var self = this;
  this.fetch = function () {
    if (this.products) return $q.when(this.products);
    return $http.get('http://localhost:5000/endpoints/' + 'products').then(function(response) {
      var deferred = $q.defer();
      self.products = response.data;
      deferred.resolve(self.products);
      return deferred.promise;
    });
  };
})

.service('Categories', function($q, $http) {
  var self = this;
  this.fetch = function () {
    if (this.categories) return $q.when(this.categories);
    return $http.get('http://localhost:5000/endpoints/' + 'categories').then(function(response) {
      var deferred = $q.defer();
      self.categories = response.data;
      deferred.resolve(self.categories);
      return deferred.promise;
    });
  };
})

.service('Genes', function($q, $http) {
  var self = this;
  this.fetch = function (category_id) {
    if (this.genes) return $q.when(this.genes);
    return $http.get('http://localhost:5000/endpoints/' + 'genes/' + category_id.toString()).then(function(response) {
      var deferred = $q.defer();
      self.genes = response.data;
      deferred.resolve(self.genes);
      return deferred.promise;
    });
  };
})
 
.config(function($routeProvider) {
  var resolveProducts = {
    products: function (Products) {
      return Products.fetch();
    }
  };

  var resolveCategories = {
    products: function (Products) {
      return Products.fetch();
    },
    categories: function (Categories) {
      return Categories.fetch();
    }
  };

  var resolveGenes = {
    genes: function (Genes) {
      return Genes.fetch(category_id);
    }
  };
 
  $routeProvider
    .when('/', {
      controller:'ProductListController as productList',
      templateUrl:'/templates/index.html',
      resolve: resolveProducts
    })
    .when('/edit/:productId', {
      controller:'EditProductController as editProduct',
      templateUrl:'/templates/detail.html',
      resolve: resolveProducts
    })
    .when('/new', {
      controller:'NewProductController as editProduct',
      templateUrl:'/templates/detail.html',
      resolve: resolveCategories
    })
    .otherwise({
      redirectTo:'/'
    });
})
 
.controller('ProductListController', function(products) {
  var productList = this;
  productList.products = products;
})
 
.controller('NewProductController', function($scope, $filter, $location, $http, Genes, products, categories) {
  var editProduct = this;
  editProduct.product = {}
  $scope.categories = categories;
  editProduct.save = function() {
    return $http.post('http://localhost:5000/' + 'add_product', editProduct.product).then(function(response) {
      products.push(editProduct.product);
    });
  };
  $scope.loadGenes = function(category) {
    var selected = $filter('filter')($scope.categories, {name: category}, true);
    if (selected.length > 0) $scope.genes = selected[0].genes;
  }

  $scope.addGene = function(category, gene) {
    if (editProduct.product.genes === undefined) editProduct.product.genes = [];
    editProduct.product.genes.push(category + ", " + gene);
  }
})
 
.controller('EditProductController',
  function($location, $routeParams, products) {
    var editProduct = this;
    var productId = $routeParams.productId,
        productIndex;
 
    editProduct.products = products;
    productIndex = editProduct.products.$indexFor(productId);
    editProduct.product = editProduct.products[productIndex];
 
    editProduct.destroy = function() {
        editProduct.products.$remove(editProduct.product).then(function(data) {
            $location.path('/');
        });
    };
 
    editProduct.save = function() {
        editProduct.products.$save(editProduct.product).then(function(data) {
           $location.path('/');
        });
    };
});