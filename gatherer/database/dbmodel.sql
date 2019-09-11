create role genesis with login
;

create database genesis with owner genesis
;

create table coins
(
	id serial not null,
	coin varchar(20) not null,
	constraint coins_id_coin_pk
		primary key (id, coin)
)
;

create unique index coins_id_uindex
	on coins (id)
;

create table coins_history
(
	time bigint not null,
	coin_id integer not null
		constraint coins_history_coins_id_fk
			references coins (id)
				on update cascade on delete cascade,
	open double precision not null,
	close double precision not null,
	high double precision not null,
	low double precision not null,
	constraint coins_history_time_coin_id_pk
		primary key (time, coin_id)
)
;