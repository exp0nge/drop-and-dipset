app.controller("MainController", ['$timeout', 'login', 'logout', function($timeout, login, logout){
    var vm = this;
    vm.title = 'drop&dip';
    vm.searchInput = '';
    vm.notes = [];
    vm.noteAdded = false;
    var savedNotes = JSON.parse(window.localStorage.getItem('storedNotes'));
    if(savedNotes){
        vm.notes = savedNotes;
    }
    vm.newNote = {};
    vm.addNote = function(){
        vm.newNote.date = new Date();
        vm.notes.push(vm.newNote);
        vm.newNote = {};
        window.localStorage.setItem('storedNotes', JSON.stringify(vm.notes));
        vm.noteAdded = true;
        $timeout(function(){vm.noteAdded = false;}, 3000);
    };
    vm.delete = function(note){
        vm.notes.splice(vm.notes.indexOf(note), 1);
        window.localStorage.setItem('storedNotes', JSON.stringify(vm.notes));
    };
    vm.download = function(){
        var blob = new Blob([JSON.stringify(vm.notes)], {type: 'application/json; charset=utf-8;'});
        window.location.href = (window.URL || window.webkitURL).createObjectURL( blob );
    };
    vm.loginFormData = {};
    vm.showLogin = function(){
        vm.loginForm = true;
    };
    vm.login = function(){
        login.login(vm.loginFormData).then(function(response){
            vm.loginForm = false;
            vm.loggedIn = true;
            console.log(response);
        })
    };
    vm.logout = function(){
        logout.then(function(response){
            console.log(response);
            vm.loggedIn = false;
        },
        function(err){
            console.log(err);
        })
    };
    

}]);