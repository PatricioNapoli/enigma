# Enigma

Stands for Enveloping of Information and Gateway Managing

# Install
> pip install -r requirements.txt

# Run (Python 3.5+ required)
> python -m gatherer

# Usage
- [FULL] `-f EPOCH` to gather currency history from provided epoch to now.
- [REALTIME] `-rt STEP` to gather currency values every seconds provided.
- [SYNC] `-s` to synchronize missing data.
- [REALTIME]+[FULL] `-rtf STEP EPOCH` gathers history since epoch and then starts realtime tracking.
- [REALTIME]+[SYNC] `-rts STEP` synchronizes then starts realtime tracking.
- EPOCH default: 1451692800 (January 1 2016)
- STEP default: 60

# DB Model
>create table coins
(
	id serial not null,
	coin varchar(20) not null,
	constraint coins_id_coin_pk
		primary key (id, coin)
)
;

>create unique index coins_id_uindex
	on coins (id)
;

>create table coins_history
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

