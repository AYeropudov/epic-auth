create table alembic_version
(
  version_num varchar(32) not null
    primary key
);

create table user
(
  id            int auto_increment
    primary key,
  user_name     varchar(64)  null,
  email         varchar(120) null,
  password_hash varchar(128) null,
  constraint ix_user_email
    unique (email),
  constraint ix_user_user_name
    unique (user_name)
);

create table token
(
  id      int auto_increment
    primary key,
  user_id int         null,
  access  varchar(40) null,
  constraint token_ibfk_1
    foreign key (user_id) references user (id)
);

create index user_id
  on token (user_id);

