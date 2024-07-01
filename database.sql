CREATE TABLE IF NOT EXISTS "urls" (
    "id" bigserial PRIMARY KEY,
    "name" varchar(255) UNIQUE NOT NULL,
    "created_at" date NOT NULL 
);

CREATE TABLE IF NOT EXISTS "url_checks" (
    "id" bigserial PRIMARY KEY,
    "url_id" bigint REFERENCES "urls"("id") NOT NULL,
    "status_code" int,
    "h1" varchar(255),
    "title" varchar(255),
    "description" text,
    "created_at" date NOT NULL 
);