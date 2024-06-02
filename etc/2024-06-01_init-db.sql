CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    version VARCHAR NOT NULL,
    model VARCHAR NOT NULL,
    serial-number VARCHAR NOT NULL
);
