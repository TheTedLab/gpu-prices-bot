CREATE TABLE architectures
(
    id serial PRIMARY KEY,
    architecture_name varchar(100) NOT NULL
);

CREATE TABLE gpus
(
    id serial PRIMARY KEY,
    gpu_name varchar(100) NOT NULL,
    architecture_id integer  NOT NULL REFERENCES architectures (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    gpu_series varchar(100) NOT NULL
);

CREATE TABLE shops
(
    id serial PRIMARY KEY,
    shop_name varchar(100) NOT NULL
);

CREATE TABLE vendors
(
    id serial PRIMARY KEY,
    vendors_name varchar(100) NOT NULL
);

CREATE TABLE offers
(
    offer_id serial PRIMARY KEY,
    gpu_id integer NOT NULL REFERENCES gpus (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    shop_id integer NOT NULL REFERENCES shops (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    vendor_id integer NOT NULL REFERENCES vendors (id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    price integer NOT NULL CONSTRAINT price_check CHECK (price > 0),
    aggregate_date date NOT NULL,
    popularity_place integer NOT NULL CONSTRAINT popularity_check CHECK (popularity_place > 0)
);