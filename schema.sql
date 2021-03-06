CREATE TABLE public.users
(
    id         integer GENERATED BY DEFAULT AS IDENTITY NOT NULL,
    first_name text                                     NOT NULL,
    last_name  text                                     NOT NULL,
    birth_date timestamp                                NOT NULL,
    created    timestamptz DEFAULT CURRENT_TIMESTAMP    NOT NULL,
    updated    timestamptz NULL,
    deleted    timestamptz NULL,

    CONSTRAINT pk_users PRIMARY KEY (id)
);

