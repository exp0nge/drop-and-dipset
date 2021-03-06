drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  username text not null,
  text text not null,
  date datetime not null
);

drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);
