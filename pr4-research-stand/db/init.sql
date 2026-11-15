CREATE TABLE items (id BIGINT PRIMARY KEY, name TEXT NOT NULL, payload TEXT NOT NULL);
INSERT INTO items SELECT g, 'item-' || g, md5(g::text) FROM generate_series(1, 1000) g;
