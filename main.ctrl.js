angular.module('app').controller("MainController", function(){
    var vm = this;
    vm.title = 'drop&dip';
    vm.searchInput = '';
    vm.notes = [];
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
    };
    

});