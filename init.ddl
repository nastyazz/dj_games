CREATE SCHEMA games_data;
drop table if exists games_data.games, games_data.comment, games_data.client, games_data.games_to_client, games_data.genre, games_data.games_to_genre cascade;
CREATE extension if not exists "uuid-ossp";

create table games_data.games
(
    id         uuid primary key default uuid_generate_v4(),
    title text,
    genre  text,
    price float
);

create table games_data.genre
(
    id uuid primary key default uuid_generate_v4(),
    title text
);

create table games_data.comment
(
    id          uuid primary key default uuid_generate_v4(),
    description      text,
    date_public timestamp,
    estimation float,
    game_id uuid references games_data.games not null
);


create table games_data.client
(
    id          uuid primary key default uuid_generate_v4(),
    nickname       text,
    date_registrate timestamp,
    money float,
    user_id int references public.auth_user
);

create table games_data.games_to_client
(
    id uuid default uuid_generate_v4(),
    game_id uuid references games_data.games,
    client_id  uuid references games_data.client,
    primary key (game_id, client_id)
);

create table games_data.games_to_genre
(
    id uuid default uuid_generate_v4(),
    game_id uuid references games_data.games,
    genre_id  uuid references games_data.genre,
    primary key (game_id, genre_id)
);